# 04 — Arquitetura de Software (Sprint 1)

O UrbanInventory segue a arquitetura em camadas comum da plataforma UrbanTech.
Cada camada só conhece a camada de baixo. Isso permite testar o núcleo matemático
sem menu e trocar a interface sem mexer na matemática.

## Camadas

```
┌──────────────────────────────────────────────────────────────┐
│ INTERFACE                     app.py                         │
│ menu CLI, leitura do teclado, exibição dos resultados        │
├──────────────────────────────────────────────────────────────┤
│ CAMADA DE APLICAÇÃO           src/services/inventario.py     │
│ cadastros, associações, consultas, RBAC, validações,         │
│ relatório (casos de uso RF01–RF11)                           │
├──────────────────────────────────────────────────────────────┤
│ NÚCLEO MATEMÁTICO             src/algorithms/nucleo_mat.py  │
│ ∪ ∩ − Δ ⊆ complemento, imagem, domínio, composição,          │
│ verificação de função, matriz de pertencimento               │
├──────────────────────────────────────────────────────────────┤
│ ESTRUTURAS DE DADOS / MODELOS src/models/entidades.py        │
│ Ativo, Local, Orgao, Usuario, Papel, Jurisdicao              │
│ dict (tabelas hash), set, tuple, list                        │
├──────────────────────────────────────────────────────────────┤
│ DADOS / I/O                   src/data/                      │
│ manuseio_dados.py (CSV), dados_sinteticos_exemplo.py,       │
│ gerador_inventario.py (sintético)                            │
└──────────────────────────────────────────────────────────────┘
   Transversal: src/utils/excecoes.py, desempenho.py, grafico_svg.py
```

## Módulos

| Módulo | Responsabilidade | Depende de |
|---|---|---|
| `app.py` | Menu, entrada e saída no terminal, tratamento das exceções para mostrar mensagens | services, data, algorithms (só para exibir) |
| `src/services/inventario.py` | Classe `Inventario`: guarda as tabelas, aplica regras de negócio e monta os conjuntos e relações | models, algorithms, utils |
| `src/algorithms/nucleo_mat.py` | Funções matemáticas usadas pela aplicação | nada |
| `src/algorithms/conjuntos.py` | Operações matemáticas e comparação de composição | `nucleo_mat.py` |
| `src/models/entidades.py` | Classes simples com validação de campos | utils.excecoes |
| `src/data/manuseio_dados.py` | Lê `data/raw/*.csv` e exporta para `data/processed/` | services |
| `src/data/dados_sinteticos_exemplo.py` | Mesmo conjunto de dados, embutido em código | services |
| `src/data/gerador_inventario.py` | Gera n ativos aleatórios (semente fixa) para os experimentos | services |
| `src/utils/excecoes.py` | Hierarquia de exceções do domínio | nada |
| `src/utils/desempenho.py` | Experimentos de tempo, memória, cProfile e gráficos | data, algorithms |
| `src/utils/grafico_svg.py` | Desenha gráfico de linhas em SVG sem bibliotecas externas | nada |

## Diagrama de classes (simplificado)

```
┌───────────────┐ 1   * ┌───────────────┐
│    Orgao      │──────▶│    Ativo      │  administra (Orgao.ativos: set)
│ id, nome      │       │ id, tipo      │
│ ativos: set   │       │ jurisdicao ───┼──▶ Jurisdicao (0..1)
└──────▲────────┘       │ manutencao    │
       │ pertence       │ local ────────┼──▶ Local (0..1)
       │ 0..1           └───────────────┘
┌──────┴────────┐ *   * ┌───────────────┐ *   * ┌──────────────┐
│   Usuario     │──────▶│    Papel      │──────▶│  Permissão   │
│ id, nome      │ possui│ nome          │ possui│ (str em P)   │
│ papeis: set   │       │ permissoes:set│       └──────────────┘
│ jurisdicao    │       └───────────────┘
└───────────────┘

            Inventario (fachada da camada de aplicação)
   jurisdicoes: dict   locais: dict   ativos: dict   orgaos: dict
   papeis: dict        usuarios: dict permissoes: set
```

## Estruturas de dados escolhidas

| Dado | Estrutura | Justificativa |
|---|---|---|
| Tabelas de entidades | `dict` {id: objeto} | Busca, inserção e remoção O(1) médio |
| Permissões do sistema (P) | `set` | Validar pertinência em O(1) |
| Papéis de um usuário | `set` | Um usuário pode ter vários papéis, sem repetição |
| Ativos de um órgão | `set` | Relação "administra" sem duplicatas |
| Relações | `set` de `tuple` | Representação literal de R ⊆ X × Y |
| Matriz | `list` de `list` | Ordem fixa de linhas e colunas |

## Fluxo de uma consulta (Sprint 2: entrada → interpretação)

```
Entrada        usuário escolhe "7. Consultar conjuntos", A = Norte, B = Pendentes
   ↓
Validação      Inventario._buscar verifica se a jurisdição existe
   ↓
Estrutura      ativos_da_jurisdicao("Norte") → set ; ativos_com_manutencao_pendente() → set
   ↓
Algoritmo      cj.intersecao(A, B), cj.diferenca(A, B), cj.uniao(A, B)...
   ↓
Resultado      {A2, A5}, {A1}, ...
   ↓
Interpretação  app.py exibe: "A ∩ B = {A2, A5}" → ativos do Norte para consertar
```

## Fluxo do RBAC

```
tem_permissao("U001", "excluir")
   ├─ "excluir" ∈ P ?              não → PermissaoInvalidaError
   ├─ "U001" ∈ usuarios ?          não → EntidadeInexistenteError
   ├─ perms = ⋃ perms(papel)       {consultar, atualizar}
   └─ "excluir" ∈ perms ?          não → False  (exigir_permissao → AcessoNegadoError)
```

## Tratamento de erros (Sprint 3)

```
UrbanInventoryError
 ├── EntidadeInexistenteError   usuário/papel/ativo/órgão/jurisdição não existe
 ├── EntidadeDuplicadaError     ID já cadastrado
 ├── PermissaoInvalidaError     permissão fora de P
 ├── AcessoNegadoError          RBAC negou a ação
 ├── AtivoSemJurisdicaoError    ativo sem jurisdição quando ela é exigida
 └── DadoInvalidoError          campo vazio, arquivo inexistente
```

O `app.py` captura `UrbanInventoryError` e mostra a mensagem: o programa nunca
"quebra" por erro de regra de negócio.

## Decisões e limites de escopo

- **Sem banco de dados**: os dados ficam em memória e em CSV, como pede o escopo.
- **Sem frameworks**: só biblioteca padrão. O matplotlib é usado *se estiver
  instalado*; caso contrário os gráficos saem em SVG gerado à mão.
- **Núcleo puro**: `conjuntos.py` não importa nada do projeto. Isso facilita testar
  e explicar a matemática isoladamente.

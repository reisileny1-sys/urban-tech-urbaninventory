# UrbanInventory — Gestão Relacional do Patrimônio Público

Squad 5 · Plataforma UrbanTech · Matemática Discreta e Algoritmos

Sistema em **Python puro** (só biblioteca padrão) que cadastra ativos públicos
(postes, semáforos, abrigos), suas jurisdições, órgãos responsáveis e usuários, e
responde às consultas usando **Teoria dos Conjuntos**, **Relações**, **Funções** e
**RBAC** (controle de acesso baseado em papéis).

```
A = ativos da Zona Norte        = {A1, A2, A5}
B = ativos com manutenção pend. = {A2, A3, A5, A7, A10}
A ∩ B = {A2, A5}   → ativos do Norte que precisam de manutenção
A − B = {A1}       → ativos do Norte em dia
```

## Como rodar

Precisa só do Python 3.8+. Nada para instalar.

```bash
python app.py                                   # menu de demonstração
python -m unittest discover -s tests -t . -v    # 30 testes unittest
python -m pytest -v                            # 56 testes (suíte completa)
python -m src.utils.desempenho                  # tempo, memória, cProfile e gráficos
```

Opcional (o documento da disciplina pede): `pip install pytest matplotlib` →
`pytest -v` executa a suíte completa e o script de desempenho passa a gerar também PNGs.

## Menu

```
 1. Cadastrar ativo            8. Consultar relações
 2. Cadastrar localização      9. Validar acesso (RBAC)
 3. Cadastrar usuário         10. Gerar relatório
 4. Cadastrar papel           11. Associar ativo à jurisdição
 5. Cadastrar permissão       12. Matriz de pertencimento
 6. Consultar ativos          13. Exportar ativos para CSV
 7. Consultar conjuntos        0. Sair
```

Dados iniciais em `data/raw/*.csv`: 10 ativos, 3 jurisdições, 2 órgãos, 3 papéis e
3 usuários (João = Fiscal, Maria = Administradora, Ana = Visitante + Fiscal).
O ativo A10 está propositalmente **sem jurisdição** (caso de borda).

## Arquitetura

```
INTERFACE            app.py
APLICAÇÃO            src/services/inventario.py     RF01–RF11, RBAC, validações
NÚCLEO MATEMÁTICO    src/algorithms/nucleo_mat.py  ∪ ∩ − Δ ⊆, relações, função, matriz
ESTRUTURAS/MODELOS   src/models/entidades.py        dict, set, tuple, list
DADOS / I/O          src/data/                      CSV, exemplo, gerador sintético
```

## Estrutura do repositório

```
├── app.py                     menu CLI
├── src/
│   ├── models/entidades.py    Ativo, Local, Orgao, Usuario, Papel, Jurisdicao
│   ├── algorithms/nucleo_mat.py  núcleo matemático usado pela aplicação
│   ├── algorithms/conjuntos.py   operações e benchmark de conjuntos
│   ├── services/inventario.py   casos de uso, RBAC, relatório
│   ├── data/                  manuseio_dados.py, dados_sinteticos_exemplo.py,
│   │                           gerador_inventario.py
│   └── utils/                 excecoes.py, desempenho.py, grafico_svg.py
├── tests/                     test_models, test_algorithms, test_services,
│                              test_edge_cases, test_data
├── docs/                      01 a 08 e diagramas de Venn
├── data/raw/                  CSVs de entrada   │ data/processed/  exportações
├── reports/                   complexity/ (CSV + tabelas), profiling/, figures/ (SVG)
├── notebooks/exploration.ipynb
└── LICENSE, requirements.txt
```

## Documentação

| Doc | Conteúdo |
|---|---|
| [01 Visão do produto](docs/01_visao_produto.md) | problema, usuário, entrada, processamento, saída, valor |
| [02 Requisitos](docs/02_requisitos.md) | RF01–RF11 mapeados no código, RNF, casos de uso |
| [03 Modelagem matemática](docs/03_modelagem_matematica.md) | conjuntos, Venn, relações, função, RBAC, matriz |
| [04 Arquitetura](docs/04_arquitetura.md) | camadas, módulos, classes, fluxos, exceções |
| [05 Algoritmos](docs/05_algoritmos.md) | pseudocódigo de cada algoritmo |
| [06 Complexidade](docs/06_complexidade.md) | Big-O + experimentos de tempo e memória |
| [07 Testes](docs/07_testes.md) | 56 testes, os 12 casos do enunciado |
| [08 Resultados](docs/08_resultados.md) | evidências, profiling, limitações |

## Resultados de desempenho (resumo)

- ∪, ∩, −, filtros: **O(n)**, poucos ms para 100 000 ativos
- RBAC: **O(1)**, ~1 µs
- Interseção com `set` x lista: **~900× mais rápida** (n = 5 000)
- Composição indexada x ingênua: **~17× mais rápida** (n = 5 000)
- Memória: **O(n)**, ~320 bytes por ativo

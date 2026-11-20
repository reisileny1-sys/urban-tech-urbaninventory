# 08 — Resultados

## 1. O software resolve o problema? (Dimensão "Problema")

Sim. Com os dados de exemplo (`data/raw/`), o sistema responde às perguntas da
visão do produto:

| Pergunta | Operação | Resposta |
|---|---|---|
| Ativos do Norte com manutenção pendente | A ∩ B | {A2, A5} |
| Ativos do Norte em dia | A − B | {A1} |
| Ativos sem jurisdição | filtro | {A10} |
| Ativo → Jurisdição é função? | `eh_funcao` | Não (A10); após associar, Sim |
| Quais ativos a Ana gerencia? | R2 ∘ R1 | {A2, A6, A9} |
| João pode excluir? | RBAC | **Negado** |
| Maria pode excluir? | RBAC | **Autorizado** |
| Ana (2 papéis) pode atualizar? | ⋃ permissões | **Autorizado** |

### Evidência de execução — relatório (opção 10 do menu, após associar A10 ao Sul)

```
==================================================
RELATÓRIO URBANINVENTORY
==================================================
Total de ativos: 10
Jurisdições: 3 | Órgãos: 2 | Usuários: 3 | Papéis: 3

Ativos por jurisdição:
  Norte      3 ativos |   2 pendentes {A2, A5}
  Sul        4 ativos |   2 pendentes {A3, A10}
  Centro     3 ativos |   1 pendentes {A7}
  Sem jurisdição: ∅

Ativo → Jurisdição é função? SIM

Matriz de pertencimento:
Jurisdição  A1  A2  A3  A4  A5  A6  A7  A8  A9 A10
--------------------------------------------------
Norte        1   1   0   0   1   0   0   0   0   0
Sul          0   0   1   0   0   1   0   1   0   1
Centro       0   0   0   1   0   0   1   0   1   0
```

## 2. Desempenho (Dimensão "Desempenho")

Resumo dos experimentos (detalhes e tabelas em `06_complexidade.md`):

- ∪, ∩, − e filtros crescem **linearmente**: 100 000 ativos → poucos milissegundos.
- RBAC é **constante** (~1 µs), não importa o tamanho do inventário.
- Memória **linear**: ~320 bytes por ativo (~30 MB para 100 000 ativos).
- `set` x lista na interseção: **~900× mais rápido** com n = 5 000.
- Composição indexada x ingênua: **~17× mais rápida** com n = 5 000, e a diferença
  cresce com n porque uma é linear e a outra quadrática.

Gráficos em `reports/figures/` (SVG; PNG se o matplotlib estiver instalado):

| Arquivo | Mostra |
|---|---|
| `conjuntos.svg` | ∪, ∩, − crescendo em linha reta |
| `filtro_matriz.svg` | filtro O(n) x matriz O(k·n) |
| `set_vs_lista.svg` | curva quadrática da lista x reta do set |
| `composicao.svg` | composição ingênua (parábola) x indexada |
| `memoria.svg` | memória linear |

## 3. Profiling (cProfile)

Carga típica com n = 50 000 (`reports/profiling/profile_cumulative.txt`):

| Função | Tempo acumulado | Interpretação |
|---|---|---|
| `relatorio` | ~0.35 s | É a operação mais cara: junta várias consultas |
| `validar_mapeamento_ativo_jurisdicao` | ~0.32 s | Validação das associações e da função |
| `eh_funcao` | ~0.28 s | Contagem de imagens com `dict` |
| `matriz_jurisdicao_ativo` | ~0.19 s | Montagem da matriz de pertencimento |
| `sorted` + `_ordem_natural` | ~0.16 s | Ordenar IDs em ordem natural (A2 antes de A10) |

**Conclusão do profiling:** a matemática básica de conjuntos não é o principal
gargalo. O custo está nas validações, na ordenação e em **apresentar** os dados. Possíveis
otimizações, se necessário:

1. Ordenar as colunas uma vez e guardar (cache) em vez de ordenar a cada chamada.
2. Não imprimir a matriz completa quando n for grande (mostrar só as somas).
3. Manter um índice `jurisdicao → set(ativos)` atualizado nos cadastros, tornando
   `ativos_da_jurisdicao` O(1) em vez de O(n).

## 4. Critérios de aceitação

| Dimensão | Pergunta | Evidência |
|---|---|---|
| Problema | Resolve o problema urbano? | Seção 1 deste documento, menu `app.py` |
| Matemática | Modelo correto? | `03_modelagem_matematica.md`, testes de propriedades |
| Algoritmo | Implementado corretamente? | `05_algoritmos.md`, 56 testes passando |
| Engenharia | Organizado e testado? | `04_arquitetura.md`, `07_testes.md` |
| Desempenho | Sabe explicar a complexidade? | `06_complexidade.md`, gráficos, cProfile |

## 5. Limitações e próximos passos

- Dados em memória/CSV: alterações feitas no menu só persistem se exportadas (opção 13).
- Um ativo tem uma única jurisdição (por regra de negócio); o modelo de relação já
  permitiria várias, se a regra mudar.
- O RBAC não restringe por jurisdição (um fiscal do Norte pode atualizar ativo do
  Sul). Uma evolução natural: `pode(u, a, ativo) ⟺ a ∈ perms(u) ∧ jur(ativo) = jur(u)`.

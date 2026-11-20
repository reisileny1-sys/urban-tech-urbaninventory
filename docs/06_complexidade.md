# 06 — Análise de Complexidade (Sprint 4)

> Pergunta do projeto: **"Como nosso algoritmo se comporta quando o tamanho do
> problema aumenta?"**

Notação: n = nº de ativos, k = nº de jurisdições, |A|, |B| = tamanhos dos conjuntos,
|R|, |S| = nº de pares das relações, r = papéis por usuário, q = permissões por papel.

## 1. Complexidade teórica

| Operação | Função | Tempo | Espaço |
|---|---|---|---|
| Buscar entidade por ID | `Inventario._buscar` | O(1) médio | O(1) |
| Cadastrar ativo/usuário | `cadastrar_*` | O(1) médio | O(1) |
| A ∪ B | `cj.uniao` | O(\|A\| + \|B\|) | O(\|A\| + \|B\|) |
| A ∩ B | `cj.intersecao` | O(min(\|A\|, \|B\|)) | O(min) |
| A − B | `cj.diferenca` | O(\|A\|) | O(\|A\|) |
| A Δ B | `cj.diferenca_simetrica` | O(\|A\| + \|B\|) | O(\|A\| + \|B\|) |
| A ⊆ B | `cj.eh_subconjunto` | O(\|A\|) | O(1) |
| A = ∅ | `cj.eh_vazio` | O(1) | O(1) |
| Disjuntos | `cj.sao_disjuntos` | O(min(\|A\|, \|B\|)) | O(1) |
| Filtrar por jurisdição/tipo | `ativos_da_jurisdicao` | O(n) | O(n) |
| Imagem R(x) | `cj.imagem` | O(\|R\|) | O(\|R\|) |
| Composição ingênua | `cj.composicao` | **O(\|R\| · \|S\|)** | O(saída) |
| Composição indexada | `cj.composicao_indexada` | **O(\|R\| + \|S\| + saída)** | O(\|S\| + saída) |
| É função? | `cj.eh_funcao` | O(\|R\| + \|X\|) | O(\|X\|) |
| Permissões do usuário | `permissoes_do_usuario` | O(r · q) ≈ O(1) | O(q) |
| Validar acesso | `tem_permissao` | O(r · q) ≈ O(1) | O(q) |
| Matriz de pertencimento | `matriz_jurisdicao_ativo` | O(k · n + n log n) | O(k · n) |
| Relatório | `relatorio` | O(k · n + n log n) | O(k · n) |
| Interseção com listas (comparação) | `intersecao_com_listas` | O(\|A\| · \|B\|) | O(\|A\|) |

**Por que O(1) "médio"?** Tabelas hash podem ter colisões. No pior caso
(todas as chaves no mesmo "balde") a busca vira O(n), mas o Python redimensiona a
tabela e usa boas funções de hash, então na prática o custo é constante.

## 2. Experimento prático

Script: `python -m src.utils.desempenho`
Dados: `src/data/gerador_inventario.py` (5 jurisdições, 5 tipos, 30% pendentes, 2% sem
jurisdição, semente 42). Cada tempo é o **menor** de várias repetições
(`time.perf_counter`). Memória medida com `tracemalloc`.

> Os números abaixo vieram de uma execução de referência. Rodem o script na máquina
> de vocês: os valores absolutos mudam, mas **o formato das curvas deve ser o mesmo**.

### 2.1 Operações lineares (n até 100 000)

| n | \|A\| | \|B\| | A ∪ B (ms) | A ∩ B (ms) | A − B (ms) | filtro (ms) | matriz (ms) | RBAC (ms) |
|---|---|---|---|---|---|---|---|---|
| 1 000 | 193 | 313 | 0.013 | 0.003 | 0.004 | 0.046 | 0.996 | 0.002 |
| 10 000 | 1 956 | 2 962 | 0.171 | 0.061 | 0.087 | 0.429 | 8.238 | 0.001 |
| 50 000 | 9 827 | 15 023 | 1.257 | 0.372 | 0.506 | 2.272 | 45.668 | 0.001 |
| 100 000 | 19 649 | 30 075 | 2.863 | 0.759 | 0.787 | 5.548 | 99.909 | 0.001 |

Leitura: multiplicar n por 10 (10 000 → 100 000) multiplica o tempo de ∩, − e do
filtro por ~10–13 → comportamento **linear**, como previsto. O RBAC fica constante
em ~1 µs → **O(1)**. Gráficos: `reports/figures/conjuntos.svg` e
`reports/figures/filtro_matriz.svg`.

### 2.2 Hash x lista e composição (efeito quadrático)

| n | ∩ com set (ms) | ∩ com lista (ms) | composição ingênua (ms) | composição indexada (ms) |
|---|---|---|---|---|
| 500 | 0.003 | 0.211 | 3.099 | 1.606 |
| 1 000 | 0.005 | 0.984 | 6.567 | 1.554 |
| 2 000 | 0.009 | 2.983 | 23.934 | 5.251 |
| 5 000 | 0.018 | 16.961 | 146.979 | 8.531 |

Leitura:

- O crescimento observado da interseção com lista é superlinear, compatível com
  **O(n²)**, enquanto o `set` mantém crescimento aproximadamente linear (**O(n)**).
  Em n = 5 000 o `set` foi ~900× mais rápido.
- A composição ingênua também apresenta crescimento quadrático. A versão indexada
  cresce aproximadamente de forma linear no tamanho da entrada + saída e foi ~17×
  mais rápida em n = 5 000.

Gráficos: `reports/figures/set_vs_lista.svg` e `reports/figures/composicao.svg`.

### 2.3 Memória

| n | pico (MB) | bytes por ativo |
|---|---|---|
| 1 000 | 0.30 | ~311 |
| 10 000 | 2.87 | ~301 |
| 50 000 | 15.22 | ~319 |
| 100 000 | 30.46 | ~319 |

Os bytes por ativo ficam praticamente constantes → memória **O(n)**.
Gráfico: `reports/figures/memoria.svg`.

## 3. Profiling (cProfile)

Arquivo: `reports/profiling/profile_cumulative.txt` (carga típica com n = 50 000).
Resumo e interpretação em `08_resultados.md`.

## 4. Conclusão

| Pergunta | Resposta |
|---|---|
| O que cresce linearmente? | Filtros, ∪, ∩, −, verificação de função, memória |
| O que é constante? | Busca por ID, RBAC |
| O que era quadrático? | Composição ingênua e interseção com listas |
| Como resolvemos? | Usando tabelas hash (`set`/`dict`) e um índice na composição |
| Gargalo real (cProfile) | Validações de mapeamento, ordenação e montagem da matriz |

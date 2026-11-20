# 07 — Testes (Sprint 5)

## Como rodar

Os testes baseados em classes podem ser executados apenas com Python:

```bash
python -m unittest discover -s tests -t . -v
```

Esse comando executa 30 testes. Para executar a suíte completa, que também
contém funções de teste, use **pytest**:

```bash
pip install pytest pytest-cov
pytest -v                                      # 56 testes
pytest --cov=src --cov-report=term-missing     # cobertura
```

## Organização

| Arquivo | O que testa | Nº de testes |
|---|---|---|
| `tests/test_models.py` | Entidades e validação de campos | 9 |
| `tests/test_algorithms.py` | Conjuntos, relações, composição, função, matriz | 18 |
| `tests/test_services.py` | Consultas, RBAC, composição no domínio, relatório | 17 |
| `tests/test_edge_cases.py` | Casos de borda do enunciado | 8 |
| `tests/test_data.py` | CSV, exportação, gerador sintético | 4 |
| **Total** | | **56** |

## Casos de teste exigidos pelo enunciado (A.10)

| # | Caso | Teste | Resultado esperado |
|---|---|---|---|
| 1 | Usuário inexistente | `test_edge_cases.test_usuario_inexistente` | `EntidadeInexistenteError` |
| 2 | Papel inexistente | `test_edge_cases.test_papel_inexistente` | `EntidadeInexistenteError` |
| 3 | Permissão inválida | `test_edge_cases.test_permissao_invalida` | `PermissaoInvalidaError` |
| 4 | Ativo sem jurisdição | `test_edge_cases.test_ativo_sem_jurisdicao` | A10 detectado; `AtivoSemJurisdicaoError` |
| 5 | Usuário com múltiplas permissões | `test_services.test_usuario_com_multiplas_permissoes` | Ana = Visitante ∪ Fiscal |
| 6 | Acesso autorizado | `test_services.test_acesso_autorizado` | `True` |
| 7 | Acesso negado | `test_services.test_acesso_negado`, `test_edge_cases.test_acesso_negado_lanca_erro` | `False` / `AcessoNegadoError`, nada apagado |
| 8 | Conjunto vazio | `test_algorithms.test_conjunto_vazio`, `test_edge_cases.test_conjunto_vazio` | `set()` |
| 9 | Conjuntos disjuntos | `test_algorithms.test_conjuntos_disjuntos`, `test_edge_cases.test_conjuntos_disjuntos` | Norte ∩ Sul = ∅ |
| 10 | Interseção | `test_algorithms.test_intersecao`, `test_services.test_consulta_do_enunciado` | {A2, A5} |
| 11 | União | `test_algorithms.test_uniao` | {A1, A2, A3, A5} |
| 12 | Diferença | `test_algorithms.test_diferenca` | {A1} e {A3} |

## Testes extras (além do enunciado)

- **Propriedades matemáticas**: A ∩ B ⊆ A ⊆ A ∪ B; (A − B) ∪ (A ∩ B) = A.
- **Composição**: a versão indexada dá o mesmo resultado que a ingênua.
- **Função**: `eh_funcao` detecta o ativo sem imagem; depois de associar, vira função.
- **Matriz**: cada ativo com jurisdição aparece em exatamente uma linha.
- **Duplicidade**: cadastrar A1 de novo → `EntidadeDuplicadaError`.
- **Jurisdição inexistente**: consultar "Leste" → erro.
- **Usuário sem papel**: conjunto de permissões = ∅.
- **Exclusão com permissão**: Maria exclui A1, e A1 some também do órgão.
- **CSV**: carregar os CSVs dá o mesmo resultado que os dados embutidos.
- **Gerador**: mesma semente → mesmos dados (experimento reproduzível).

## Resultado da última execução

```
Ran 56 tests in pytest
OK
```

## Definition of Done aplicada

Cada função nova só é considerada pronta quando: tem docstring, tem pelo menos um
teste, tem um caso de borda considerado e todos os testes passam.

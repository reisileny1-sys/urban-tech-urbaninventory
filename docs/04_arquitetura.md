# Arquitetura de Software

```
┌───────────────────────────────────────┐
│  INTERFACE — app.py (CLI/menu)        │
├───────────────────────────────────────┤
│  APLICAÇÃO — src/services/            │
│  InventoryService (RF01–RF11)         │
├───────────────────────────────────────┤
│  NÚCLEO MATEMÁTICO — src/algorithms/  │
│  set_operations, relations, rbac,     │
│  membership_matrix                    │
├───────────────────────────────────────┤
│  ESTRUTURAS — src/data/repository.py  │
│  dict, set, tuple, list aninhados     │
├───────────────────────────────────────┤
│  DADOS — data/, synthetic_data.py     │
└───────────────────────────────────────┘
```

## Módulos

| Pasta | Responsabilidade |
|-------|------------------|
| `src/models/` | Entidades: Ativo, Local, Órgão, Usuário, Papel, Permissão, Jurisdição |
| `src/algorithms/` | Núcleo matemático exclusivo |
| `src/services/` | Orquestração e validações |
| `src/data/` | Repositório em memória e dados sintéticos |
| `src/utils/` | Exceções e validadores |
| `tests/` | pytest |
| `reports/` | Complexidade, profiling, gráficos |

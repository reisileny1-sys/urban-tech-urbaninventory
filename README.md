# UrbanInventory

**Gestão Relacional do Patrimônio Público** - Squad 5, Plataforma UrbanTech.

Sistema para representar ativos públicos, jurisdições, relações e controle de acesso (RBAC) usando Teoria dos Conjuntos, relações binárias e estruturas dict/set.


## Estrutura

```
urban-tech-urbaninventory/
├── app.py                 # Interface CLI
├── src/
│   ├── models/            # Entidades de domínio
│   ├── algorithms/        # Núcleo matemático (conjuntos, RBAC, matriz)
│   ├── services/          # Casos de uso RF01–RF11
│   ├── data/              # Repositório e dados sintéticos
│   └── utils/             # Validações e exceções
├── tests/                 # pytest
├── docs/                  # Documentação do projeto
├── reports/               # Profiling e gráficos
└── data/                  # Datasets sintéticos
```

## Requisitos Funcionais

| RF | Descrição |
|----|-----------|
| RF01 | Cadastrar ativo |
| RF02 | Cadastrar localização |
| RF03 | Cadastrar usuário |
| RF04 | Cadastrar papel |
| RF05 | Cadastrar permissão |
| RF06 | Associar ativo à jurisdição |
| RF07 | Consultar ativos por conjunto (∩, ∪, −) |
| RF08 | Consultar relações |
| RF09 | Validar mapeamentos |
| RF10 | Validar acesso RBAC |
| RF11 | Produzir relatório |

## RBAC (Controle de Acesso Baseado em Papéis) 

```
João → Fiscal → [consultar, atualizar] → Ativos
Maria → Administrador → [consultar, criar, atualizar, excluir]
```


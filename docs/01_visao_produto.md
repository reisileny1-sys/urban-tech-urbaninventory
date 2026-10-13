# Visão do Produto — UrbanInventory

## Problema
Gestores públicos precisam controlar ativos urbanos (postes, semáforos, abrigos) distribuídos por jurisdições territoriais, com controle de acesso baseado em papéis (RBAC).

## Usuário
- Fiscais de campo
- Administradores de secretarias
- Gestores de patrimônio público

## Objetivo
Representar ativos, relacionamentos, jurisdições e permissões usando Teoria dos Conjuntos, relações binárias e RBAC.

## Entrada
- Cadastros de ativos, locais, usuários, papéis e permissões
- Associações ativo ↔ jurisdição
- Consultas por operações de conjuntos (∩, ∪, −)

## Processamento
1. Validação de dados
2. Armazenamento em dict/set aninhados
3. Operações de conjuntos e consulta de relações
4. Verificação RBAC

## Saída
- Conjuntos de ativos filtrados
- Matriz de pertencimento
- Relatórios consolidados
- Decisões de acesso (autorizado/negado)

## Valor Produzido
Consultas matemáticas precisas sobre o patrimônio público, com rastreabilidade e controle de acesso.

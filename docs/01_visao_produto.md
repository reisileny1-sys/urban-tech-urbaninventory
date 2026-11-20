# 01 — Visão do Produto (Sprint 0)

**Produto:** UrbanInventory — Gestão Relacional do Patrimônio Público
**Plataforma:** UrbanTech · Squad 5
**Núcleo matemático:** Teoria dos Conjuntos, Relações Binárias, Funções e RBAC

## Problema

Uma prefeitura tem milhares de bens públicos espalhados pela cidade (postes,
semáforos, abrigos de ônibus). Cada um fica numa região (jurisdição), é cuidado
por um órgão e pode precisar de manutenção. Muitas pessoas acessam essas
informações, mas nem todas podem fazer tudo: um fiscal pode consultar e atualizar,
mas não pode excluir um ativo.

Sem um modelo organizado, perguntas simples ficam difíceis de responder:

- Quais ativos da Zona Norte estão com manutenção pendente?
- Quais ativos estão sem jurisdição definida (cadastro incompleto)?
- Quais ativos este usuário administra, por meio do órgão dele?
- Este usuário tem permissão para excluir um ativo?

## Usuário

| Perfil | O que faz no sistema |
|---|---|
| Administrador (ex.: Maria) | Cadastra, consulta, atualiza e exclui |
| Fiscal (ex.: João) | Consulta e atualiza status de manutenção |
| Visitante | Apenas consulta |
| Gestor público | Lê relatórios e a matriz de pertencimento |

## Objetivo

Representar o patrimônio público como **conjuntos e relações** e usar operações
matemáticas (∪, ∩, −, composição, verificação de função) para responder às
consultas e controlar o acesso.

## Entrada

- Jurisdições, permissões, papéis, órgãos, locais, ativos e usuários
  (arquivos CSV em `data/raw/` ou cadastro pelo menu).
- Pedidos do usuário: uma consulta por conjuntos ou uma verificação de acesso.

## Processamento

1. Validação dos dados (campos vazios, IDs duplicados, referências inexistentes).
2. Construção dos conjuntos: ativos por jurisdição, pendentes, por tipo, por órgão.
3. Operações de conjuntos e relações (∪, ∩, −, Δ, ⊆, composição).
4. RBAC: permissões do usuário = ⋃ das permissões dos seus papéis.

## Saída

- Conjuntos resultantes das consultas (ex.: `A ∩ B = {A2, A5}`).
- Pares das relações (Usuário→Órgão, Órgão→Ativo...).
- Resposta de acesso: **autorizado** ou **negado**.
- Matriz de pertencimento Jurisdição × Ativo e relatório geral.

## Valor produzido

- Consultas que antes exigiam planilhas manuais viram **uma operação de conjuntos**.
- Erros de cadastro (ativo sem jurisdição) são detectados automaticamente,
  verificando se Ativo → Jurisdição é uma **função**.
- O acesso é controlado de forma auditável: dá para explicar *por que* alguém foi
  autorizado ou negado.

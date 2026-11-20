# 02 — Requisitos (Sprint 1)

## Requisitos funcionais

| Código | Descrição | Onde está no código | Opção do menu |
|---|---|---|---|
| RF01 | Cadastrar ativo | `Inventario.cadastrar_ativo` | 1 |
| RF02 | Cadastrar localização | `Inventario.cadastrar_local` | 2 |
| RF03 | Cadastrar usuário | `Inventario.cadastrar_usuario` | 3 |
| RF04 | Cadastrar papel | `Inventario.cadastrar_papel` | 4 |
| RF05 | Cadastrar permissão | `Inventario.cadastrar_permissao` | 5 |
| RF06 | Associar ativo à jurisdição | `Inventario.associar_ativo_jurisdicao` | 11 |
| RF07 | Consultar ativos por conjunto | `consulta_norte_pendente`, `ativos_da_jurisdicao`... + `algorithms/conjuntos.py` | 6, 7 |
| RF08 | Consultar relações | `relacao_usuario_orgao`, `relacao_orgao_ativo`, `relacao_usuario_papel`, `relacao_papel_permissao`, `ativos_que_usuario_gerencia` | 8 |
| RF09 | Validar mapeamentos | `validar_mapeamento_ativo_jurisdicao`, `exigir_jurisdicao`, `cj.eh_funcao` | 10 |
| RF10 | Validar acesso | `tem_permissao`, `exigir_permissao`, `permissoes_do_usuario` | 9 |
| RF11 | Produzir relatório | `Inventario.relatorio`, `exportar_ativos_csv` | 10, 12, 13 |

## Requisitos não funcionais

| Código | Descrição |
|---|---|
| RNF01 | Somente Python e biblioteca padrão (sem frameworks web, sem banco de dados) |
| RNF02 | Arquitetura em camadas: interface, aplicação, núcleo matemático, estruturas, dados |
| RNF03 | Busca por ID em O(1) médio (tabelas hash / `dict`) |
| RNF04 | Mensagens de erro claras para dados inválidos (exceções próprias) |
| RNF05 | Testes automatizados para todos os casos do enunciado |
| RNF06 | Toda função pública com docstring |
| RNF07 | Dados de exemplo reproduzíveis (CSV e gerador com semente fixa) |

## Casos de uso

**UC01 — Consultar ativos por conjuntos**
Ator: Fiscal. Fluxo: escolhe o conjunto A (ex.: Zona Norte) e o conjunto B
(ex.: pendentes) → o sistema mostra A ∪ B, A ∩ B, A − B, B − A, A Δ B, se A é vazio,
se A e B são disjuntos e se A ⊆ B.
Exceção: jurisdição inexistente → mensagem de erro.

**UC02 — Validar acesso**
Ator: qualquer usuário. Fluxo: informa ID do usuário e a ação → o sistema calcula a
união das permissões dos papéis do usuário → responde AUTORIZADO ou NEGADO.
Exceções: usuário inexistente; permissão inválida.

**UC03 — Excluir ativo**
Ator: Administrador. Pré-condição: ter a permissão `excluir`. Fluxo: o sistema
verifica o RBAC e remove o ativo e suas associações com órgãos.
Exceção: Fiscal tenta excluir → `AcessoNegadoError`, nada é apagado.

**UC04 — Corrigir ativo sem jurisdição**
Ator: Administrador. Fluxo: o relatório mostra que Ativo → Jurisdição **não é
função** (A10 sem imagem) → associa A10 a uma jurisdição → o relatório passa a
indicar que é função.

**UC05 — Gerar relatório e matriz**
Ator: Gestor. Fluxo: pede o relatório → o sistema mostra totais, ativos e pendentes
por jurisdição, ativos sem jurisdição, validação do mapeamento e a matriz.

## Histórias de usuário (backlog por épico)

| Épico | História | Status |
|---|---|---|
| 1 Modelagem | Como desenvolvedor, quero representar ativos e jurisdições como conjuntos | Feito |
| 2 Estruturas | Como sistema, quero guardar as entidades em `dict` para buscar por ID em O(1) | Feito |
| 3 Núcleo | Como fiscal, quero ver A ∩ B para saber o que consertar na minha zona | Feito |
| 3 Núcleo | Como gestor, quero ver a matriz de pertencimento | Feito |
| 4 Validação | Como usuário, quero mensagens claras quando um ID não existe | Feito |
| 4 Validação | Como administrador, quero que um fiscal não consiga excluir ativos | Feito |
| 5 Desempenho | Como desenvolvedor, quero medir tempo e memória ao aumentar n | Feito |
| 6 Qualidade | Como equipe, quero testes que quebrem se alguém estragar uma regra | Feito |

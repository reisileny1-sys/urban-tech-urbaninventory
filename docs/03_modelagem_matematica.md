# Modelagem Matemática — UrbanInventory

## 1. Introdução

O UrbanInventory é um sistema de gestão relacional do patrimônio público, desenvolvido para organizar ativos, jurisdições, órgãos, usuários e permissões de acesso.

A modelagem matemática utiliza conceitos de Matemática Discreta para representar os dados e os relacionamentos existentes no sistema. Os principais conceitos utilizados são teoria dos conjuntos, relações binárias, funções, mapeamentos e matrizes de pertencimento.

Esses conceitos permitem realizar consultas, identificar associações entre entidades, verificar a consistência dos dados e apoiar o controle de acesso baseado em papéis (RBAC).

## 2. Definição dos conjuntos

Os elementos do UrbanInventory podem ser representados por conjuntos matemáticos.

Considere os seguintes conjuntos:

- **A:** conjunto de todos os ativos públicos cadastrados.
- **J:** conjunto das jurisdições.
- **U:** conjunto dos usuários.
- **O:** conjunto dos órgãos.
- **R:** conjunto dos papéis.
- **P:** conjunto das permissões.

Por exemplo:

```text
A = {A1, A2, A3, A4}
J = {Norte, Sul, Centro}
U = {U1, U2}
O = {O1, O2}
R = {Fiscal, Administrador}
P = {consultar, criar, atualizar, excluir}
```

Cada conjunto reúne elementos de uma mesma categoria, facilitando sua organização e manipulação.

## 3. Operações com conjuntos

As operações com conjuntos são utilizadas para consultar e comparar grupos de ativos públicos.

Considere:

```text
A = {A1, A2, A3}
B = {A2, A3, A4}
```

Neste exemplo, A representa os ativos da Zona Norte e B representa os ativos com manutenção pendente.

### 3.1 União

A união reúne todos os elementos presentes em pelo menos um dos conjuntos, sem repetições.

**A ∪ B = {A1, A2, A3, A4}**

No UrbanInventory, essa operação permite reunir ativos de diferentes categorias.

### 3.2 Interseção

A interseção identifica os elementos que pertencem simultaneamente aos dois conjuntos.

**A ∩ B = {A2, A3}**

Nesse caso, representa os ativos da Zona Norte que estão com manutenção pendente.

### 3.3 Diferença

A diferença identifica os elementos presentes em um conjunto, mas ausentes no outro.

**A − B = {A1}**

Representa os ativos da Zona Norte que não estão com manutenção pendente.

### 3.4 Diferença simétrica

A diferença simétrica reúne os elementos que pertencem a apenas um dos conjuntos.

**A Δ B = {A1, A4}**

Essa operação permite identificar ativos que não são comuns aos dois grupos.

### 3.5 Subconjuntos e conjuntos disjuntos

Um conjunto A é subconjunto de B quando todos os seus elementos também pertencem a B.

**A ⊆ B**

Dois conjuntos são disjuntos quando não possuem elementos em comum.

**A ∩ B = ∅**

Essas verificações auxiliam na análise das relações entre grupos de ativos.

## 4. Relações binárias

Uma relação binária representa associações entre elementos de dois conjuntos.

No UrbanInventory, as principais relações são:

- Usuário → Órgão
- Órgão → Ativo
- Usuário → Papel
- Papel → Permissão
- Ativo → Jurisdição

As relações são representadas por pares ordenados.

Por exemplo:

```text
R1 = {(U1, O1), (U2, O2)}
R2 = {(O1, A1), (O1, A2), (O2, A3)}
```

A primeira relação indica a qual órgão cada usuário pertence.

A segunda indica quais ativos são administrados por cada órgão.

### 4.1 Composição de relações

A composição permite combinar duas relações para descobrir uma associação indireta.

Se:

```text
U1 → O1
O1 → A1
O1 → A2
```

Então, pela composição das relações:

```text
U1 → A1
U1 → A2
```

Dessa forma, o sistema consegue identificar os ativos gerenciados por um usuário a partir do órgão ao qual ele pertence.

## 5. Funções e mapeamentos

Uma função matemática associa cada elemento de um domínio a exatamente um elemento do contradomínio.

No UrbanInventory, podemos representar a associação entre ativos e jurisdições por:

**f: A → J**

Em que:

- A é o conjunto de ativos.
- J é o conjunto de jurisdições.
- f associa cada ativo à sua jurisdição.

Exemplo:

```text
f(A1) = Norte
f(A2) = Norte
f(A3) = Sul
```

Para que o mapeamento seja considerado uma função total de A para J, cada ativo deve possuir exatamente uma jurisdição válida.

Um ativo sem jurisdição torna esse mapeamento incompleto. Por isso, a validação matemática identifica ativos que ainda não possuem uma associação definida.

O sistema pode permitir o cadastro temporário de ativos sem jurisdição, mas esses ativos devem ser identificados durante a validação.

## 6. Modelagem matemática do RBAC

O RBAC (Role-Based Access Control) é um modelo de controle de acesso baseado em papéis.

Nesse modelo, os usuários recebem papéis, e cada papel possui um conjunto de permissões.

A estrutura pode ser representada por:

```text
Usuário → Papel → Permissão
```

Considere:

```text
Fiscal = {consultar, atualizar}

Administrador = {consultar, criar, atualizar, excluir}
```

Se um usuário possuir os papéis Fiscal e Administrador, suas permissões efetivas serão obtidas pela união:

```text
Permissões(U1) = Fiscal ∪ Administrador
```

Resultado:

```text
{consultar, criar, atualizar, excluir}
```

Matematicamente, podemos definir duas relações:

- **UR ⊆ U × R:** associa usuários aos seus papéis.
- **RP ⊆ R × P:** associa papéis às suas permissões.

A composição dessas relações permite determinar quais permissões estão associadas a cada usuário.

Uma ação é autorizada quando a permissão correspondente pertence ao conjunto de permissões efetivas do usuário.

Essa modelagem fornece a base matemática utilizada pelas regras de autorização implementadas na camada de serviços do UrbanInventory.

## 7. Matriz de pertencimento

A matriz de pertencimento representa a associação entre jurisdições e ativos públicos.

Cada linha representa uma jurisdição, e cada coluna representa um ativo.

Os valores são binários:

- **1:** o ativo pertence à jurisdição.
- **0:** o ativo não pertence à jurisdição.

Exemplo:

| Jurisdição | A1 | A2 | A3 |
|---|---|---|---|
| Norte | 1 | 1 | 0 |
| Sul | 0 | 0 | 1 |
| Centro | 0 | 0 | 0 |

A matriz correspondente é:

```text
M = [
    [1, 1, 0],
    [0, 0, 1],
    [0, 0, 0]
]
```

Formalmente, cada elemento da matriz pode ser definido por:

**M[i][j] = 1**, se o ativo da coluna j pertence à jurisdição da linha i.

**M[i][j] = 0**, caso contrário.

A matriz permite visualizar a distribuição dos ativos e identificar aqueles que não estão associados a nenhuma jurisdição.

Em um mapeamento válido, cada coluna correspondente a um ativo deve possuir exatamente um valor igual a 1.

## 8. Estruturas de dados utilizadas

A implementação matemática utiliza estruturas de dados da linguagem Python.

| Estrutura | Aplicação |
|---|---|
| `set` | Representação de conjuntos e operações matemáticas |
| `tuple` | Representação de pares ordenados nas relações |
| `dict` | Mapeamento de ativos, jurisdições e outras associações |
| `list` | Representação das linhas e colunas da matriz |
| Estruturas aninhadas | Organização de associações e dados relacionados |

Essas estruturas permitem representar os conceitos matemáticos de maneira organizada e realizar operações sobre os dados.

## 9. Aplicação da modelagem no UrbanInventory

Os conceitos matemáticos apresentados são utilizados no núcleo algorítmico do projeto, localizado em `src/algorithms/`.

Os arquivos relacionados são:

- `nucleo_mat.py`: contém operações básicas com conjuntos, relações, mapeamentos e matriz de pertencimento.
- `conjuntos.py`: reúne as operações utilizadas na integração com a aplicação, incluindo operações adicionais de conjuntos, composição de relações, validação de funções e formatação da matriz.

A camada de serviços utiliza essas operações para apoiar consultas, relacionamentos, validações e regras de controle de acesso.

A implementação detalhada dos algoritmos é apresentada no documento `05_algoritmos.md`.

## 10. Considerações finais

A modelagem matemática do UrbanInventory demonstra como os conceitos de Matemática Discreta podem ser aplicados à organização e à consulta de informações sobre o patrimônio público.

A teoria dos conjuntos permite comparar grupos de ativos, as relações binárias representam associações entre entidades, as funções validam os mapeamentos, o RBAC utiliza relações e conjuntos de permissões, e a matriz de pertencimento representa a distribuição dos ativos entre jurisdições.

Dessa forma, a matemática fornece uma base lógica para o funcionamento e a validação das operações do sistema.
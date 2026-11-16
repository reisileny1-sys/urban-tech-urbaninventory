# Algoritmos — UrbanInventory

## 1. Introdução

O núcleo matemático do UrbanInventory é responsável pelas operações de Matemática Discreta utilizadas na gestão relacional de ativos públicos.

Os algoritmos foram desenvolvidos em Python e permitem realizar operações com conjuntos, consultar e compor relações binárias, validar mapeamentos, representar matrizes de pertencimento e apoiar o controle de acesso baseado em papéis (RBAC).

A implementação está organizada principalmente em dois arquivos:

- `src/algorithms/nucleo_mat.py`: operações matemáticas básicas.
- `src/algorithms/conjuntos.py`: operações adicionais e integração com os serviços do sistema.

O objetivo dessa separação é reaproveitar as funções já desenvolvidas e disponibilizar as operações necessárias para a aplicação.

## 2. Operações com conjuntos

As operações com conjuntos são utilizadas para consultar e comparar grupos de ativos públicos.

### 2.1 União

**Função:** `uniao(conjunto_a, conjunto_b)`

**Objetivo:** reunir todos os elementos presentes em pelo menos um dos conjuntos, sem repetições.

**Implementação:**

```python
def uniao(conjunto_a, conjunto_b):
    return conjunto_a | conjunto_b
```

**Exemplo:**

```python
a = {"A1", "A2"}
b = {"A2", "A3"}

resultado = uniao(a, b)
# {"A1", "A2", "A3"}
```

A operação utiliza o operador `|` do Python.

### 2.2 Interseção

**Função:** `intersecao(conjunto_a, conjunto_b)`

**Objetivo:** identificar os elementos comuns aos dois conjuntos.

```python
def intersecao(conjunto_a, conjunto_b):
    return conjunto_a & conjunto_b
```

**Exemplo:**

```python
a = {"A1", "A2"}
b = {"A2", "A3"}

resultado = intersecao(a, b)
# {"A2"}
```

Essa operação permite identificar, por exemplo, ativos de determinada jurisdição que também possuem manutenção pendente.

### 2.3 Diferença

**Função:** `diferenca(conjunto_a, conjunto_b)`

**Objetivo:** retornar os elementos presentes no primeiro conjunto e ausentes no segundo.

```python
def diferenca(conjunto_a, conjunto_b):
    return conjunto_a - conjunto_b
```

**Exemplo:**

```python
a = {"A1", "A2"}
b = {"A2", "A3"}

resultado = diferenca(a, b)
# {"A1"}
```

### 2.4 Diferença simétrica

**Função:** `diferenca_simetrica(a, b)`

**Objetivo:** identificar os elementos que pertencem exclusivamente a um dos conjuntos.

```python
def diferenca_simetrica(a, b):
    return a ^ b
```

**Exemplo:**

```python
a = {"A1", "A2"}
b = {"A2", "A3"}

resultado = diferenca_simetrica(a, b)
# {"A1", "A3"}
```

### 2.5 Verificação de conjunto vazio

**Função:** `eh_vazio(conjunto)`

**Objetivo:** verificar se um conjunto não possui elementos.

```python
def eh_vazio(conjunto):
    return len(conjunto) == 0
```

A função retorna `True` quando o conjunto está vazio e `False` caso contrário.

### 2.6 Verificação de conjuntos disjuntos

**Função:** `sao_disjuntos(a, b)`

**Objetivo:** verificar se dois conjuntos não possuem elementos em comum.

```python
def sao_disjuntos(a, b):
    return a.isdisjoint(b)
```

O método `isdisjoint()` retorna um valor booleano.

### 2.7 Verificação de subconjuntos

**Função:** `eh_subconjunto(a, b)`

**Objetivo:** verificar se todos os elementos de A pertencem a B.

```python
def eh_subconjunto(a, b):
    return a.issubset(b)
```

Essa operação pode ser utilizada para verificar relações de inclusão entre grupos de ativos.

## 3. Relações binárias

As relações binárias representam associações entre elementos, utilizando pares ordenados.

### 3.1 Criação de relações

**Função:** `criar_relacao(elemento_a, elemento_b)`

```python
def criar_relacao(elemento_a, elemento_b):
    return (elemento_a, elemento_b)
```

A função recebe dois elementos e retorna uma tupla.

**Exemplo:**

```python
criar_relacao("O1", "A1")
# ("O1", "A1")
```

### 3.2 Consulta de relações

**Funções:** `consultar_relacoes()` e `imagem()`

Essas funções permitem consultar os elementos relacionados a uma origem.

```python
def imagem(relacao, elemento):
    return {
        destino
        for origem, destino in relacao
        if origem == elemento
    }
```

**Exemplo:**

```python
relacao = {
    ("O1", "A1"),
    ("O1", "A2"),
    ("O2", "A3")
}

resultado = imagem(relacao, "O1")
# {"A1", "A2"}
```

A função `consultar_relacoes()` do núcleo básico realiza uma consulta equivalente utilizando um laço `for`.

### 3.3 Composição indexada de relações

**Função:** `composicao_indexada(relacao_a, relacao_b)`

**Objetivo:** combinar duas relações binárias para identificar associações indiretas.

O algoritmo cria inicialmente um índice da segunda relação. Depois, percorre a primeira relação e procura os elementos correspondentes nesse índice.

**Exemplo:**

```python
relacao_a = {("U1", "O1")}
relacao_b = {
    ("O1", "A1"),
    ("O1", "A2")
}

resultado = composicao_indexada(relacao_a, relacao_b)

# {("U1", "A1"), ("U1", "A2")}
```

No UrbanInventory, essa operação permite identificar quais ativos um usuário gerencia por meio do órgão ao qual pertence.

O uso de um índice evita percorrer toda a segunda relação para cada elemento da primeira.

## 4. Funções e mapeamentos

Os mapeamentos são utilizados para associar ativos às suas respectivas jurisdições.

### 4.1 Consulta de jurisdição

**Função:** `consultar_jurisdicao(mapeamento, ativo)`

```python
def consultar_jurisdicao(mapeamento, ativo):
    return mapeamento.get(ativo)
```

**Exemplo:**

```python
mapeamento = {"A1": "Norte"}

resultado = consultar_jurisdicao(mapeamento, "A1")
# "Norte"
```

Se o ativo não existir no dicionário, a função retorna `None`.

### 4.2 Validação de mapeamento

**Função:** `validar_mapeamento(mapeamento, ativos, jurisdicoes)`

**Objetivo:** verificar se todos os ativos informados possuem uma jurisdição pertencente ao conjunto de jurisdições válidas.

O algoritmo percorre os ativos e verifica se cada um está presente no mapeamento e se sua jurisdição é permitida.

Retorna `True` quando todas as verificações são satisfeitas e `False` quando encontra alguma inconsistência.

### 4.3 Verificação de função matemática

**Função:** `eh_funcao(relacao, dominio)`

**Objetivo:** verificar se cada elemento do domínio possui exatamente uma imagem.

O algoritmo organiza as imagens de cada elemento e identifica:

- Elementos do domínio sem imagem.
- Elementos do domínio com mais de uma imagem.
- Origens presentes na relação que não pertencem ao domínio informado.

**Exemplo:**

```python
relacao = {("A1", "Norte")}
dominio = {"A1", "A2"}

resultado = eh_funcao(relacao, dominio)

# (False, {"A2"})
```

A função retorna uma tupla contendo um valor booleano e um conjunto com os elementos problemáticos.

No exemplo, o resultado é `False` porque o ativo A2 não possui jurisdição associada.

## 5. Matriz de pertencimento

A matriz de pertencimento representa a relação entre jurisdições e ativos públicos utilizando valores binários.

### 5.1 Construção da matriz

**Função:** `matriz_pertencimento()`

No módulo `conjuntos.py`, a função recebe:

- `conjuntos`: dicionário que associa cada jurisdição ao conjunto de seus ativos.
- `colunas`: lista ordenada dos ativos que serão representados.

**Exemplo:**

```python
conjuntos = {
    "Norte": {"A1", "A2"},
    "Sul": {"A3"}
}

colunas = ["A1", "A2", "A3"]

resultado = matriz_pertencimento(conjuntos, colunas)
```

**Retorno:**

```python
(
    ["Norte", "Sul"],
    ["A1", "A2", "A3"],
    [
        [1, 1, 0],
        [0, 0, 1]
    ]
)
```

Cada valor igual a `1` indica que o ativo pertence à jurisdição correspondente.

O valor `0` indica ausência dessa associação.

O arquivo `nucleo_mat.py` também possui uma implementação de matriz que recebe os ativos, as jurisdições e o mapeamento diretamente.

### 5.2 Formatação da matriz

**Função:** `formatar_matriz(linhas, colunas, matriz)`

**Objetivo:** transformar a matriz em uma representação textual organizada para exibição no terminal.

A função recebe os nomes das linhas, os identificadores das colunas e os valores binários, retornando uma string formatada.

Essa operação é utilizada na apresentação da matriz pelo sistema.

## 6. Aplicação matemática ao RBAC

O controle de acesso baseado em papéis utiliza operações matemáticas para determinar as permissões associadas a cada usuário.

Cada papel possui um conjunto de permissões.

Quando um usuário possui vários papéis, suas permissões efetivas podem ser obtidas pela união dos conjuntos de permissões.

**Exemplo:**

```python
fiscal = {"consultar", "atualizar"}
administrador = {
    "consultar",
    "criar",
    "atualizar",
    "excluir"
}

permissoes = uniao(fiscal, administrador)
```

**Resultado:**

```python
{"consultar", "criar", "atualizar", "excluir"}
```

O núcleo matemático também permite identificar permissões inválidas utilizando a diferença entre conjuntos.

A atribuição de papéis e a decisão de autorizar ou negar uma ação são responsabilidades da camada de serviços, que utiliza as operações disponibilizadas pelo núcleo matemático.

## 7. Estruturas de dados

Os algoritmos utilizam estruturas nativas do Python para representar os conceitos matemáticos.

| Estrutura | Utilização |
|---|---|
| `set` | Conjuntos de ativos, permissões e resultados de relações |
| `tuple` | Pares ordenados e retornos com múltiplos valores |
| `dict` | Índices, mapeamentos e associações |
| `list` | Linhas, colunas e valores da matriz |

Essas estruturas facilitam a implementação das operações e a organização dos dados utilizados pelo sistema.

## 8. Testes e validação

O núcleo matemático possui testes automatizados desenvolvidos com `pytest`.

Os testes iniciais verificam operações de conjuntos, relações, consultas de jurisdição, validação de mapeamentos e construção da matriz.

Também foram desenvolvidos testes de casos de borda, incluindo situações como conjuntos vazios, relações inexistentes e mapeamentos incompletos ou inválidos.

Os testes do núcleo básico e dos casos de borda foram executados durante o desenvolvimento.

As funções adicionais de integração também passaram por verificações manuais, mas ainda precisam de cobertura automatizada específica e de validação completa com os demais módulos do UrbanInventory.

## 9. Organização dos arquivos

Os algoritmos estão distribuídos nos seguintes módulos:

```text
src/
└── algorithms/
    ├── __init__.py
    ├── nucleo_mat.py
    └── conjuntos.py
```

O arquivo `nucleo_mat.py` contém as operações matemáticas iniciais.

O arquivo `conjuntos.py` reutiliza algumas dessas funções e disponibiliza outras operações necessárias para a integração com o sistema.

Essa organização permite manter as operações matemáticas separadas das regras de negócio e das funcionalidades de cadastro e armazenamento de dados.

## 10. Considerações finais

Os algoritmos desenvolvidos para o UrbanInventory aplicam conceitos de Matemática Discreta à gestão de ativos públicos.

As operações com conjuntos permitem realizar consultas e comparações, as relações binárias representam associações entre entidades, as funções validam mapeamentos, e as matrizes organizam visualmente a distribuição dos ativos.

Além disso, essas operações fornecem suporte matemático ao modelo RBAC.

A integração completa dos algoritmos com os demais componentes do sistema deverá ser verificada após a conclusão e a revisão dos módulos desenvolvidos pela equipe.
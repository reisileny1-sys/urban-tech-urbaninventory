# 05 — Algoritmos do UrbanInventory

## 1. Introdução

Nesta parte do projeto, desenvolvemos as funções matemáticas usadas pelo UrbanInventory. A ideia é ajudar na organização dos patrimônios públicos, usando os conteúdos de Matemática Discreta que estudamos, como conjuntos, relações binárias, funções e matrizes.

Os algoritmos foram feitos em Python e estão principalmente no arquivo `src/algorithms/nucleo_mat.py`. Eles não fazem o cadastro dos patrimônios e nem controlam o sistema inteiro. O papel deles é realizar as operações matemáticas que podem ser utilizadas pelos outros módulos.

Também existe o arquivo `src/algorithms/conjuntos.py`, que reúne algumas operações semelhantes. Neste documento, usamos como referência as funções do `nucleo_mat.py`, que também é o módulo importado pelo serviço de inventário.

## 2. Operações com conjuntos

Usamos o tipo `set` do Python para trabalhar com conjuntos. Ele é útil porque não armazena elementos repetidos. No projeto, podemos usar conjuntos para representar grupos de ativos, jurisdições ou permissões.

### 2.1 União

A função `uniao(conjunto_a, conjunto_b)` junta os elementos dos dois conjuntos, sem repetir os que aparecem em ambos. No Python, usamos o operador `|`.

```python
a = {"A1", "A2"}
b = {"A2", "A3"}

uniao(a, b)
# Resultado: {"A1", "A2", "A3"}
```

Isso pode ser útil, por exemplo, para reunir os ativos de dois grupos diferentes.

### 2.2 Interseção

A função `intersecao(conjunto_a, conjunto_b)` retorna apenas os elementos que estão nos dois conjuntos. Para isso, usamos `&`.

```python
intersecao(a, b)
# Resultado: {"A2"}
```

Com essa operação, podemos encontrar os ativos que aparecem em duas listas ao mesmo tempo.

### 2.3 Diferença

A função `diferenca(conjunto_a, conjunto_b)` mostra os elementos que estão no primeiro conjunto, mas não estão no segundo. O operador usado é `-`.

```python
diferenca(a, b)
# Resultado: {"A1"}
```

### 2.4 Diferença simétrica

A função `diferenca_simetrica(conjunto_a, conjunto_b)` retorna os elementos que aparecem em apenas um dos conjuntos. Os elementos que aparecem nos dois ficam de fora. Usamos o operador `^`.

```python
diferenca_simetrica(a, b)
# Resultado: {"A1", "A3"}
```

### 2.5 Conjunto vazio, conjuntos disjuntos e subconjunto

Criamos também três funções para fazer verificações simples:

- `eh_vazio(conjunto)`: retorna `True` quando o conjunto não possui elementos.
- `sao_disjuntos(conjunto_a, conjunto_b)`: retorna `True` quando os dois conjuntos não têm elementos em comum.
- `eh_subconjunto(conjunto_a, conjunto_b)`: retorna `True` quando todos os elementos de A também estão em B.

```python
eh_vazio(set())                      # True
sao_disjuntos({"A1"}, {"A2"})        # True
eh_subconjunto({"A1"}, {"A1", "A2"})  # True
```

Na implementação, usamos `not conjunto`, o método `isdisjoint()` e o operador `<=`, respectivamente.

## 3. Relações binárias

As relações binárias são usadas para representar ligações entre dois elementos. Por exemplo, podemos relacionar um usuário a um órgão ou um órgão a um patrimônio.

No código, cada relação é um par ordenado, representado por uma tupla. Um conjunto de tuplas pode guardar várias associações.

### 3.1 Criar e consultar relações

A função `criar_relacao(elemento_a, elemento_b)` recebe dois valores e devolve uma tupla com esses elementos.

Já `consultar_relacoes(relacoes, elemento)` procura os pares que começam com o elemento informado e retorna seus destinos.

```python
relacoes = {
    criar_relacao("O1", "A1"),
    criar_relacao("O1", "A2"),
    criar_relacao("O2", "A3")
}

consultar_relacoes(relacoes, "O1")
# Resultado: {"A1", "A2"}
```

A função `imagem(relacao, elemento)` faz uma consulta semelhante. Ela retorna o conjunto de destinos relacionados a uma determinada origem. Caso não encontre nenhum, retorna um conjunto vazio.

```python
imagem(relacoes, "O2")  # {"A3"}
imagem(relacoes, "O3")  # set()
```

### 3.2 Composição de relações

A função `composicao_indexada(relacao_ab, relacao_bc)` combina duas relações para encontrar uma ligação indireta.

Um exemplo é quando sabemos a qual órgão cada usuário pertence e quais ativos estão ligados a cada órgão. Com a composição, podemos encontrar os ativos associados a cada usuário por meio do órgão.

```python
usuario_orgao = {
    ("U1", "O1"),
    ("U2", "O2")
}

orgao_ativo = {
    ("O1", "A1"),
    ("O1", "A2"),
    ("O2", "A3")
}

composicao_indexada(usuario_orgao, orgao_ativo)
# Resultado: {("U1", "A1"), ("U1", "A2"), ("U2", "A3")}
```

Para realizar essa operação, primeiro organizamos a segunda relação em um dicionário. Depois, percorremos a primeira relação e consultamos os elementos correspondentes nesse dicionário.

Assim, não precisamos comparar cada par da primeira relação com todos os pares da segunda. Essa organização utiliza o funcionamento das tabelas hash dos dicionários do Python.

## 4. Funções e mapeamentos

Nesta parte, usamos os conceitos de funções matemáticas para trabalhar com as jurisdições dos ativos. A ideia é que cada ativo tenha uma jurisdição válida associada a ele.

### 4.1 Consulta de jurisdição

A função `consultar_jurisdicao(mapeamento, ativo)` procura a jurisdição de um ativo em um dicionário.

```python
mapeamento = {
    "A1": "Norte",
    "A2": "Sul"
}

consultar_jurisdicao(mapeamento, "A1")
# Resultado: "Norte"
```

Se o ativo não estiver no dicionário, a função retorna `None`.

### 4.2 Validação do mapeamento

A função `validar_mapeamento(mapeamento, ativos, jurisdicoes)` verifica se cada ativo informado aparece no dicionário e se sua jurisdição está entre as permitidas.

```python
ativos = {"A1", "A2"}
jurisdicoes = {"Norte", "Sul"}

validar_mapeamento(mapeamento, ativos, jurisdicoes)
# Resultado: True
```

Se algum dos ativos não possuir jurisdição ou estiver associado a uma jurisdição inválida, o resultado será `False`.

É importante observar que essa função verifica os ativos recebidos como parâmetro. Ela não foi feita para identificar chaves extras no dicionário.

### 4.3 Verificação de função matemática

A função `eh_funcao(relacao, dominio)` verifica se cada elemento do domínio tem exatamente uma imagem na relação.

Ela identifica três situações: um elemento sem imagem, um elemento com mais de uma imagem e uma origem que aparece na relação, mas não pertence ao domínio informado.

```python
relacao = {("A1", "Norte")}
dominio = {"A1", "A2"}

eh_funcao(relacao, dominio)
# Resultado: (False, {"A2"})
```

Nesse exemplo, a relação não atende à condição porque o ativo `A2` ficou sem jurisdição.

O retorno tem duas partes: um valor `True` ou `False` e um conjunto com os elementos que apresentaram problemas. Quando está tudo certo, o retorno é `(True, set())`.

A verificação da existência da jurisdição entre os valores permitidos é feita separadamente, porque `eh_funcao()` não recebe a lista de jurisdições válidas.

## 5. Matriz de pertencimento

A matriz de pertencimento ajuda a visualizar quais ativos pertencem a cada jurisdição. Ela utiliza apenas os valores `0` e `1`:

- `1` significa que o ativo pertence àquela jurisdição.
- `0` significa que não pertence.

### 5.1 Construção da matriz

A função `matriz_pertencimento(conjuntos, colunas)` recebe um dicionário com as jurisdições e seus ativos e uma lista com os ativos que serão apresentados nas colunas.

```python
conjuntos = {
    "Norte": {"A1", "A2"},
    "Sul": {"A3"}
}

colunas = ["A1", "A2", "A3"]

linhas, ativos, matriz = matriz_pertencimento(conjuntos, colunas)

# linhas = ["Norte", "Sul"]
# ativos = ["A1", "A2", "A3"]
# matriz = [[1, 1, 0], [0, 0, 1]]
```

Cada linha representa uma jurisdição e cada coluna representa um ativo. A função retorna as linhas, as colunas e a matriz de valores.

A matriz mostra as associações que foram informadas. Ela não verifica sozinha se um ativo foi colocado em mais de uma jurisdição.

### 5.2 Formatação da matriz

A função `formatar_matriz(linhas, colunas, matriz)` transforma esses dados em um texto para ser exibido no terminal ou no relatório.

```python
print(formatar_matriz(linhas, ativos, matriz))
```

O resultado apresenta os nomes das jurisdições e os valores `0` e `1` de cada ativo. Quando linhas e colunas estão vazias, a função retorna `"Matriz vazia"`.

## 6. Uso dos algoritmos no controle de acesso (RBAC)

O RBAC é uma forma de organizar as permissões dos usuários conforme os papéis que eles possuem no sistema.

Os conceitos de conjuntos e relações ajudam nessa parte. Podemos representar a ligação entre usuários e papéis, e também entre papéis e permissões. Se um usuário tiver mais de um papel, a união dos conjuntos permite reunir as permissões desses papéis.

```python
fiscal = {"consultar", "atualizar"}
administrador = {"consultar", "criar", "atualizar", "excluir"}

uniao(fiscal, administrador)
# Resultado: {"consultar", "criar", "atualizar", "excluir"}
```

Essas operações servem como apoio matemático. A decisão de permitir ou negar uma ação ao usuário é uma responsabilidade da parte de serviços do sistema, e não dessas funções isoladamente.

## 7. Estruturas de dados utilizadas

Para desenvolver os algoritmos, utilizamos estruturas do próprio Python:

| Estrutura | Como foi utilizada |
| --- | --- |
| `set` | Para guardar conjuntos de ativos, permissões e resultados sem repetição. |
| `tuple` | Para representar os pares ordenados das relações. |
| `dict` | Para associar ativos a jurisdições e criar o índice na composição de relações. |
| `list` | Para organizar as linhas, as colunas e os valores da matriz. |

Na composição de relações e na verificação de funções, também usamos dicionários que guardam conjuntos como valores. Isso facilita a consulta dos elementos relacionados a uma mesma origem.

## 8. Testes dos algoritmos

Para verificar o funcionamento das funções, utilizamos testes automatizados com `pytest`. Os testes estão organizados na pasta `tests/`, incluindo o arquivo `test_algorithms.py`.

Testamos as operações com conjuntos, a criação e a consulta de relações, a validação de mapeamentos e a construção da matriz de pertencimento. Também acrescentamos testes para `eh_funcao()`, `composicao_indexada()`, `imagem()` e `formatar_matriz()`.

Além dos exemplos em que tudo funciona corretamente, testamos situações como:

- Ativo sem jurisdição e ativo associado a duas jurisdições na relação.
- Origem que não pertence ao domínio informado.
- Relações sem correspondência entre os elementos intermediários.
- Consulta de imagem que não existe na relação.
- Matriz vazia.

Na execução mais recente dos testes, **26 testes passaram**. Esse resultado mostra que os casos testados funcionaram como esperado, mas não significa que todos os caminhos possíveis do código já tenham sido testados.

Para executar os testes pelo terminal, utilizamos:

```powershell
python -m pytest -v
```

## 9. Organização dos arquivos

Os arquivos relacionados ao núcleo matemático ficam na pasta `src/algorithms/`:

```text
src/
└── algorithms/
    ├── __init__.py
    ├── nucleo_mat.py
    └── conjuntos.py
```

O arquivo `nucleo_mat.py` reúne as funções de conjuntos, relações, mapeamentos e matrizes apresentadas nesta documentação. O arquivo `conjuntos.py` também possui algumas operações matemáticas semelhantes.

Essa separação permite que os serviços do sistema utilizem os resultados dos algoritmos sem colocar as regras de cadastro e controle de acesso dentro do núcleo matemático.

A explicação dos conjuntos e das relações do projeto aparece de forma mais detalhada em `03_modelagem_matematica.md`. Já a análise de complexidade dos algoritmos fica em `06_complexidade.md`.

## 10. Considerações finais

Com o desenvolvimento desses algoritmos, conseguimos aplicar os conteúdos de Matemática Discreta em situações do UrbanInventory. As operações com conjuntos ajudam a comparar grupos de ativos e permissões, enquanto as relações binárias permitem representar ligações entre usuários, órgãos e patrimônios.

Também usamos funções para conferir as associações dos ativos com as jurisdições e uma matriz para mostrar essas informações de maneira mais organizada. A composição de relações foi importante para entender como um dicionário pode facilitar as consultas.

Os testes automatizados ajudaram a verificar os resultados das funções e a encontrar possíveis erros durante o desenvolvimento. Assim, o núcleo matemático pode ser utilizado pelos outros módulos do projeto para realizar as operações que dependem desses conceitos.

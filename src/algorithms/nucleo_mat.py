"""NÚCLEO MATEMÁTICO - URBANINVENTORY"""

# Operações com conjuntos

def uniao(conjunto_a, conjunto_b):
    """Retorna todos os elementos dos dois conjuntos."""
    return conjunto_a | conjunto_b


def intersecao(conjunto_a, conjunto_b):
    """Retorna os elementos presentes nos dois conjuntos."""
    return conjunto_a & conjunto_b


def diferenca(conjunto_a, conjunto_b):
    """Retorna os elementos de A que não estão em B."""
    return conjunto_a - conjunto_b


def diferenca_simetrica(conjunto_a, conjunto_b):
    """Retorna os elementos que estão em A ou em B, mas não em ambos."""
    return conjunto_a ^ conjunto_b


def eh_vazio(conjunto):
    """Retorna True se o conjunto estiver vazio, False caso contrário."""
    return not conjunto


def sao_disjuntos(conjunto_a, conjunto_b):
    """Verifica se dois conjuntos não possuem elementos em comum."""
    return conjunto_a.isdisjoint(conjunto_b)


def eh_subconjunto(conjunto_a, conjunto_b):
    """Verifica se todos os elementos de A também pertencem a B."""
    return conjunto_a <= conjunto_b


# RELAÇÕES MATEMÁTICAS

def criar_relacao(elemento_a, elemento_b):
    """Cria uma relação entre dois elementos."""
    return (elemento_a, elemento_b)


def consultar_relacoes(relacoes, elemento):
    """Retorna os elementos relacionados ao elemento informado."""
    resultado = set()

    for origem, destino in relacoes:
        if origem == elemento:
            resultado.add(destino)

    return resultado


# FUNÇÕES E MAPEAMENTOS

def consultar_jurisdicao(mapeamento, ativo):
    """Consulta a jurisdição de um patrimônio."""
    return mapeamento.get(ativo)


def validar_mapeamento(mapeamento, ativos, jurisdicoes):
    """Verifica se todos os ativos possuem jurisdição válida."""
    for ativo in ativos:
        if ativo not in mapeamento:
            return False

        if mapeamento[ativo] not in jurisdicoes:
            return False

    return True



def composicao_indexada(relacao_ab, relacao_bc):
    """
    Compõe duas relações binárias A → B e B → C,
    utilizando um dicionário para agilizar as consultas.

    Retorna:
        Conjunto de pares ordenados (origem, destino).
    """
    indice = {}

    for intermediario, destino in relacao_bc:
        indice.setdefault(intermediario, set()).add(destino)

    resultado = set()

    for origem, intermediario in relacao_ab:
        for destino in indice.get(intermediario, set()):
            resultado.add((origem, destino))

    return resultado



def imagem(relacao, elemento):
    """Retorna as imagens associadas a um elemento de uma relação."""
    return {
        destino
        for origem, destino in relacao
        if origem == elemento
    }


def eh_funcao(relacao, dominio):
    """
    Verifica se cada elemento do domínio possui exatamente
    uma imagem na relação.

    Retorna:
        (True, set()) se a relação for uma função.
        (False, problemas) caso contrário.
    """
    imagens = {}

    for origem, destino in relacao:
        imagens.setdefault(origem, set()).add(destino)

    problemas = set()

    for elemento in dominio:
        if len(imagens.get(elemento, set())) != 1:
            problemas.add(elemento)

    for origem in imagens:
        if origem not in dominio:
            problemas.add(origem)

    return len(problemas) == 0, problemas


# MATRIZ DE PERTENCIMENTO

def matriz_pertencimento(conjuntos, colunas):
    """
    Cria a matriz de pertencimento entre jurisdições e ativos.

    Parâmetros:
        conjuntos: dicionário com jurisdições e conjuntos de ativos.
        colunas: lista de identificadores dos ativos.

    Retorna:
        Tupla contendo linhas, colunas e matriz binária.
    """
    linhas = list(conjuntos)

    matriz = [
        [1 if ativo in conjuntos[jurisdicao] else 0 for ativo in colunas]
        for jurisdicao in linhas
    ]

    return linhas, colunas, matriz



def formatar_matriz(linhas, colunas, matriz):
    """
    Formata a matriz de pertencimento para exibição.

    Parâmetros:
        linhas: nomes das jurisdições.
        colunas: identificadores dos ativos.
        matriz: matriz binária de pertencimento.

    Retorna:
        String com a matriz organizada em linhas e colunas.
    """
    if not linhas and not colunas:
        return "Matriz vazia"

    largura = max(
        [len(str(item)) for item in linhas] + [10]
    ) + 2

    cabecalho = " " * largura + "  ".join(map(str, colunas))

    resultado = [cabecalho]

    for jurisdicao, valores in zip(linhas, matriz):
        linha = (
            f"{str(jurisdicao):<{largura}}"
            + "  ".join(map(str, valores))
        )
        resultado.append(linha)

    return "\n".join(resultado)

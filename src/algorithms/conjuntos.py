
"""Operações matemáticas com conjuntos do UrbanInventory."""

from src.algorithms.nucleo_mat import (
    uniao,
    intersecao,
    diferenca
)


def diferenca_simetrica(a, b):
    """Retorna elementos que pertencem a apenas um dos conjuntos."""
    return a ^ b


def eh_vazio(conjunto):
    """Verifica se um conjunto está vazio."""
    return len(conjunto) == 0


def sao_disjuntos(a, b):
    """Verifica se dois conjuntos não possuem elementos em comum."""
    return a.isdisjoint(b)


def eh_subconjunto(a, b):
    """Verifica se todos os elementos de A pertencem a B."""
    return a.issubset(b)


# RELAÇÕES MATEMÁTICAS

def composicao_indexada(relacao_a, relacao_b):
    """Compõe duas relações binárias A→B e B→C."""
    indice = {}

    for origem, destino in relacao_b:
        indice.setdefault(origem, set()).add(destino)

    resultado = set()

    for origem, intermediario in relacao_a:
        for destino in indice.get(intermediario, set()):
            resultado.add((origem, destino))

    return resultado


def imagem(relacao, elemento):
    """Retorna os elementos relacionados à origem informada."""
    return {
        destino
        for origem, destino in relacao
        if origem == elemento
    }


def eh_funcao(relacao, dominio):
    """Verifica se cada elemento do domínio possui exatamente uma imagem."""
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
    """Cria uma matriz binária de jurisdições por ativos."""
    linhas = list(conjuntos)
    matriz = []

    for jurisdicao in linhas:
        linha = []

        for ativo in colunas:
            if ativo in conjuntos[jurisdicao]:
                linha.append(1)
            else:
                linha.append(0)

        matriz.append(linha)

    return linhas, colunas, matriz


def formatar_matriz(linhas, colunas, matriz):
    """Formata uma matriz de pertencimento para exibição."""
    largura = max(
        12,
        *(len(str(item)) + 2 for item in linhas + colunas)
    )

    cabecalho = "Jurisdição".ljust(largura)
    cabecalho += "".join(
        str(ativo).center(largura) for ativo in colunas
    )

    resultado = [cabecalho]

    for jurisdicao, valores in zip(linhas, matriz):
        linha = str(jurisdicao).ljust(largura)

        for valor in valores:
            linha += str(valor).center(largura)

        resultado.append(linha)

    return "\n".join(resultado)


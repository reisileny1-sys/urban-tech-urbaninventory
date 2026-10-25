# NÚCLEO MATEMÁTICO - URBANINVENTORY

# Operações com conjuntos

def uniao(conjunto_a, conjunto_b):
    # Retorna todos os elementos dos dois conjuntos.
    return conjunto_a | conjunto_b


def intersecao(conjunto_a, conjunto_b):
    # Retorna os elementos presentes nos dois conjuntos.
    return conjunto_a & conjunto_b


def diferenca(conjunto_a, conjunto_b):
    # Retorna os elementos de A que não estão em B.
    return conjunto_a - conjunto_b


# RELAÇÕES MATEMÁTICAS

def criar_relacao(elemento_a, elemento_b):
    # Cria uma relação entre dois elementos.
    return (elemento_a, elemento_b)


def consultar_relacoes(relacoes, elemento):
    # Retorna os elementos relacionados ao elemento informado.
    resultado = set()

    for origem, destino in relacoes:
        if origem == elemento:
            resultado.add(destino)

    return resultado


# FUNÇÕES E MAPEAMENTOS

def consultar_jurisdicao(mapeamento, ativo):
    # Consulta a jurisdição de um patrimônio.
    return mapeamento.get(ativo)


def validar_mapeamento(mapeamento, ativos, jurisdicoes):
    # Verifica se todos os ativos possuem jurisdição válida.
    for ativo in ativos:
        if ativo not in mapeamento:
            return False

        if mapeamento[ativo] not in jurisdicoes:
            return False

    return True

# MATRIZ DE PERTENCIMENTO

def matriz_pertencimento(ativos, jurisdicoes, mapeamento):
    # Cria uma matriz indicando a jurisdição de cada ativo.
    matriz = []

    for jurisdicao in jurisdicoes:
        linha = []

        for ativo in ativos:
            if mapeamento.get(ativo) == jurisdicao:
                linha.append(1)
            else:
                linha.append(0)

        matriz.append(linha)

    return matriz
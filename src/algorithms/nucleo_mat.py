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


def diferenca_simetrica(conjunto_a, conjunto_b):
    return conjunto_a ^ conjunto_b


def eh_vazio(conjunto):
    return not conjunto


def sao_disjuntos(conjunto_a, conjunto_b):
    return conjunto_a.isdisjoint(conjunto_b)


def eh_subconjunto(conjunto_a, conjunto_b):
    return conjunto_a <= conjunto_b


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


def composicao_indexada(relacao_ab, relacao_bc):
    return {
        (origem, destino)
        for origem, intermediario in relacao_ab
        for candidato, destino in relacao_bc
        if intermediario == candidato
    }


def imagem(relacao, elemento):
    return {destino for origem, destino in relacao if origem == elemento}


def eh_funcao(relacao, dominio):
    problemas = dominio - {origem for origem, _ in relacao}
    return not problemas, problemas

# MATRIZ DE PERTENCIMENTO

def matriz_pertencimento(mapeamento, ativos, jurisdicoes=None):
    # Cria uma matriz indicando a jurisdição de cada ativo.
    if jurisdicoes is None:
        jurisdicoes = list(mapeamento)
        matriz = mapeamento
    else:
        matriz = {jurisdicao: set(ativos_da_jurisdicao)
                  for jurisdicao, ativos_da_jurisdicao in mapeamento.items()}

    return [
        [1 if ativo in matriz.get(jurisdicao, set()) else 0 for ativo in ativos]
        for jurisdicao in jurisdicoes
    ]


def formatar_matriz(matriz, *linhas):
    if linhas:
        matriz = (matriz,) + linhas
    return "\n".join("  " + " ".join(map(str, linha)) for linha in matriz)
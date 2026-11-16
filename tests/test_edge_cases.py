
from src.algorithms.nucleo_mat import (
    uniao,
    intersecao,
    diferenca,
    consultar_relacoes,
    consultar_jurisdicao,
    validar_mapeamento,
    matriz_pertencimento
)


# Teste 1: união de conjuntos vazios
def test_uniao_vazia():
    assert uniao(set(), set()) == set()


# Teste 2: interseção sem elementos em comum
def test_intersecao_sem_elementos_comuns():
    a = {"A1", "A2"}
    b = {"A3", "A4"}

    assert intersecao(a, b) == set()


# Teste 3: diferença com conjunto A vazio
def test_diferenca_conjunto_vazio():
    assert diferenca(set(), {"A1"}) == set()


# Teste 4: elemento sem relações cadastradas
def test_consultar_relacoes_inexistentes():
    relacoes = {("Secretaria", "A1")}

    assert consultar_relacoes(relacoes, "Prefeitura") == set()


# Teste 5: ativo inexistente no mapeamento
def test_consultar_jurisdicao_inexistente():
    mapeamento = {"A1": "Norte"}

    assert consultar_jurisdicao(mapeamento, "A2") is None


# Teste 6: ativo sem jurisdição cadastrada
def test_validar_mapeamento_incompleto():
    ativos = ["A1", "A2"]
    jurisdicoes = ["Norte", "Sul"]
    mapeamento = {"A1": "Norte"}

    assert validar_mapeamento(
        mapeamento, ativos, jurisdicoes
    ) is False


# Teste 7: jurisdição inválida
def test_validar_mapeamento_jurisdicao_invalida():
    ativos = ["A1"]
    jurisdicoes = ["Norte", "Sul"]
    mapeamento = {"A1": "Leste"}

    assert validar_mapeamento(
        mapeamento, ativos, jurisdicoes
    ) is False


# Teste 8: matriz com listas vazias
def test_matriz_pertencimento_vazia():
    assert matriz_pertencimento([], [], {}) == []

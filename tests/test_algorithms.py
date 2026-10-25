
from src.algorithms.nucleo_mat import (
    uniao,
    intersecao,
    diferenca,
    criar_relacao,
    consultar_relacoes,
    consultar_jurisdicao,
    validar_mapeamento,
    matriz_pertencimento
)


# Teste de união
def test_uniao():
    a = {"A1", "A2"}
    b = {"A2", "A3"}

    assert uniao(a, b) == {"A1", "A2", "A3"}


# Teste de interseção
def test_intersecao():
    a = {"A1", "A2"}
    b = {"A2", "A3"}

    assert intersecao(a, b) == {"A2"}


# Teste de diferença
def test_diferenca():
    a = {"A1", "A2"}
    b = {"A2", "A3"}

    assert diferenca(a, b) == {"A1"}


# Teste de relações
def test_relacoes():
    relacoes = {
        criar_relacao("Secretaria", "A2"),
        criar_relacao("Secretaria", "A3")
    }

    resultado = consultar_relacoes(
        relacoes, "Secretaria"
    )

    assert resultado == {"A2", "A3"}


# Teste de jurisdição
def test_consultar_jurisdicao():
    mapeamento = {"A1": "Norte"}

    assert consultar_jurisdicao(
        mapeamento, "A1"
    ) == "Norte"


# Teste de validação
def test_validar_mapeamento():
    ativos = ["A1", "A2"]
    jurisdicoes = ["Norte", "Sul"]

    mapeamento = {
        "A1": "Norte",
        "A2": "Sul"
    }

    assert validar_mapeamento(
        mapeamento, ativos, jurisdicoes
    ) is True


# Teste da matriz
def test_matriz_pertencimento():
    ativos = ["A1", "A2", "A3"]
    jurisdicoes = ["Norte", "Sul"]

    mapeamento = {
        "A1": "Norte",
        "A2": "Norte",
        "A3": "Sul"
    }

    resultado = matriz_pertencimento(
        ativos, jurisdicoes, mapeamento
    )

    assert resultado == [
        [1, 1, 0],
        [0, 0, 1]
    ]

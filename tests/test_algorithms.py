
from src.algorithms.nucleo_mat import (
    uniao,
    intersecao,
    diferenca,
    criar_relacao,
    consultar_relacoes,
    consultar_jurisdicao,
    validar_mapeamento,
    matriz_pertencimento,
    eh_funcao,
    composicao_indexada,
    imagem,
    formatar_matriz
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
    conjuntos = {
        "Norte": {"A1", "A2"},
        "Sul": {"A3"}
    }

    colunas = ["A1", "A2", "A3"]

    linhas, ativos, matriz = matriz_pertencimento(conjuntos, colunas)

    assert linhas == ["Norte", "Sul"]
    assert ativos == ["A1", "A2", "A3"]
    assert matriz == [
        [1, 1, 0],
        [0, 0, 1]
    ]

    
# Teste de função válida
def test_eh_funcao_valida():
    relacao = {
        ("A1", "Norte"),
        ("A2", "Sul")
    }
    dominio = {"A1", "A2"}

    assert eh_funcao(relacao, dominio) == (True, set())


# Teste de ativo associado a duas jurisdições
def test_eh_funcao_duas_jurisdicoes():
    relacao = {
        ("A1", "Norte"),
        ("A1", "Sul")
    }
    dominio = {"A1"}

    assert eh_funcao(relacao, dominio) == (False, {"A1"})


# Teste de ativo sem jurisdição
def test_eh_funcao_sem_jurisdicao():
    relacao = {
        ("A1", "Norte")
    }
    dominio = {"A1", "A2"}

    assert eh_funcao(relacao, dominio) == (False, {"A2"})


# Teste de ativo fora do domínio
def test_eh_funcao_fora_dominio():
    relacao = {
        ("A1", "Norte"),
        ("A3", "Sul")
    }
    dominio = {"A1"}

    assert eh_funcao(relacao, dominio) == (False, {"A3"})


# Teste com conjuntos vazios
def test_eh_funcao_vazia():
    relacao = set()
    dominio = set()

    assert eh_funcao(relacao, dominio) == (True, set())


# TESTES DE COMPOSIÇÃO DE RELAÇÕES

def test_composicao_indexada():
    """Verifica a associação indireta entre usuários e ativos."""
    usuario_orgao = {
        ("U1", "O1"),
        ("U2", "O2")
    }

    orgao_ativo = {
        ("O1", "A1"),
        ("O1", "A2"),
        ("O2", "A3")
    }

    resultado = composicao_indexada(
        usuario_orgao, orgao_ativo
    )

    assert resultado == {
        ("U1", "A1"),
        ("U1", "A2"),
        ("U2", "A3")
    }


def test_composicao_sem_correspondencia():
    """Verifica relações sem elementos intermediários comuns."""
    usuario_orgao = {("U1", "O1")}
    orgao_ativo = {("O2", "A1")}

    resultado = composicao_indexada(
        usuario_orgao, orgao_ativo
    )

    assert resultado == set()


# TESTES DE IMAGEM DE UMA RELAÇÃO

def test_imagem():
    """Verifica os destinos associados a um elemento."""
    relacao = {
        ("A1", "Norte"),
        ("A2", "Sul"),
        ("A3", "Norte")
    }

    resultado = imagem(relacao, "A1")

    assert resultado == {"Norte"}


def test_imagem_inexistente():
    """Verifica um elemento sem associação na relação."""
    relacao = {
        ("A1", "Norte")
    }

    resultado = imagem(relacao, "A2")

    assert resultado == set()


# TESTES DE FORMATAÇÃO DA MATRIZ

def test_formatar_matriz():
    """Verifica a apresentação de linhas, colunas e valores."""
    linhas = ["Norte", "Sul"]
    colunas = ["A1", "A2", "A3"]
    matriz = [
        [1, 1, 0],
        [0, 0, 1]
    ]

    resultado = formatar_matriz(
        linhas, colunas, matriz
    )

    linhas_texto = resultado.splitlines()

    assert linhas_texto[0].split() == ["A1", "A2", "A3"]
    assert linhas_texto[1].split() == ["Norte", "1", "1", "0"]
    assert linhas_texto[2].split() == ["Sul", "0", "0", "1"]


def test_formatar_matriz_vazia():
    """Verifica a mensagem exibida para uma matriz vazia."""
    resultado = formatar_matriz([], [], [])

    assert resultado == "Matriz vazia"

"""Dados sintéticos de exemplo para demonstração e testes."""

from src.services.inventario import Inventario


def carregar_exemplo():
    """Cria um Inventario já preenchido com dados de exemplo.

    10 ativos, 3 jurisdições, 2 órgãos, 3 papéis e 3 usuários.
    O ativo A10 fica de propósito SEM jurisdição (caso de borda).
    """
    inv = Inventario()

    for j in ("Norte", "Sul", "Centro"):
        inv.cadastrar_jurisdicao(j)

    for p in ("consultar", "criar", "atualizar", "excluir"):
        inv.cadastrar_permissao(p)

    inv.cadastrar_papel("Administrador", ["consultar", "criar", "atualizar", "excluir"])
    inv.cadastrar_papel("Fiscal", ["consultar", "atualizar"])
    inv.cadastrar_papel("Visitante", ["consultar"])

    inv.cadastrar_orgao("O1", "Secretaria de Obras")
    inv.cadastrar_orgao("O2", "Secretaria de Mobilidade")

    inv.cadastrar_local("L1", "Av. Norte, 100", "Norte")
    inv.cadastrar_local("L2", "Rua Sul, 50", "Sul")
    inv.cadastrar_local("L3", "Praça Central, s/n", "Centro")

    #            id     tipo        jurisdição  pendente
    ativos = [
        ("A1", "poste", "Norte", False),
        ("A2", "semaforo", "Norte", True),
        ("A3", "abrigo", "Sul", True),
        ("A4", "poste", "Centro", False),
        ("A5", "poste", "Norte", True),
        ("A6", "semaforo", "Sul", False),
        ("A7", "abrigo", "Centro", True),
        ("A8", "poste", "Sul", False),
        ("A9", "semaforo", "Centro", False),
        ("A10", "abrigo", None, True),
    ]
    for id_a, tipo, jur, pend in ativos:
        inv.cadastrar_ativo(id_a, tipo, jur, pend)

    # Obras cuida de postes e abrigos; Mobilidade de semáforos
    for a in ("A1", "A3", "A4", "A5", "A7", "A8", "A10"):
        inv.associar_orgao_ativo("O1", a)
    for a in ("A2", "A6", "A9"):
        inv.associar_orgao_ativo("O2", a)

    inv.cadastrar_usuario("U001", "João", "O1", ["Fiscal"], "Norte")
    inv.cadastrar_usuario("U002", "Maria", "O1", ["Administrador"], "Centro")
    inv.cadastrar_usuario("U003", "Ana", "O2", ["Visitante", "Fiscal"], "Sul")

    return inv

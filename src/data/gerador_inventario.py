"""Gerador de dados sintéticos em grande escala (para medir desempenho)."""

import random

from src.services.inventario import Inventario

TIPOS = ("poste", "semaforo", "abrigo", "lixeira", "banco")
JURISDICOES = ("Norte", "Sul", "Centro", "Leste", "Oeste")


def gerar_inventario(n_ativos, n_usuarios=None, semente=42):
    """Cria um Inventario com n_ativos ativos aleatórios.

    A semente fixa garante que o experimento é reproduzível.
    """
    rnd = random.Random(semente)
    n_usuarios = n_usuarios if n_usuarios is not None else max(1, n_ativos // 10)
    inv = Inventario()
    for j in JURISDICOES:
        inv.cadastrar_jurisdicao(j)
    for p in ("consultar", "criar", "atualizar", "excluir"):
        inv.cadastrar_permissao(p)
    inv.cadastrar_papel("Administrador", ["consultar", "criar", "atualizar", "excluir"])
    inv.cadastrar_papel("Fiscal", ["consultar", "atualizar"])
    inv.cadastrar_papel("Visitante", ["consultar"])
    papeis = list(inv.papeis)

    n_orgaos = max(1, n_ativos // 100)
    for i in range(n_orgaos):
        inv.cadastrar_orgao(f"O{i + 1}", f"Órgão {i + 1}")

    for i in range(n_ativos):
        id_a = f"A{i + 1}"
        jur = rnd.choice(JURISDICOES) if rnd.random() > 0.02 else None
        inv.cadastrar_ativo(id_a, rnd.choice(TIPOS), jur, rnd.random() < 0.3)
        inv.associar_orgao_ativo(f"O{rnd.randint(1, n_orgaos)}", id_a)

    for i in range(n_usuarios):
        inv.cadastrar_usuario(
            f"U{i + 1:04d}",
            f"Usuário {i + 1}",
            f"O{rnd.randint(1, n_orgaos)}",
            rnd.sample(papeis, rnd.randint(1, 2)),
            rnd.choice(JURISDICOES),
        )
    return inv

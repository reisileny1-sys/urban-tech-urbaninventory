"""Camada de dados / I/O: leitura e escrita de arquivos CSV.
Usa só módulo csv da biblioteca padrão.
Lista dentro de uma célula como papéis, permissões de um papel, são separados por ';'.
"""

import csv
import os

from src.services.inventario import Inventario
from src.utils.excecoes import DadoInvalidoError

PASTA_PADRAO = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")


def _ler(pasta, nome):
    # lê o CSV e devolve uma lista de dicionários (um)
    caminho = os.path.join(pasta, nome)
    if not os.path.exists(caminho):
        raise DadoInvalidoError(f"Arquivo não encontrado: {caminho}")
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _lista(celula):
    return [x.strip() for x in (celula or "").split(";") if x.strip()]


def _opcional(celula):
    # celula vazia vira None.
    return celula.strip() if celula and celula.strip() else None


def carregar_csv(pasta=PASTA_PADRAO):
    """
    Monta um inventário a partir dos CSVs da pasta
    A ordem importa: jurisdição e permissões primeiro,
    porque as outras entidades fazerem referência a elas (integridade referencial)
    """

    inv = Inventario()
    for linha in _ler(pasta, "jurisdicao.csv"):
        inv.cadastrar_jurisdicao(linha["nome"])
    for linha in _ler(pasta, "permissoes.csv"):
        inv.cadastrar_permissao(linha["nome"])
    for linha in _ler(pasta, "papeis.csv"):
        inv.cadastrar_papel(linha["nome"], _lista(linha["permissoes"]))
    for linha in _ler(pasta, "orgaos.csv"):
        inv.cadastrar_orgao(linha["id"], linha["nome"])
    for linha in _ler(pasta, "localizacao.csv"):
        inv.cadastrar_local(linha["id"], linha["endereco"], linha["jurisdicao"])
    for linha in _ler(pasta, "ativos.csv"):
        inv.cadastrar_ativo(
            linha["id"],
            linha["tipo"],
            _opcional(linha["jurisdicao"]),
            linha["manutencao_pendente"].strip() == "1",
        )
        orgao = _opcional(linha.get("orgao"))
        if orgao:
            inv.associar_orgao_ativo(orgao, linha["id"])
    for linha in _ler(pasta, "usuarios.csv"):
        orgao = _opcional(linha.get("orgao") or linha.get("orgaos"))
        if orgao and orgao.isdigit():
            orgao = f"O{int(orgao):d}"
        inv.cadastrar_usuario(
            linha["id"],
            linha["nome"],
            orgao,
            _lista(linha["papeis"]),
            _opcional(linha["jurisdicao"]),
        )

    return inv


def exportar_ativos_csv(inv, caminho):
    """
    Salva os ativos atuais em CSV

    """

    dono = {a: o.id for o in inv.orgaos.values() for a in o.ativos}
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "tipo", "jurisdicao", "manutencao_pendente", "orgao"])
        for a in inv.ativos.values():
            w.writerow(
                [
                    a.id,
                    a.tipo,
                    a.jurisdicao or "",
                    int(a.manutencao_pendente),
                    dono.get(a.id, ""),
                ]
            )
    return caminho

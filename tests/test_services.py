
"""Testes dos serviços do UrbanInventory.

executar teste: python -m unittest tests.test_services -v"""

import unittest

from src.services.inventario import Inventario
from src.utils.excecoes import (
    AcessoNegadoError,
    AtivoSemJurisdicaoError,
    EntidadeDuplicadaError,
    EntidadeInexistenteError,
    PermissaoInvalidaError
)


class TestServices(unittest.TestCase):

    def setUp(self):
        """Prepara os dados iniciais para cada teste."""
        self.inv = Inventario()

        self.inv.cadastrar_jurisdicao("Norte")
        self.inv.cadastrar_jurisdicao("Sul")

        self.inv.cadastrar_orgao("O1", "Secretaria de Educação")

        self.inv.cadastrar_permissao("consultar")
        self.inv.cadastrar_permissao("excluir")

        self.inv.cadastrar_papel("Fiscal", {"consultar"})

        self.inv.cadastrar_usuario(
            "U1",
            "João",
            "O1",
            {"Fiscal"},
            "Norte"
        )

    def test_cadastrar_jurisdicao(self):
        jur = self.inv.cadastrar_jurisdicao("Centro")

        self.assertEqual(jur.nome, "Centro")
        self.assertIn("Centro", self.inv.jurisdicoes)

    def test_cadastrar_ativo(self):
        id_a = "A11"
        tipo = "poste"
        jur = "Norte"
        pend = False

        ativo = self.inv.cadastrar_ativo(id_a, tipo, jur, pend)

        self.assertEqual(ativo.id, id_a)
        self.assertEqual(ativo.tipo, tipo)
        self.assertEqual(ativo.jurisdicao, jur)
        self.assertFalse(ativo.manutencao_pendente)

    def test_cadastrar_local(self):
        id_l = "L4"
        end = "Rua Central"
        jur = "Norte"

        local = self.inv.cadastrar_local(id_l, end, jur)

        self.assertEqual(local.id, id_l)
        self.assertEqual(local.endereco, end)
        self.assertEqual(local.jurisdicao, jur)

    def test_cadastrar_usuario(self):
        id_u = "U2"
        nome = "Maria"
        orgao = "O1"
        papeis = {"Fiscal"}
        jur = "Sul"

        usuario = self.inv.cadastrar_usuario(
            id_u, nome, orgao, papeis, jur
        )

        self.assertEqual(usuario.id, id_u)
        self.assertEqual(usuario.nome, nome)
        self.assertEqual(usuario.orgao, orgao)
        self.assertEqual(usuario.papeis, papeis)
        self.assertEqual(usuario.jurisdicao, jur)

    def test_cadastrar_papel(self):
        nome = "Administrador"

        papel = self.inv.cadastrar_papel(
            nome, {"consultar", "excluir"}
        )

        self.assertEqual(papel.nome, nome)
        self.assertEqual(
            papel.permissoes,
            {"consultar", "excluir"}
        )

    def test_permissao_invalida(self):
        with self.assertRaises(PermissaoInvalidaError):
            self.inv.cadastrar_papel(
                "Gerente", {"permissao_inexistente"}
            )

    def test_cadastrar_entidade_duplicada(self):
        with self.assertRaises(EntidadeDuplicadaError):
            self.inv.cadastrar_ativo("A11", "poste", "Norte")

            self.inv.cadastrar_ativo("A11", "semaforo", "Sul")

    def test_associar_ativo_jurisdicao(self):
        id_a = "A12"

        self.inv.cadastrar_ativo(id_a, "semaforo")

        self.inv.associar_ativo_jurisdicao(id_a, "Sul")

        self.assertEqual(
            self.inv.ativos[id_a].jurisdicao,
            "Sul"
        )

    def test_associar_orgao_ativo(self):
        id_a = "A13"

        self.inv.cadastrar_ativo(id_a, "abrigo", "Norte")
        self.inv.associar_orgao_ativo("O1", id_a)

        self.assertIn(id_a, self.inv.orgaos["O1"].ativos)

    def test_consultar_ativos_por_jurisdicao(self):
        self.inv.cadastrar_ativo("A14", "poste", "Norte")
        self.inv.cadastrar_ativo("A15", "semaforo", "Sul")

        ativos = self.inv.ativos_da_jurisdicao("Norte")

        self.assertIn("A14", ativos)
        self.assertNotIn("A15", ativos)

    def test_consultar_manutencao_pendente(self):
        self.inv.cadastrar_ativo(
            "A16", "poste", "Norte", True
        )

        ativos = self.inv.ativos_com_manutencao_pendente()

        self.assertIn("A16", ativos)

    def test_exigir_jurisdicao(self):
        self.inv.cadastrar_ativo("A17", "abrigo")

        with self.assertRaises(AtivoSemJurisdicaoError):
            self.inv.exigir_jurisdicao("A17")

    def test_acesso_autorizado(self):
        resultado = self.inv.tem_permissao("U1", "consultar")

        self.assertTrue(resultado)

    def test_acesso_negado(self):
        with self.assertRaises(AcessoNegadoError):
            self.inv.exigir_permissao("U1", "excluir")

    def test_usuario_inexistente(self):
        with self.assertRaises(EntidadeInexistenteError):
            self.inv.permissoes_do_usuario("U99")

    def test_excluir_ativo(self):
        id_a = "A18"

        self.inv.cadastrar_ativo(id_a, "poste", "Norte")
        self.inv.associar_orgao_ativo("O1", id_a)

        self.inv.associar_permissao_papel("Fiscal", "excluir")

        self.inv.excluir_ativo("U1", id_a)

        self.assertNotIn(id_a, self.inv.ativos)
        self.assertNotIn(id_a, self.inv.orgaos["O1"].ativos)

    def test_gerar_relatorio(self):
        self.inv.cadastrar_ativo("A19", "poste", "Norte")

        relatorio = self.inv.relatorio()

        self.assertIn("RELATÓRIO URBANINVENTORY", relatorio)
        self.assertIn("Total de ativos: 1", relatorio)


if __name__ == "__main__":
    unittest.main()

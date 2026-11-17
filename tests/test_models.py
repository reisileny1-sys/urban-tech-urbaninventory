
"""Testes das entidades.

executar teste com: python -m unittest tests.test_models -v"""

import unittest

from src.models.entidades import (
    Jurisdicao,
    Local,
    Ativo,
    Orgao,
    Papel,
    Usuario
)


class TestModelos(unittest.TestCase):

    def test_jurisdicao(self):
        jur = Jurisdicao("Norte")
        self.assertEqual(jur.nome, "Norte")

    def test_local(self):
        id_l = "L4"
        end = "Rua Central"
        jur = "Norte"

        local = Local(id_l, end, jur)

        self.assertEqual(local.id, id_l)
        self.assertEqual(local.endereco, end)
        self.assertEqual(local.jurisdicao, jur)

    def test_ativo_padrao(self):
        id_a = "A11"
        tipo = "poste"

        ativo = Ativo(id_a, tipo)

        self.assertEqual(ativo.id, id_a)
        self.assertEqual(ativo.tipo, tipo)
        self.assertIsNone(ativo.jurisdicao)
        self.assertFalse(ativo.manutencao_pendente)
        self.assertIsNone(ativo.local)

    def test_ativo_com_jurisdicao(self):
        id_a = "A12"
        tipo = "semaforo"
        jur = "Norte"
        pend = True

        ativo = Ativo(id_a, tipo, jur, pend)

        self.assertEqual(ativo.jurisdicao, jur)
        self.assertTrue(ativo.manutencao_pendente)

    def test_orgao(self):
        id_o = "O1"
        nome = "Secretaria de Educação"

        orgao = Orgao(id_o, nome)

        self.assertEqual(orgao.id, id_o)
        self.assertEqual(orgao.nome, nome)
        self.assertEqual(orgao.ativos, set())

    def test_papel(self):
        nome = "Fiscal"
        perms = {"consultar", "atualizar"}

        papel = Papel(nome, perms)

        self.assertEqual(papel.nome, nome)
        self.assertEqual(papel.permissoes, perms)

    def test_usuario(self):
        id_u = "U004"
        nome = "João"
        orgao = "O1"
        papeis = {"Fiscal"}
        jur = "Norte"

        usuario = Usuario(id_u, nome, orgao, papeis, jur)

        self.assertEqual(usuario.id, id_u)
        self.assertEqual(usuario.nome, nome)
        self.assertEqual(usuario.orgao, orgao)
        self.assertEqual(usuario.papeis, papeis)
        self.assertEqual(usuario.jurisdicao, jur)

    def test_conjuntos_independentes(self):
        orgao1 = Orgao("O1", "Secretaria A")
        orgao2 = Orgao("O2", "Secretaria B")

        orgao1.ativos.add("A11")

        self.assertEqual(orgao1.ativos, {"A11"})
        self.assertEqual(orgao2.ativos, set())

    def test_permissoes_independentes(self):
        papel1 = Papel("Administrador")
        papel2 = Papel("Fiscal")

        papel1.permissoes.add("excluir")

        self.assertEqual(papel1.permissoes, {"excluir"})
        self.assertEqual(papel2.permissoes, set())


if __name__ == "__main__":
    unittest.main()

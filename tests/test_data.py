"""Testes da camada de dados (CSV e gerador sintético)."""

import os
import tempfile
import unittest

from src.data.manuseio_dados import carregar_csv, exportar_ativos_csv
from src.data.dados_sinteticos_exemplo import carregar_exemplo
from src.data.gerador_inventario import gerar_inventario
from src.utils.excecoes import DadoInvalidoError


class TestDados(unittest.TestCase):

    def test_csv_igual_ao_exemplo(self):
        a, b = carregar_csv(), carregar_exemplo()
        self.assertEqual(set(a.ativos), set(b.ativos))
        self.assertEqual(a.relacao_orgao_ativo(), b.relacao_orgao_ativo())
        self.assertEqual(a.relacao_usuario_papel(), b.relacao_usuario_papel())
        self.assertEqual(a.consulta_norte_pendente(), b.consulta_norte_pendente())

    def test_pasta_inexistente(self):
        with self.assertRaises(DadoInvalidoError):
            carregar_csv("/pasta/que/nao/existe")

    def test_exportar(self):
        inv = carregar_exemplo()
        with tempfile.TemporaryDirectory() as d:
            caminho = exportar_ativos_csv(inv, os.path.join(d, "ativos.csv"))
            with open(caminho, encoding="utf-8") as f:
                self.assertEqual(len(f.readlines()), 11)  # cabeçalho + 10

    def test_gerador_reproduzivel(self):
        a = gerar_inventario(500)
        b = gerar_inventario(500)
        self.assertEqual(len(a.ativos), 500)
        self.assertEqual(
            a.ativos_com_manutencao_pendente(), b.ativos_com_manutencao_pendente()
        )


if __name__ == "__main__":
    unittest.main()

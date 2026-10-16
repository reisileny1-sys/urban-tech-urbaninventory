"""Exceções do domínio UrbanInventory.

Cada erro de regra de negócio tem sua própria exceção, para que a
interface e os testes saibam exatamente o que deu errado.
"""


class UrbanInventoryError(Exception):
    """Erro base do sistema."""


class EntidadeInexistenteError(UrbanInventoryError):
    """Usuário, papel, ativo, órgão ou jurisdição não encontrado."""


class EntidadeDuplicadaError(UrbanInventoryError):
    """Tentativa de cadastrar um ID que já existe."""


class PermissaoInvalidaError(UrbanInventoryError):
    """Permissão que não pertence ao conjunto universo de permissões."""


class AcessoNegadoError(UrbanInventoryError):
    """Usuário não possui a permissão necessária (RBAC)."""


class AtivoSemJurisdicaoError(UrbanInventoryError):
    """Ativo que não está associado a nenhuma jurisdição."""


class DadoInvalidoError(UrbanInventoryError):
    """Campo vazio ou valor fora do esperado."""

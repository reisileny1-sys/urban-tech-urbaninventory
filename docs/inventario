"""Serviços do UrbanInventory: cadastros, relações, consultas, RBAC e relatório."""

from src.algorithms import conjuntos as cj
from src.models.entidades import Ativo, Jurisdicao, Local, Orgao, Papel, Usuario
from src.utils.excecoes import (
    AcessoNegadoError, AtivoSemJurisdicaoError, EntidadeDuplicadaError,
    EntidadeInexistenteError, PermissaoInvalidaError,
)


class Inventario:
    """Sistema UrbanInventory em memória."""

    def __init__(self):
        self.jurisdicoes = {}
        self.locais = {}
        self.ativos = {}
        self.orgaos = {}
        self.permissoes = set()
        self.papeis = {}
        self.usuarios = {}

    @staticmethod
    def _buscar(tabela, chave, entidade):
        if chave not in tabela:
            raise EntidadeInexistenteError(f"{entidade} '{chave}' não existe.")
        return tabela[chave]

    @staticmethod
    def _garantir_novo(tabela, chave, entidade):
        if chave in tabela:
            raise EntidadeDuplicadaError(
                f"{entidade} '{chave}' já está cadastrado(a)."
            )

    # Cadastros (RF01–RF05)
    def cadastrar_jurisdicao(self, nome):
        item = Jurisdicao(nome)
        self._garantir_novo(self.jurisdicoes, item.nome, "Jurisdição")
        self.jurisdicoes[item.nome] = item
        return item

    def cadastrar_local(self, id_local, endereco, jurisdicao):
        self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        item = Local(id_local, endereco, jurisdicao)
        self._garantir_novo(self.locais, item.id, "Local")
        self.locais[item.id] = item
        return item

    def cadastrar_ativo(self, id_ativo, tipo, jurisdicao=None,
                        manutencao_pendente=False, local=None):
        if local is not None:
            jurisdicao = self._buscar(self.locais, local, "Local").jurisdicao
        if jurisdicao is not None:
            self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        item = Ativo(id_ativo, tipo, jurisdicao, manutencao_pendente, local)
        self._garantir_novo(self.ativos, item.id, "Ativo")
        self.ativos[item.id] = item
        return item

    def cadastrar_orgao(self, id_orgao, nome):
        item = Orgao(id_orgao, nome)
        self._garantir_novo(self.orgaos, item.id, "Órgão")
        self.orgaos[item.id] = item
        return item

    def cadastrar_permissao(self, nome):
        nome = nome.strip().lower()
        if not nome:
            raise PermissaoInvalidaError("Permissão não pode ser vazia.")
        self.permissoes.add(nome)
        return nome

    def cadastrar_papel(self, nome, permissoes=()):
        perms = {p.strip().lower() for p in permissoes}
        invalidas = cj.diferenca(perms, self.permissoes)
        if invalidas:
            raise PermissaoInvalidaError(
                f"Permissões inválidas: {sorted(invalidas)}"
            )
        item = Papel(nome, perms)
        self._garantir_novo(self.papeis, item.nome, "Papel")
        self.papeis[item.nome] = item
        return item

    def cadastrar_usuario(self, id_usuario, nome, orgao=None, papeis=(),
                          jurisdicao=None):
        if orgao is not None:
            self._buscar(self.orgaos, orgao, "Órgão")
        for papel in papeis:
            self._buscar(self.papeis, papel, "Papel")
        if jurisdicao is not None:
            self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        item = Usuario(id_usuario, nome, orgao, papeis, jurisdicao)
        self._garantir_novo(self.usuarios, item.id, "Usuário")
        self.usuarios[item.id] = item
        return item

    # Associações (RF06)
    def associar_ativo_jurisdicao(self, id_ativo, jurisdicao):
        ativo = self._buscar(self.ativos, id_ativo, "Ativo")
        self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        ativo.jurisdicao = jurisdicao

    def associar_orgao_ativo(self, id_orgao, id_ativo):
        orgao = self._buscar(self.orgaos, id_orgao, "Órgão")
        self._buscar(self.ativos, id_ativo, "Ativo")
        orgao.ativos.add(id_ativo)

    def associar_permissao_papel(self, nome_papel, permissao):
        papel = self._buscar(self.papeis, nome_papel, "Papel")
        permissao = permissao.strip().lower()
        if permissao not in self.permissoes:
            raise PermissaoInvalidaError(
                f"Permissão '{permissao}' não existe."
            )
        papel.permissoes.add(permissao)

    def atribuir_papel(self, id_usuario, nome_papel):
        usuario = self._buscar(self.usuarios, id_usuario, "Usuário")
        self._buscar(self.papeis, nome_papel, "Papel")
        usuario.papeis.add(nome_papel)

    def marcar_manutencao(self, id_ativo, pendente=True):
        self._buscar(self.ativos, id_ativo, "Ativo").manutencao_pendente = bool(pendente)

    # Consultas por conjuntos (RF07)
    def universo_ativos(self):
        return set(self.ativos)

    def ativos_da_jurisdicao(self, jurisdicao):
        self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        return {a.id for a in self.ativos.values() if a.jurisdicao == jurisdicao}

    def ativos_com_manutencao_pendente(self):
        return {a.id for a in self.ativos.values() if a.manutencao_pendente}

    def ativos_por_tipo(self, tipo):
        return {a.id for a in self.ativos.values() if a.tipo == tipo}

    def ativos_do_orgao(self, id_orgao):
        return set(self._buscar(self.orgaos, id_orgao, "Órgão").ativos)

    def ativos_sem_jurisdicao(self):
        return {a.id for a in self.ativos.values() if a.jurisdicao is None}

    def consulta_norte_pendente(self, jurisdicao="Norte"):
        a = self.ativos_da_jurisdicao(jurisdicao)
        b = self.ativos_com_manutencao_pendente()
        return {
            "A": a,
            "B": b,
            "A ∩ B": cj.intersecao(a, b),
            "A − B": cj.diferenca(a, b),
            "A ∪ B": cj.uniao(a, b),
        }

    # Relações (RF08)
    def relacao_usuario_orgao(self):
        return {(u.id, u.orgao) for u in self.usuarios.values() if u.orgao is not None}

    def relacao_orgao_ativo(self):
        return {(o.id, ativo) for o in self.orgaos.values() for ativo in o.ativos}

    def relacao_usuario_papel(self):
        return {(u.id, papel) for u in self.usuarios.values() for papel in u.papeis}

    def relacao_papel_permissao(self):
        return {(p.nome, perm) for p in self.papeis.values() for perm in p.permissoes}

    def relacao_ativo_jurisdicao(self):
        return {
            (a.id, a.jurisdicao)
            for a in self.ativos.values()
            if a.jurisdicao is not None
        }

    def ativos_que_usuario_gerencia(self, id_usuario):
        self._buscar(self.usuarios, id_usuario, "Usuário")
        relacao = cj.composicao_indexada(
            self.relacao_usuario_orgao(), self.relacao_orgao_ativo()
        )
        return cj.imagem(relacao, id_usuario)

    # Validações (RF09)
    def validar_mapeamento_ativo_jurisdicao(self):
        return cj.eh_funcao(
            self.relacao_ativo_jurisdicao(), self.universo_ativos()
        )

    def exigir_jurisdicao(self, id_ativo):
        ativo = self._buscar(self.ativos, id_ativo, "Ativo")
        if ativo.jurisdicao is None:
            raise AtivoSemJurisdicaoError(
                f"Ativo '{id_ativo}' não possui jurisdição."
            )
        return ativo.jurisdicao

    # Controle de acesso por papéis (RF10)
    def permissoes_do_usuario(self, id_usuario):
        usuario = self._buscar(self.usuarios, id_usuario, "Usuário")
        resultado = set()
        for nome in usuario.papeis:
            papel = self._buscar(self.papeis, nome, "Papel")
            resultado = cj.uniao(resultado, papel.permissoes)
        return resultado

    def tem_permissao(self, id_usuario, permissao):
        permissao = permissao.strip().lower()
        if permissao not in self.permissoes:
            raise PermissaoInvalidaError(
                f"Permissão '{permissao}' não existe."
            )
        return permissao in self.permissoes_do_usuario(id_usuario)

    def exigir_permissao(self, id_usuario, permissao):
        if not self.tem_permissao(id_usuario, permissao):
            nome = self.usuarios[id_usuario].nome
            raise AcessoNegadoError(
                f"Acesso negado: {nome} não tem permissão '{permissao}'."
            )
        return True

    def excluir_ativo(self, id_usuario, id_ativo):
        self.exigir_permissao(id_usuario, "excluir")
        self._buscar(self.ativos, id_ativo, "Ativo")
        del self.ativos[id_ativo]
        for orgao in self.orgaos.values():
            orgao.ativos.discard(id_ativo)

    # Matriz e relatório (RF11)
    def matriz_jurisdicao_ativo(self):
        conjuntos = {j: self.ativos_da_jurisdicao(j) for j in self.jurisdicoes}
        colunas = sorted(self.ativos, key=_ordem_natural)
        return cj.matriz_pertencimento(conjuntos, colunas)

    def relatorio(self):
        linhas = [
            "=" * 50,
            "RELATÓRIO URBANINVENTORY",
            "=" * 50,
            f"Total de ativos: {len(self.ativos)}",
            (f"Jurisdições: {len(self.jurisdicoes)} | "
             f"Órgãos: {len(self.orgaos)} | Usuários: {len(self.usuarios)} | "
             f"Papéis: {len(self.papeis)}"),
            "",
            "Ativos por jurisdição:",
        ]
        pendentes = self.ativos_com_manutencao_pendente()
        for jurisdicao in self.jurisdicoes:
            ativos = self.ativos_da_jurisdicao(jurisdicao)
            pend = cj.intersecao(ativos, pendentes)
            linhas.append(
                f"  {jurisdicao:<8} {len(ativos):>3} ativos | "
                f"{len(pend):>3} pendentes {_fmt(pend)}"
            )
        linhas.extend(["  Sem jurisdição: " + _fmt(self.ativos_sem_jurisdicao()), ""])
        ok, problemas = self.validar_mapeamento_ativo_jurisdicao()
        status = "SIM" if ok else f"NÃO (problemas: {_fmt(problemas)})"
        linhas.extend([
            f"Ativo → Jurisdição é função? {status}",
            "",
            "Matriz de pertencimento:",
            cj.formatar_matriz(*self.matriz_jurisdicao_ativo()),
        ])
        return "\n".join(linhas)


def _ordem_natural(texto):
    """Ordena identificadores como A2 antes de A10."""
    prefixo = texto.rstrip("0123456789")
    numero = texto[len(prefixo):]
    return prefixo, int(numero) if numero else 0


def _fmt(conjunto):
    """Formata um conjunto ordenado; usa ∅ quando vazio."""
    return "∅" if not conjunto else "{" + ", ".join(sorted(conjunto, key=_ordem_natural)) + "}"

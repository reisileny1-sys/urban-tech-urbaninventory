"""Serviços do UrbanInventory: cadastros, relações, consultas, RBAC e relatório."""

from src.algorithms import nucleo_mat as cj

from src.models.entidades import Ativo, Jurisdicao, Local, Orgao, Papel, Usuario
from src.utils.excecoes import (
    AcessoNegadoError,
    AtivoSemJurisdicaoError,
    EntidadeDuplicadaError,
    EntidadeInexistenteError,
    PermissaoInvalidaError,
)


class Inventario:
    """Sistema UrbanInventory em memória."""
    
    def __init__(self):
        """Inicializa o inventário e suas estruturas de armazenamento.
        Cria dicionários para entidades e um conjunto para permissões.
        Todos os dados permanecem em memória durante a execução."""
        self.jurisdicoes = {}
        self.locais = {}
        self.ativos = {}
        self.orgaos = {}
        self.permissoes = set()
        self.papeis = {}
        self.usuarios = {}

    @staticmethod
    def _buscar(tabela, chave, entidade):
        """Busca uma entidade em uma tabela pela chave informada.
        Args:
            tabela: Dicionário que armazena as entidades.
            chave: Identificador usado para localizar a entidade.
            entidade: Nome da entidade, usado na mensagem de erro.
        Returns:
            A entidade encontrada.
        Raises:
            EntidadeInexistenteError: Se a chave não estiver cadastrada."""
        if chave not in tabela:
            raise EntidadeInexistenteError(f"{entidade} '{chave}' não existe.")
        return tabela[chave]

    @staticmethod
    def _garantir_novo(tabela, chave, entidade):
        """Verifica se uma chave ainda não está cadastrada na tabela.
        Args:
            tabela: Dicionário em que será feita a verificação.
            chave: Identificador que deverá ser exclusivo.
            entidade: Nome da entidade, usado na mensagem de erro.
        Raises:
            EntidadeDuplicadaError: Se a chave já existir na tabela."""
        if chave in tabela:
            raise EntidadeDuplicadaError(f"{entidade} '{chave}' já está cadastrado(a).")

    # Cadastros (RF01–RF05)
    def cadastrar_jurisdicao(self, nome):
        """Cadastra uma nova jurisdição no inventário.
        Args:
            nome: Nome que identificará a jurisdição.
        Returns:
            O objeto Jurisdicao criado.
        Raises:
            EntidadeDuplicadaError: Se já existir uma jurisdição com esse nome."""
        item = Jurisdicao(nome)
        self._garantir_novo(self.jurisdicoes, item.nome, "Jurisdição")
        self.jurisdicoes[item.nome] = item
        return item

    def cadastrar_local(self, id_local, endereco, jurisdicao):
        """Cadastra um local vinculado a uma jurisdição existente.
        Args:
            id_local: Identificador único do local.
            endereco: Endereço ou descrição do local.
            jurisdicao: Nome da jurisdição à qual o local pertence.
        Returns:
            O objeto Local criado.
        Raises:
            EntidadeInexistenteError: Se a jurisdição não estiver cadastrada.
            EntidadeDuplicadaError: Se o identificador do local já existir."""
        self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        item = Local(id_local, endereco, jurisdicao)
        self._garantir_novo(self.locais, item.id, "Local")
        self.locais[item.id] = item
        return item

    def cadastrar_ativo(
        self, id_ativo, tipo, jurisdicao=None, manutencao_pendente=False, local=None
    ):
        """Cadastra um ativo e, opcionalmente, vincula-o a uma jurisdição ou local.
        Quando um local é informado, a jurisdição é obtida automaticamente
        a partir desse local.
        Args:
            id_ativo: Identificador único do ativo.
            tipo: Categoria ou tipo do ativo.
            jurisdicao: Jurisdição do ativo; pode ser None.
            manutencao_pendente: Indica se há manutenção pendente.
            local: Identificador de um local; pode ser None.
        Returns:
            O objeto Ativo criado.
        Raises:
            EntidadeInexistenteError: Se o local ou a jurisdição não existir.
            EntidadeDuplicadaError: Se o identificador do ativo já existir."""
        if local is not None:
            jurisdicao = self._buscar(self.locais, local, "Local").jurisdicao
        if jurisdicao is not None:
            self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        item = Ativo(id_ativo, tipo, jurisdicao, manutencao_pendente, local)
        self._garantir_novo(self.ativos, item.id, "Ativo")
        self.ativos[item.id] = item
        return item

    def cadastrar_orgao(self, id_orgao, nome):
        """Cadastra um órgão no inventário.
        Args:
            id_orgao: Identificador único do órgão.
            nome: Nome do órgão.
        Returns:
            O objeto Orgao criado.
        Raises:
            EntidadeDuplicadaError: Se o identificador já estiver em uso."""
        item = Orgao(id_orgao, nome)
        self._garantir_novo(self.orgaos, item.id, "Órgão")
        self.orgaos[item.id] = item
        return item

    def cadastrar_permissao(self, nome):
        """Registra uma permissão disponível no sistema.
        O nome é removido de espaços nas extremidades e convertido para
        letras minúsculas antes do cadastro.
        Args:
            nome: Nome da permissão.
        Returns:
            O nome normalizado da permissão.
        Raises:
            PermissaoInvalidaError: Se o nome estiver vazio."""
        nome = nome.strip().lower()
        if not nome:
            raise PermissaoInvalidaError("Permissão não pode ser vazia.")
        self.permissoes.add(nome)
        return nome

    def cadastrar_papel(self, nome, permissoes=()):
        """Cadastra um papel com um conjunto de permissões existentes.
        Os nomes das permissões são normalizados antes da validação.
        Args:
            nome: Nome que identificará o papel.
            permissoes: Coleção de permissões que serão atribuídas ao papel.
        Returns:
            O objeto Papel criado.
        Raises:
            PermissaoInvalidaError: Se alguma permissão não estiver cadastrada.
            EntidadeDuplicadaError: Se já existir um papel com esse nome."""
        perms = {p.strip().lower() for p in permissoes}
        invalidas = cj.diferenca(perms, self.permissoes)
        if invalidas:
            raise PermissaoInvalidaError(f"Permissões inválidas: {sorted(invalidas)}")
        item = Papel(nome, perms)
        self._garantir_novo(self.papeis, item.nome, "Papel")
        self.papeis[item.nome] = item
        return item

    def cadastrar_usuario(
        self, id_usuario, nome, orgao=None, papeis=(), jurisdicao=None
    ):
        """Cadastra um usuário e valida seus vínculos opcionais.
        Args:
            id_usuario: Identificador único do usuário.
            nome: Nome do usuário.
            orgao: Identificador do órgão ao qual pertence; pode ser None.
            papeis: Coleção de nomes de papéis atribuídos ao usuário.
            jurisdicao: Nome da jurisdição do usuário; pode ser None.
        Returns:
            O objeto Usuario criado.
        Raises:
            EntidadeInexistenteError: Se algum órgão, papel ou jurisdição
                informado não estiver cadastrado.
            EntidadeDuplicadaError: Se o identificador do usuário já existir."""
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
        """Vincula um ativo a uma jurisdição existente.
        Args:
            id_ativo: Identificador do ativo.
            jurisdicao: Nome da jurisdição que será associada.
        Raises:
            EntidadeInexistenteError: Se o ativo ou a jurisdição não existir."""
        ativo = self._buscar(self.ativos, id_ativo, "Ativo")
        self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        ativo.jurisdicao = jurisdicao

    def associar_orgao_ativo(self, id_orgao, id_ativo):
        """Associa um ativo existente ao conjunto de ativos de um órgão.
        Args:
            id_orgao: Identificador do órgão.
            id_ativo: Identificador do ativo.
        Raises:
            EntidadeInexistenteError: Se o órgão ou o ativo não existir."""
        orgao = self._buscar(self.orgaos, id_orgao, "Órgão")
        self._buscar(self.ativos, id_ativo, "Ativo")
        orgao.ativos.add(id_ativo)

    def associar_permissao_papel(self, nome_papel, permissao):
        """Adiciona uma permissão existente a um papel.
        O nome da permissão é normalizado para letras minúsculas.
        Args:
            nome_papel: Nome do papel que receberá a permissão.
            permissao: Nome da permissão a ser associada.
        Raises:
            EntidadeInexistenteError: Se o papel não existir.
            PermissaoInvalidaError: Se a permissão não estiver cadastrada."""
        papel = self._buscar(self.papeis, nome_papel, "Papel")
        permissao = permissao.strip().lower()
        if permissao not in self.permissoes:
            raise PermissaoInvalidaError(f"Permissão '{permissao}' não existe.")
        papel.permissoes.add(permissao)

    def atribuir_papel(self, id_usuario, nome_papel):
        """Atribui um papel existente a um usuário.
        Args:
            id_usuario: Identificador do usuário.
            nome_papel: Nome do papel que será atribuído.
        Raises:
            EntidadeInexistenteError: Se o usuário ou o papel não existir."""
        usuario = self._buscar(self.usuarios, id_usuario, "Usuário")
        self._buscar(self.papeis, nome_papel, "Papel")
        usuario.papeis.add(nome_papel)

    def marcar_manutencao(self, id_ativo, pendente=True):
        """Define se um ativo está com manutenção pendente.
        Args:
            id_ativo: Identificador do ativo.
            pendente: Valor convertido para booleano que indica a pendência.
        Raises:
            EntidadeInexistenteError: Se o ativo não estiver cadastrado."""
        self._buscar(self.ativos, id_ativo, "Ativo").manutencao_pendente = bool(
            pendente
        )

    # Consultas por conjuntos (RF07)
    def universo_ativos(self):
        """Retorna o conjunto de identificadores de todos os ativos.
        Returns:
            Um set contendo as chaves cadastradas em self.ativos."""
        return set(self.ativos)

    def ativos_da_jurisdicao(self, jurisdicao):
        """Consulta os ativos vinculados a uma jurisdição.
        Args:
            jurisdicao: Nome da jurisdição consultada.
        Returns:
            Conjunto com os identificadores dos ativos dessa jurisdição.
        Raises:
            EntidadeInexistenteError: Se a jurisdição não existir."""
        self._buscar(self.jurisdicoes, jurisdicao, "Jurisdição")
        return {a.id for a in self.ativos.values() if a.jurisdicao == jurisdicao}

    def ativos_com_manutencao_pendente(self):
        """Retorna os identificadores dos ativos com manutenção pendente.
        Returns:
            Conjunto com os IDs dos ativos cujo indicador de manutenção
            pendente é verdadeiro."""
        return {a.id for a in self.ativos.values() if a.manutencao_pendente}

    def ativos_por_tipo(self, tipo):
        """Filtra os ativos pelo tipo informado.
        Args:
            tipo: Categoria que será usada como filtro.
        Returns:
            Conjunto com os identificadores dos ativos desse tipo."""
        return {a.id for a in self.ativos.values() if a.tipo == tipo}

    def ativos_do_orgao(self, id_orgao):
        """Retorna os ativos associados a um órgão.
        Args:
            id_orgao: Identificador do órgão consultado.
        Returns:
            Conjunto com os identificadores dos ativos associados.
        Raises:
            EntidadeInexistenteError: Se o órgão não existir."""
        return set(self._buscar(self.orgaos, id_orgao, "Órgão").ativos)

    def ativos_sem_jurisdicao(self):
        """Retorna os ativos que ainda não possuem jurisdição.
        Returns:
            Conjunto com os identificadores dos ativos cuja jurisdição é None."""
        return {a.id for a in self.ativos.values() if a.jurisdicao is None}

    def consulta_norte_pendente(self, jurisdicao="Norte"):
        """Compara os ativos da jurisdição com os que têm manutenção pendente.
        Args:
            jurisdicao: Jurisdição usada na consulta; por padrão, 'Norte'.
        Returns:
            Dicionário com os conjuntos A e B, sua interseção (A ∩ B),
            diferença (A − B) e união (A ∪ B)."""
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
        """Monta a relação entre usuários e órgãos.
        Returns:
            Conjunto de pares (ID do usuário, ID do órgão), ignorando
            usuários que não possuem órgão associado."""
        return {(u.id, u.orgao) for u in self.usuarios.values() if u.orgao is not None}

    def relacao_orgao_ativo(self):
        """Monta a relação entre órgãos e ativos associados.
        Returns:
            Conjunto de pares (ID do órgão, ID do ativo)."""
        return {(o.id, ativo) for o in self.orgaos.values() for ativo in o.ativos}

    def relacao_usuario_papel(self):
        """Monta a relação entre usuários e seus papéis.
        Returns:
            Conjunto de pares (ID do usuário, nome do papel)."""
        return {(u.id, papel) for u in self.usuarios.values() for papel in u.papeis}

    def relacao_papel_permissao(self):
        """Monta a relação entre papéis e permissões.
        Returns:
            Conjunto de pares (nome do papel, nome da permissão)."""
        return {(p.nome, perm) for p in self.papeis.values() for perm in p.permissoes}

    def relacao_ativo_jurisdicao(self):
        """Monta a relação entre ativos e suas jurisdições.
        Returns:
            Conjunto de pares (ID do ativo, jurisdição), excluindo ativos
            que ainda não possuem jurisdição."""
        return {
            (a.id, a.jurisdicao)
            for a in self.ativos.values()
            if a.jurisdicao is not None
        }

    def ativos_que_usuario_gerencia(self, id_usuario):
        """Identifica os ativos que um usuário gerencia indiretamente.
        A consulta compõe a relação usuário–órgão com a relação órgão–ativo.
        Args:
            id_usuario: Identificador do usuário consultado.
        Returns:
            Conjunto de IDs dos ativos vinculados aos órgãos do usuário.
        Raises:
            EntidadeInexistenteError: Se o usuário não existir."""
        self._buscar(self.usuarios, id_usuario, "Usuário")
        relacao = cj.composicao_indexada(
            self.relacao_usuario_orgao(), self.relacao_orgao_ativo()
        )
        return cj.imagem(relacao, id_usuario)

    # Validações (RF09)
    def validar_mapeamento_ativo_jurisdicao(self):
        """Verifica se a relação ativo–jurisdição representa uma função.
        Returns:
            Resultado produzido por cj.eh_funcao: indicador booleano e
            conjunto de possíveis problemas encontrados."""
        return cj.eh_funcao(self.relacao_ativo_jurisdicao(), self.universo_ativos())

    def exigir_jurisdicao(self, id_ativo):
        """Obtém a jurisdição de um ativo e exige que ela esteja definida.
        Args:
            id_ativo: Identificador do ativo consultado.
        Returns:
            Nome da jurisdição associada ao ativo.
        Raises:
            EntidadeInexistenteError: Se o ativo não existir.
            AtivoSemJurisdicaoError: Se o ativo não possuir jurisdição."""
        ativo = self._buscar(self.ativos, id_ativo, "Ativo")
        if ativo.jurisdicao is None:
            raise AtivoSemJurisdicaoError(f"Ativo '{id_ativo}' não possui jurisdição.")
        return ativo.jurisdicao

    # Controle de acesso por papéis (RF10)
    def permissoes_do_usuario(self, id_usuario):
        """Calcula todas as permissões herdadas pelos papéis do usuário.
        Args:
            id_usuario: Identificador do usuário consultado.
        Returns:
            União dos conjuntos de permissões de todos os papéis do usuário.
        Raises:
            EntidadeInexistenteError: Se o usuário ou algum papel atribuído
                não existir."""
        usuario = self._buscar(self.usuarios, id_usuario, "Usuário")
        resultado = set()
        for nome in usuario.papeis:
            papel = self._buscar(self.papeis, nome, "Papel")
            resultado = cj.uniao(resultado, papel.permissoes)
        return resultado

    def tem_permissao(self, id_usuario, permissao):
        """Verifica se um usuário possui uma permissão específica.
        Args:
            id_usuario: Identificador do usuário.
            permissao: Nome da permissão que será verificada.
        Returns:
            True se o usuário possuir a permissão; caso contrário, False.
        Raises:
            PermissaoInvalidaError: Se a permissão não estiver cadastrada.
            EntidadeInexistenteError: Se o usuário ou algum de seus papéis
                não existir."""
        permissao = permissao.strip().lower()
        if permissao not in self.permissoes:
            raise PermissaoInvalidaError(f"Permissão '{permissao}' não existe.")
        return permissao in self.permissoes_do_usuario(id_usuario)

    def exigir_permissao(self, id_usuario, permissao):
        """Exige que o usuário possua a permissão informada.
        Args:
            id_usuario: Identificador do usuário.
            permissao: Permissão necessária para continuar a operação.
        Returns:
            True quando o usuário possui a permissão exigida.
        Raises:
            AcessoNegadoError: Se o usuário não possuir a permissão.
            PermissaoInvalidaError: Se a permissão não existir.
            EntidadeInexistenteError: Se o usuário não existir."""
        if not self.tem_permissao(id_usuario, permissao):
            nome = self.usuarios[id_usuario].nome
            raise AcessoNegadoError(
                f"Acesso negado: {nome} não tem permissão '{permissao}'."
            )
        return True

    def excluir_ativo(self, id_usuario, id_ativo):
        """Exclui um ativo após verificar a permissão do usuário.
        Além de remover o ativo do inventário, remove seu identificador
        dos conjuntos de ativos associados aos órgãos.
        Args:
            id_usuario: Usuário que está solicitando a exclusão.
            id_ativo: Identificador do ativo que será excluído.
        Raises:
            AcessoNegadoError: Se o usuário não tiver a permissão 'excluir'.
            EntidadeInexistenteError: Se o usuário, papel ou ativo não existir."""
        self.exigir_permissao(id_usuario, "excluir")
        self._buscar(self.ativos, id_ativo, "Ativo")
        del self.ativos[id_ativo]
        for orgao in self.orgaos.values():
            orgao.ativos.discard(id_ativo)

    # Matriz e relatório (RF11)
    def matriz_jurisdicao_ativo(self):
        """Gera a matriz de pertencimento entre jurisdições e ativos.
        As jurisdições formam os conjuntos/linhas e os ativos ordenados
        naturalmente formam as colunas.
        Returns:
            Estrutura retornada por cj.matriz_pertencimento, contendo a
            matriz e os respectivos rótulos."""
        conjuntos = {j: self.ativos_da_jurisdicao(j) for j in self.jurisdicoes}
        colunas = sorted(self.ativos, key=_ordem_natural)
        return cj.matriz_pertencimento(conjuntos, colunas)

    def relatorio(self):
        """Gera um relatório textual com o resumo do inventário.
        O relatório apresenta totais, ativos por jurisdição, pendências,
        ativos sem jurisdição, validação do mapeamento e matriz de
        pertencimento.
        Returns:
            Uma única string contendo o relatório formatado."""
        linhas = [
            "=" * 50,
            "RELATÓRIO URBANINVENTORY",
            "=" * 50,
            f"Total de ativos: {len(self.ativos)}",
            (
                f"Jurisdições: {len(self.jurisdicoes)} | "
                f"Órgãos: {len(self.orgaos)} | Usuários: {len(self.usuarios)} | "
                f"Papéis: {len(self.papeis)}"
            ),
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
        linhas.extend(
            [
                f"Ativo → Jurisdição é função? {status}",
                "",
                "Matriz de pertencimento:",
                cj.formatar_matriz(*self.matriz_jurisdicao_ativo()),
            ]
        )
        return "\n".join(linhas)


def _ordem_natural(texto):
    """Gera uma chave de ordenação natural para identificadores.
    Separa o prefixo textual do sufixo numérico para que, por exemplo,
    'A2' seja ordenado antes de 'A10'.
    Args:
        texto: Identificador que será separado.
    Returns:
        Tupla formada pelo prefixo e pelo número convertido para inteiro."""
    prefixo = texto.rstrip("0123456789")
    numero = texto[len(prefixo) :]
    return prefixo, int(numero) if numero else 0


def _fmt(conjunto):
    """Formata um conjunto de identificadores em ordem natural.
    Args:
        conjunto: Conjunto de identificadores que será exibido.
    Returns:
        '∅' quando o conjunto estiver vazio ou uma representação entre
        chaves com os elementos separados por vírgula."""
    return (
        "∅"
        if not conjunto
        else "{" + ", ".join(sorted(conjunto, key=_ordem_natural)) + "}"
    )

"""UrbanInventory — interface de terminal (CLI / menu de demonstração).

Execute com:  python app.py
"""

from src.algorithms import conjuntos as cj
import os

from src.data.carregador import carregar_csv, exportar_ativos_csv
from src.data.dados_exemplo import carregar_exemplo
from src.services.inventario import _fmt
from src.utils.excecoes import UrbanInventoryError

MENU = """
==================== URBANINVENTORY ====================
 1. Cadastrar ativo
 2. Cadastrar localização
 3. Cadastrar usuário
 4. Cadastrar papel
 5. Cadastrar permissão
 6. Consultar ativos
 7. Consultar conjuntos (∪, ∩, −, disjuntos)
 8. Consultar relações
 9. Validar acesso (RBAC)
10. Gerar relatório
11. Associar ativo à jurisdição
12. Matriz de pertencimento
13. Exportar ativos para CSV
 0. Sair
========================================================"""


def perguntar(texto, obrigatorio=True):
    """Lê uma entrada do teclado. Campos opcionais podem ficar vazios."""
    while True:
        valor = input(f"{texto}: ").strip()
        if valor or not obrigatorio:
            return valor or None
        print("  Campo obrigatório.")


def lista(texto):
    """Lê uma lista separada por vírgulas."""
    valor = input(f"{texto} (separe por vírgula): ").strip()
    return [v.strip() for v in valor.split(",") if v.strip()]


# --------------------------------------------------------------------- ações

def cadastrar_ativo(inv):
    """RF01 — Pede os dados e cadastra um ativo."""
    id_a = perguntar("ID do ativo (ex.: A11)")
    tipo = perguntar("Tipo (poste, semaforo, abrigo...)")
    print(f"  Jurisdições: {', '.join(inv.jurisdicoes)}")
    jur = perguntar("Jurisdição (Enter para deixar sem)", obrigatorio=False)
    pend = perguntar("Manutenção pendente? (s/n)").lower() == "s"
    inv.cadastrar_ativo(id_a, tipo, jur, pend)
    print(f"  ✔ Ativo {id_a} cadastrado.")


def cadastrar_local(inv):
    """RF02 — Pede os dados e cadastra uma localização."""
    id_l = perguntar("ID do local (ex.: L4)")
    end = perguntar("Endereço")
    jur = perguntar(f"Jurisdição ({', '.join(inv.jurisdicoes)})")
    inv.cadastrar_local(id_l, end, jur)
    print(f"  ✔ Local {id_l} cadastrado.")


def cadastrar_usuario(inv):
    """RF03 — Pede os dados e cadastra um usuário."""
    id_u = perguntar("ID do usuário (ex.: U004)")
    nome = perguntar("Nome")
    print(f"  Órgãos: {', '.join(f'{o.id}={o.nome}' for o in inv.orgaos.values())}")
    orgao = perguntar("Órgão (Enter para nenhum)", obrigatorio=False)
    print(f"  Papéis: {', '.join(inv.papeis)}")
    papeis = lista("Papéis")
    jur = perguntar("Jurisdição (Enter para nenhuma)", obrigatorio=False)
    inv.cadastrar_usuario(id_u, nome, orgao, papeis, jur)
    print(f"  ✔ Usuário {nome} cadastrado.")


def cadastrar_papel(inv):
    """RF04 — Cadastra um papel com suas permissões."""
    nome = perguntar("Nome do papel")
    print(f"  Permissões existentes: {_fmt(inv.permissoes)}")
    perms = lista("Permissões do papel")
    inv.cadastrar_papel(nome, perms)
    print(f"  ✔ Papel {nome} cadastrado.")


def cadastrar_permissao(inv):
    """RF05 — Adiciona uma permissão ao universo P."""
    nome = inv.cadastrar_permissao(perguntar("Nome da permissão"))
    print(f"  ✔ Permissão '{nome}' cadastrada. P = {_fmt(inv.permissoes)}")


def consultar_ativos(inv):
    """RF07 — Lista todos os ativos em forma de tabela."""
    print("\n  ID    TIPO       JURISDIÇÃO  MANUTENÇÃO")
    for a in sorted(inv.ativos.values(),
                    key=lambda x: (len(x.id), x.id)):
        print(f"  {a.id:<5} {a.tipo:<10} {str(a.jurisdicao or '—'):<11} "
              f"{'PENDENTE' if a.manutencao_pendente else 'ok'}")


def escolher_conjunto(inv, rotulo):
    """Submenu: deixa o usuário escolher qual conjunto montar."""
    print(f"\n  Escolha o conjunto {rotulo}:")
    print("   1. Ativos de uma jurisdição")
    print("   2. Ativos com manutenção pendente")
    print("   3. Ativos de um tipo")
    print("   4. Ativos de um órgão")
    print("   5. Ativos sem jurisdição")
    op = perguntar("  Opção")
    if op == "1":
        j = perguntar(f"  Jurisdição ({', '.join(inv.jurisdicoes)})")
        return f"Ativos({j})", inv.ativos_da_jurisdicao(j)
    if op == "2":
        return "Pendentes", inv.ativos_com_manutencao_pendente()
    if op == "3":
        t = perguntar("  Tipo")
        return f"Tipo({t})", inv.ativos_por_tipo(t)
    if op == "4":
        o = perguntar("  ID do órgão")
        return f"Órgão({o})", inv.ativos_do_orgao(o)
    if op == "5":
        return "SemJurisdição", inv.ativos_sem_jurisdicao()
    raise UrbanInventoryError("Opção de conjunto inválida.")


def consultar_conjuntos(inv):
    """RF07 — Mostra o exemplo do enunciado e consultas livres A x B."""
    print("\n  Exemplo do enunciado: A = Zona Norte, B = manutenção pendente")
    for nome, valor in inv.consulta_norte_pendente("Norte").items():
        print(f"   {nome:<6} = {_fmt(valor)}")

    if perguntar("\n  Montar sua própria consulta? (s/n)").lower() != "s":
        return
    na, a = escolher_conjunto(inv, "A")
    nb, b = escolher_conjunto(inv, "B")
    print(f"\n  A = {na} = {_fmt(a)}")
    print(f"  B = {nb} = {_fmt(b)}")
    print(f"  A ∪ B = {_fmt(cj.uniao(a, b))}")
    print(f"  A ∩ B = {_fmt(cj.intersecao(a, b))}")
    print(f"  A − B = {_fmt(cj.diferenca(a, b))}")
    print(f"  B − A = {_fmt(cj.diferenca(b, a))}")
    print(f"  A Δ B = {_fmt(cj.diferenca_simetrica(a, b))}")
    print(f"  A é vazio? {'sim' if cj.eh_vazio(a) else 'não'}")
    print(f"  A e B são disjuntos? {'sim' if cj.sao_disjuntos(a, b) else 'não'}")
    print(f"  A ⊆ B? {'sim' if cj.eh_subconjunto(a, b) else 'não'}")


def consultar_relacoes(inv):
    """RF08 — Exibe as quatro relações e a composição Usuário→Ativo."""
    def mostrar(titulo, rel):
        """Imprime uma relação como lista de pares."""
        pares = sorted(rel)
        print(f"\n  {titulo}  (|R| = {len(pares)})")
        print("   " + ", ".join(f"({x}, {y})" for x, y in pares) if pares
              else "   ∅")

    mostrar("Usuário → pertence → Órgão", inv.relacao_usuario_orgao())
    mostrar("Órgão → administra → Ativo", inv.relacao_orgao_ativo())
    mostrar("Usuário → possui → Papel", inv.relacao_usuario_papel())
    mostrar("Papel → possui → Permissão", inv.relacao_papel_permissao())

    print("\n  Composição Usuário → Órgão → Ativo (quem gerencia o quê):")
    for u in inv.usuarios.values():
        print(f"   {u.nome:<6} → {_fmt(inv.ativos_que_usuario_gerencia(u.id))}")


def validar_acesso(inv):
    """RF10 — Verifica se um usuário pode executar uma ação (RBAC)."""
    for u in inv.usuarios.values():
        print(f"   {u.id} {u.nome:<6} papéis={_fmt(u.papeis)} "
              f"permissões={_fmt(inv.permissoes_do_usuario(u.id))}")
    id_u = perguntar("\n  ID do usuário")
    acao = perguntar(f"  Ação ({', '.join(sorted(inv.permissoes))})")
    nome = inv.usuarios[id_u].nome if id_u in inv.usuarios else id_u
    if inv.tem_permissao(id_u, acao):
        print(f"  ✔ ACESSO AUTORIZADO: {nome} pode '{acao}'.")
    else:
        print(f"  ✘ ACESSO NEGADO: {nome} não pode '{acao}'.")


def associar_jurisdicao(inv):
    """RF06 — Associa um ativo a uma jurisdição."""
    sem = inv.ativos_sem_jurisdicao()
    print(f"  Ativos sem jurisdição: {_fmt(sem)}")
    id_a = perguntar("ID do ativo")
    jur = perguntar(f"Jurisdição ({', '.join(inv.jurisdicoes)})")
    inv.associar_ativo_jurisdicao(id_a, jur)
    print(f"  ✔ {id_a} agora pertence a {jur}.")


def mostrar_matriz(inv):
    """Exibe a matriz de pertencimento Jurisdição x Ativo."""
    print()
    print(cj.formatar_matriz(*inv.matriz_jurisdicao_ativo()))


def exportar(inv):
    """RF11 — Salva os ativos em data/processed/ativos.csv."""
    caminho = os.path.join("data", "processed", "ativos.csv")
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    exportar_ativos_csv(inv, caminho)
    print(f"  ✔ Ativos salvos em {caminho}")


ACOES = {
    "1": cadastrar_ativo, "2": cadastrar_local, "3": cadastrar_usuario,
    "4": cadastrar_papel, "5": cadastrar_permissao, "6": consultar_ativos,
    "7": consultar_conjuntos, "8": consultar_relacoes, "9": validar_acesso,
    "10": lambda inv: print(inv.relatorio()),
    "11": associar_jurisdicao, "12": mostrar_matriz, "13": exportar,
}


def main():
    """Carrega os dados e executa o laço do menu."""
    try:
        inv = carregar_csv()
        origem = "data/raw/*.csv"
    except UrbanInventoryError as erro:
        print(f"Aviso: {erro}. Usando dados embutidos.")
        inv = carregar_exemplo()
        origem = "dados_exemplo.py"
    print(f"Dados carregados de {origem}: "
          f"{len(inv.ativos)} ativos, {len(inv.usuarios)} usuários.")
    while True:
        print(MENU)
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        acao = ACOES.get(opcao)
        if acao is None:
            print("  Opção inválida.")
            continue
        try:
            acao(inv)
        except UrbanInventoryError as erro:
            print(f"  ✘ Erro: {erro}")
        input("\n[Enter para continuar]")


if __name__ == "__main__":
    main()
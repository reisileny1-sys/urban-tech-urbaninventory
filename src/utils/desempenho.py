"""Sprint 4 — Desempenho: tempo, memória, cProfile e gráficos.

Responde à pergunta do projeto: "Como nosso algoritmo se comporta quando o
tamanho do problema aumenta?"

Execute a partir da raiz do projeto:
    python -m src.utils.desempenho

Usa só biblioteca padrão: time, tracemalloc, cProfile, pstats, csv.
Se o matplotlib estiver instalado, também gera PNGs (opcional).
"""

import cProfile
import csv
import io
import os
import pstats
import time
import tracemalloc

from src.algorithms import conjuntos as cj
from src.data.gerador_inventario import gerar_inventario
from src.utils.grafico_svg import grafico_linhas

RAIZ = os.path.join(os.path.dirname(__file__), "..", "..")
PASTA_COMPLEXIDADE = os.path.join(RAIZ, "reports", "complexity")
PASTA_PROFILING = os.path.join(RAIZ, "reports", "profiling")
PASTA_FIGURAS = os.path.join(RAIZ, "reports", "figures")

TAMANHOS = [1_000, 5_000, 10_000, 25_000, 50_000, 75_000, 100_000]
TAMANHOS_QUADRATICOS = [500, 1_000, 2_000, 3_000, 4_000, 5_000]


def cronometrar(funcao, repeticoes=5):
    """Executa a função várias vezes e devolve o MENOR tempo, em ms.

    O menor tempo é o mais confiável: os outros incluem ruído do sistema.
    """
    melhor = float("inf")
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao()
        melhor = min(melhor, time.perf_counter() - inicio)
    return melhor * 1000


def intersecao_com_listas(a, b):
    """Versão ingênua de A ∩ B com listas: O(n · m). Só para comparação."""
    return [x for x in a if x in b]


def experimento_tempo():
    """Mede o tempo das operações principais para vários tamanhos n."""
    linhas = []
    for n in TAMANHOS:
        inv = gerar_inventario(n)
        a = inv.ativos_da_jurisdicao("Norte")
        b = inv.ativos_com_manutencao_pendente()
        usuario = next(iter(inv.usuarios))
        linhas.append({
            "n": n,
            "|A|": len(a),
            "|B|": len(b),
            "uniao_ms": cronometrar(lambda: cj.uniao(a, b)),
            "intersecao_ms": cronometrar(lambda: cj.intersecao(a, b)),
            "diferenca_ms": cronometrar(lambda: cj.diferenca(a, b)),
            "filtrar_jurisdicao_ms": cronometrar(
                lambda: inv.ativos_da_jurisdicao("Norte")),
            "matriz_ms": cronometrar(inv.matriz_jurisdicao_ativo, 3),
            "rbac_tem_permissao_ms": cronometrar(
                lambda: inv.tem_permissao(usuario, "excluir"), 50),
        })
        print(f"  n={n:>7}: ok")
    return linhas


def experimento_quadratico():
    """Compara set (hash) x lista e mede a composição de relações."""
    linhas = []
    for n in TAMANHOS_QUADRATICOS:
        inv = gerar_inventario(n)
        a = inv.ativos_da_jurisdicao("Norte")
        b = inv.ativos_com_manutencao_pendente()
        la, lb = list(a), list(b)
        r1, r2 = inv.relacao_usuario_orgao(), inv.relacao_orgao_ativo()
        linhas.append({
            "n": n,
            "intersecao_set_ms": cronometrar(lambda: cj.intersecao(a, b)),
            "intersecao_lista_ms": cronometrar(
                lambda: intersecao_com_listas(la, lb), 3),
            "composicao_ms": cronometrar(lambda: cj.composicao(r1, r2), 3),
            "composicao_indexada_ms": cronometrar(
                lambda: cj.composicao_indexada(r1, r2), 3),
        })
        print(f"  n={n:>7}: ok")
    return linhas


def experimento_memoria():
    """Mede o pico de memória para construir o inventário (tracemalloc)."""
    linhas = []
    for n in TAMANHOS:
        tracemalloc.start()
        inv = gerar_inventario(n)
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        linhas.append({"n": n, "pico_mb": pico / 1024 / 1024,
                       "bytes_por_ativo": pico / n})
        del inv
    return linhas


def experimento_profiling(n=50_000):
    """Roda uma carga típica com cProfile e salva as funções mais caras."""
    inv = gerar_inventario(n)
    perfil = cProfile.Profile()
    perfil.enable()
    for j in inv.jurisdicoes:
        inv.consulta_norte_pendente(j)
    inv.matriz_jurisdicao_ativo()
    inv.validar_mapeamento_ativo_jurisdicao()
    for u in list(inv.usuarios)[:200]:
        inv.tem_permissao(u, "atualizar")
    inv.relatorio()
    perfil.disable()

    saida = io.StringIO()
    stats = pstats.Stats(perfil, stream=saida)
    stats.strip_dirs().sort_stats("cumulative").print_stats(15)
    caminho = os.path.join(PASTA_PROFILING, "profile_cumulative.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"cProfile — carga típica com n = {n} ativos\n\n")
        f.write(saida.getvalue())
    stats.dump_stats(os.path.join(PASTA_PROFILING, "profile.prof"))
    return caminho


def salvar_csv(linhas, caminho):
    """Salva uma lista de dicionários em CSV."""
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        for linha in linhas:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v)
                        for k, v in linha.items()})


def tabela_markdown(linhas):
    """Converte os resultados em uma tabela Markdown."""
    cab = list(linhas[0])
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for linha in linhas:
        out.append("| " + " | ".join(
            f"{linha[c]:.3f}" if isinstance(linha[c], float) else str(linha[c])
            for c in cab) + " |")
    return "\n".join(out)


def gerar_graficos(tempo, quad, memoria):
    """Gera os gráficos em SVG (e PNG, se o matplotlib existir)."""
    s1 = {
        "União A ∪ B": [(l["n"], l["uniao_ms"]) for l in tempo],
        "Interseção A ∩ B": [(l["n"], l["intersecao_ms"]) for l in tempo],
        "Diferença A − B": [(l["n"], l["diferenca_ms"]) for l in tempo],
    }
    s2 = {
        "Filtrar jurisdição": [(l["n"], l["filtrar_jurisdicao_ms"])
                               for l in tempo],
        "Matriz (k·n)": [(l["n"], l["matriz_ms"]) for l in tempo],
    }
    s3 = {
        "Interseção com set": [(l["n"], l["intersecao_set_ms"]) for l in quad],
        "Interseção com lista": [(l["n"], l["intersecao_lista_ms"])
                                 for l in quad],
    }
    s4 = {"Composição ingênua": [(l["n"], l["composicao_ms"]) for l in quad],
          "Composição indexada": [(l["n"], l["composicao_indexada_ms"])
                                  for l in quad]}
    s5 = {"Pico de memória": [(l["n"], l["pico_mb"]) for l in memoria]}

    graficos = [
        (s1, "conjuntos", "Operações de conjuntos — O(n)", "tempo (ms)"),
        (s2, "filtro_matriz", "Filtro O(n) x Matriz O(k·n)", "tempo (ms)"),
        (s3, "set_vs_lista", "Interseção: set O(n) x lista O(n·m)",
         "tempo (ms)"),
        (s4, "composicao", "Composição: O(|R|·|S|) x indexada O(|R|+|S|)",
         "tempo (ms)"),
        (s5, "memoria", "Pico de memória — O(n)", "memória (MB)"),
    ]
    arquivos = [grafico_linhas(series, os.path.join(PASTA_FIGURAS,
                                                    f"{nome}.svg"),
                               titulo, "n (nº de ativos)", ylabel)
                for series, nome, titulo, ylabel in graficos]

    try:  # opcional: o documento pede matplotlib, mas não é obrigatório aqui
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        for series, nome, titulo, ylabel in graficos:
            plt.figure(figsize=(8, 5))
            for rotulo, pts in series.items():
                plt.plot([p[0] for p in pts], [p[1] for p in pts], "o-",
                         label=rotulo)
            plt.title(titulo)
            plt.xlabel("n (nº de ativos)")
            plt.ylabel(ylabel)
            plt.legend()
            plt.grid(alpha=0.3)
            caminho = os.path.join(PASTA_FIGURAS, f"{nome}.png")
            plt.savefig(caminho, dpi=120, bbox_inches="tight")
            plt.close()
            arquivos.append(caminho)
    except ImportError:
        print("  (matplotlib não instalado: gerados só os SVGs)")
    return arquivos


def main():
    """Executa todos os experimentos e salva os relatórios."""
    for pasta in (PASTA_COMPLEXIDADE, PASTA_PROFILING, PASTA_FIGURAS):
        os.makedirs(pasta, exist_ok=True)

    print("1/4 Tempo das operações...")
    tempo = experimento_tempo()
    print("2/4 Set x lista e composição...")
    quad = experimento_quadratico()
    print("3/4 Memória...")
    memoria = experimento_memoria()
    print("4/4 cProfile...")
    perfil = experimento_profiling()

    salvar_csv(tempo, os.path.join(PASTA_COMPLEXIDADE, "tempo.csv"))
    salvar_csv(quad, os.path.join(PASTA_COMPLEXIDADE, "set_vs_lista.csv"))
    salvar_csv(memoria, os.path.join(PASTA_COMPLEXIDADE, "memoria.csv"))
    with open(os.path.join(PASTA_COMPLEXIDADE, "resultados.md"), "w",
              encoding="utf-8") as f:
        f.write("# Resultados medidos\n\n## Tempo (ms)\n\n")
        f.write(tabela_markdown(tempo))
        f.write("\n\n## Set x lista e composição (ms)\n\n")
        f.write(tabela_markdown(quad))
        f.write("\n\n## Memória\n\n")
        f.write(tabela_markdown(memoria))
        f.write("\n")

    arquivos = gerar_graficos(tempo, quad, memoria)
    print("\nPronto! Arquivos gerados:")
    for a in arquivos + [perfil]:
        print("  ", os.path.relpath(a, RAIZ))


if __name__ == "__main__":
    main()

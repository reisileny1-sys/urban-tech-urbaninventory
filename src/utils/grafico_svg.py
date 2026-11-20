"""Gráfico de linhas em SVG feito só com Python puro (sem matplotlib).

Gera um arquivo .svg que abre em qualquer navegador.
"""

CORES = ("#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c", "#0891b2",
         "#4b5563")


def _escala(v, v_min, v_max, p_min, p_max):
    if v_max == v_min:
        return (p_min + p_max) / 2
    return p_min + (v - v_min) * (p_max - p_min) / (v_max - v_min)


def _ticks(v_max, n=5):
    passo = v_max / n if v_max else 1
    return [passo * i for i in range(n + 1)]


def _fmt(v):
    if v == 0:
        return "0"
    if v >= 1000:
        return f"{v / 1000:.0f}k" if v % 1000 == 0 else f"{v / 1000:.1f}k"
    if v >= 10:
        return f"{v:.0f}"
    if v >= 1:
        return f"{v:.1f}"
    return f"{v:.2f}"


def grafico_linhas(series, caminho, titulo, rotulo_x, rotulo_y,
                   largura=760, altura=440):
    """Desenha um gráfico de linhas.

    Args:
        series: dict {nome: [(x, y), ...]}.
        caminho: arquivo .svg de saída.
    """
    m_esq, m_dir, m_top, m_base = 70, 190, 50, 60
    x0, x1 = m_esq, largura - m_dir
    y0, y1 = altura - m_base, m_top
    xs = [x for pts in series.values() for x, _ in pts]
    ys = [y for pts in series.values() for _, y in pts]
    x_max, y_max = max(xs), max(ys) * 1.05

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" '
           f'height="{altura}" font-family="Arial, sans-serif" font-size="12">',
           f'<rect width="100%" height="100%" fill="white"/>',
           f'<text x="{largura / 2 - m_dir / 2 + m_esq / 2}" y="28" '
           f'text-anchor="middle" font-size="16" font-weight="bold">'
           f'{titulo}</text>']

    for t in _ticks(y_max):
        y = _escala(t, 0, y_max, y0, y1)
        svg.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" '
                   f'stroke="#e5e7eb"/>')
        svg.append(f'<text x="{x0 - 8}" y="{y + 4:.1f}" text-anchor="end" '
                   f'fill="#374151">{_fmt(t)}</text>')
    for t in _ticks(x_max):
        x = _escala(t, 0, x_max, x0, x1)
        svg.append(f'<text x="{x:.1f}" y="{y0 + 18}" text-anchor="middle" '
                   f'fill="#374151">{_fmt(t)}</text>')
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" '
               f'stroke="#111827"/>')
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" '
               f'stroke="#111827"/>')
    svg.append(f'<text x="{(x0 + x1) / 2}" y="{altura - 18}" '
               f'text-anchor="middle">{rotulo_x}</text>')
    svg.append(f'<text x="18" y="{(y0 + y1) / 2}" text-anchor="middle" '
               f'transform="rotate(-90 18 {(y0 + y1) / 2})">{rotulo_y}</text>')

    for i, (nome, pts) in enumerate(series.items()):
        cor = CORES[i % len(CORES)]
        coords = " ".join(f"{_escala(x, 0, x_max, x0, x1):.1f},"
                          f"{_escala(y, 0, y_max, y0, y1):.1f}"
                          for x, y in pts)
        svg.append(f'<polyline points="{coords}" fill="none" stroke="{cor}" '
                   f'stroke-width="2"/>')
        for x, y in pts:
            svg.append(f'<circle cx="{_escala(x, 0, x_max, x0, x1):.1f}" '
                       f'cy="{_escala(y, 0, y_max, y0, y1):.1f}" r="3" '
                       f'fill="{cor}"/>')
        ly = m_top + 10 + i * 22
        svg.append(f'<line x1="{x1 + 15}" y1="{ly}" x2="{x1 + 35}" y2="{ly}" '
                   f'stroke="{cor}" stroke-width="3"/>')
        svg.append(f'<text x="{x1 + 42}" y="{ly + 4}">{nome}</text>')

    svg.append("</svg>")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    return caminho

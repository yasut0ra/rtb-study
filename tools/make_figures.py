"""本書の図版（SVG）を生成するスクリプト。

すべての図を同じ配色・書体・線幅で描くために、図はこのスクリプトから生成します。
図を直したいときは、SVG を直接編集せずにこのファイルを編集して再実行してください。

    python tools/make_figures.py

出力先: docs/images/fig-*.svg
"""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"

FONT = "'Noto Sans JP','Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','Meiryo',sans-serif"

# 配色（役割ごとに固定）
INK, MUTED, LINE, PAPER = "#1e293b", "#64748b", "#cbd5e1", "#ffffff"
ROLE = {
    "buy": ("#eef2ff", "#4f46e5", "#312e81"),  # 買い手側（DSP・広告主）
    "sell": ("#ecfdf5", "#059669", "#064e3b"),  # 売り手側（SSP・媒体社）
    "market": ("#fffbeb", "#d97706", "#78350f"),  # 取引所・オークション
    "user": ("#f1f5f9", "#475569", "#0f172a"),  # ユーザー・中立
    "alert": ("#fef2f2", "#dc2626", "#7f1d1d"),  # 注意・不正
    "good": ("#f0fdf4", "#16a34a", "#14532d"),  # 成功・収益
}
ACCENT = {"buy": "#4f46e5", "sell": "#059669", "market": "#d97706", "alert": "#dc2626", "good": "#16a34a"}


# ---------------------------------------------------------------- primitives
def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w: int, h: int, body: list[str], title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(title)}" font-family="{FONT}">\n'
        f"<title>{esc(title)}</title>\n"
        "<defs>\n"
        + "".join(
            f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>\n'
            for k, c in {"ink": INK, "muted": MUTED, **ACCENT}.items()
        )
        + "</defs>\n"
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{PAPER}" stroke="#e2e8f0"/>\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )


def text(x, y, s, size=14, color=INK, anchor="middle", weight=400, extra=""):
    lines = s.split("\n")
    if len(lines) == 1:
        return (
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'font-weight="{weight}" dominant-baseline="middle" {extra}>{esc(s)}</text>'
        )
    lh = size * 1.35
    y0 = y - lh * (len(lines) - 1) / 2
    spans = "".join(
        f'<tspan x="{x}" y="{y0 + i * lh:.1f}">{esc(t)}</tspan>' for i, t in enumerate(lines)
    )
    return (
        f'<text font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}" '
        f'dominant-baseline="middle" {extra}>{spans}</text>'
    )


def box(x, y, w, h, label, role="user", size=14, sub=None, dashed=False, weight=700, rx=10):
    fill, stroke, ink = ROLE[role]
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>']
    if sub:
        out.append(text(x + w / 2, y + h / 2 - size * 0.55, label, size, ink, weight=weight))
        out.append(text(x + w / 2, y + h / 2 + size * 0.75, sub, size - 2, ink))
    else:
        out.append(text(x + w / 2, y + h / 2, label, size, ink, weight=weight))
    return "\n".join(out)


def arrow(x1, y1, x2, y2, color="ink", width=2, dashed=False, both=False):
    c = {"ink": INK, "muted": MUTED, **ACCENT}[color]
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    start = f' marker-start="url(#ah-{color})"' if both else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{width}"{dash}'
        f'{start} marker-end="url(#ah-{color})"/>'
    )


def path_arrow(d, color="ink", width=2, dashed=False):
    c = {"ink": INK, "muted": MUTED, **ACCENT}[color]
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}"{dash} marker-end="url(#ah-{color})"/>'


def label_tag(x, y, s, role="market", size=12):
    fill, stroke, ink = ROLE[role]
    w = sum(size if ord(ch) > 0x2000 else size * 0.6 for ch in s) + 16
    return (
        f'<rect x="{x - w/2:.1f}" y="{y - size}" width="{w:.1f}" height="{size*2}" rx="{size}" fill="{fill}" stroke="{stroke}"/>'
        + text(x, y, s, size, ink, weight=700)
    )


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- figures
def fig_ecosystem():
    W, H = 760, 340
    b = []
    # グループ見出し
    b.append(text(160, 34, "買い手側（Buy Side）", 13, ROLE["buy"][2], weight=700))
    b.append(text(380, 34, "取引所", 13, ROLE["market"][2], weight=700))
    b.append(text(600, 34, "売り手側（Sell Side）", 13, ROLE["sell"][2], weight=700))
    # お金の流れ
    b.append(arrow(70, 66, 690, 66, "good", 2))
    b.append(label_tag(380, 66, "お金（広告費）の流れ", "good"))
    # 主役の 5 つ
    y, h = 104, 64
    xs = [20, 172, 324, 476, 628]
    w = 112
    b.append(box(xs[0], y, w, h, "広告主", "buy", sub="広告代理店"))
    b.append(box(xs[1], y, w, h, "DSP", "buy", 18, sub="入札する"))
    b.append(box(xs[2], y, w, h, "アドエクス", "market", sub="チェンジ"))
    b.append(box(xs[3], y, w, h, "SSP", "sell", 18, sub="入札を募る"))
    b.append(box(xs[4], y, w, h, "媒体社", "sell", sub="サイト・アプリ"))
    for x in xs[:-1]:
        b.append(arrow(x + w + 6, y + h / 2, x + 152 - 6, y + h / 2, "ink", 2, both=True))
    # 広告枠の流れ
    b.append(arrow(690, 202, 70, 202, "sell", 2))
    b.append(label_tag(380, 202, "広告枠（インプレッション）の流れ", "sell"))
    # 補助
    b.append(box(168, 240, 120, 54, "DMP / CDP", "buy", 13, sub="ユーザーデータ", dashed=True, weight=700))
    b.append(arrow(228, 240, 228, 172, "buy", 1.5, dashed=True))
    b.append(box(624, 240, 120, 54, "ユーザー", "user", 13, sub="ページを見る人"))
    b.append(arrow(684, 240, 684, 172, "muted", 1.5, both=True))
    b.append(text(380, 318, "1 回の表示ごとに、この流れが約 0.1 秒で完了する", 12, MUTED))
    write("fig-ecosystem.svg", svg(W, H, b, "RTB の登場人物と、お金・広告枠の流れ"))


def fig_timeline():
    W, H = 760, 300
    x0, x1, t1 = 170, 730, 120  # 0ms〜120ms
    sx = (x1 - x0) / t1
    X = lambda t: x0 + t * sx  # noqa: E731
    b = []
    # 目盛り
    for t in range(0, t1 + 1, 20):
        b.append(f'<line x1="{X(t):.1f}" y1="56" x2="{X(t):.1f}" y2="246" stroke="{LINE}" stroke-width="1"/>')
        b.append(text(X(t), 262, f"{t} ms", 11, MUTED))
    rows = [("SSP", 80, "market"), ("ネットワーク", 140, "user"), ("DSP 内部", 200, "buy")]
    for name, y, role in rows:
        b.append(text(150, y, name, 13, ROLE[role][2], anchor="end", weight=700))

    def bar(t0, t, y, label, role, inside=True, below=False):
        fill, stroke, ink = ROLE[role]
        w = t * sx
        out = f'<rect x="{X(t0):.1f}" y="{y-15}" width="{w:.1f}" height="30" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        if inside:
            out += text(X(t0) + w / 2, y, label, 12, ink, weight=700)
        elif below:
            out += text(X(t0), y + 26, label, 11, ink, anchor="start")
        else:
            out += text(X(t0), y - 26, label, 11, ink, anchor="start")
        return out

    b.append(bar(0, 10, 80, "受信・作成", "market", inside=False))
    b.append(bar(10, 100, 80, "DSP の応答を待つ（tmax = 100 ms）", "market"))
    b.append(bar(110, 8, 80, "落札決定", "market", inside=False, below=True))
    b.append(bar(10, 12, 140, "Bid Request", "user", inside=False))
    b.append(bar(88, 12, 140, "Bid Response", "user", inside=False))
    b.append(bar(22, 20, 200, "ユーザー情報の参照", "buy", inside=False))
    b.append(bar(42, 46, 200, "CTR 予測・入札額の計算", "buy"))
    # 締め切り
    b.append(f'<line x1="{X(110):.1f}" y1="48" x2="{X(110):.1f}" y2="246" stroke="{ACCENT["alert"]}" stroke-width="2" stroke-dasharray="5 4"/>')
    b.append(text(X(110), 38, "締め切り", 12, ACCENT["alert"], weight=700))
    b.append(text(380, 284, "※ 数値は一例。実際の tmax は SSP により 100〜300 ms 程度", 11, MUTED))
    write("fig-timeline.svg", svg(W, H, b, "1 インプレッションの処理タイムライン"))


def fig_auction_types():
    W, H = 760, 330
    b = []
    # 左：入札の棒グラフ
    gx0, gy0, gh = 70, 280, 220  # y=280 が 0 円
    ymax = 500
    Y = lambda v: gy0 - v / ymax * gh  # noqa: E731
    for v in range(0, 501, 100):
        b.append(f'<line x1="{gx0}" y1="{Y(v):.1f}" x2="370" y2="{Y(v):.1f}" stroke="{LINE}" stroke-width="1"/>')
        b.append(text(gx0 - 8, Y(v), f"{v}", 11, MUTED, anchor="end"))
    b.append(text(gx0 - 8, 44, "円 CPM", 11, MUTED, anchor="end"))
    bids = [("DSP A", 300, "user"), ("DSP B", 450, "buy"), ("DSP C", 200, "user")]
    for i, (name, v, role) in enumerate(bids):
        x = gx0 + 20 + i * 98
        fill, stroke, ink = ROLE[role]
        b.append(f'<rect x="{x}" y="{Y(v):.1f}" width="64" height="{gy0 - Y(v):.1f}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(text(x + 32, Y(v) - 14, f"{v} 円", 13, ink, weight=700))
        b.append(text(x + 32, gy0 + 16, name, 12, INK))
    b.append(text(gx0 + 52 + 98, Y(450) - 34, "最高額", 11, ROLE["buy"][2], weight=700))
    # フロア
    b.append(f'<line x1="{gx0}" y1="{Y(100):.1f}" x2="370" y2="{Y(100):.1f}" stroke="{ACCENT["alert"]}" stroke-width="2" stroke-dasharray="6 4"/>')
    b.append(text(372, Y(100), "フロア 100 円", 11, ACCENT["alert"], anchor="start", weight=700))

    # 右：2 つの方式
    def card(y, title, pay, note, role):
        fill, stroke, ink = ROLE[role]
        return "\n".join([
            f'<rect x="460" y="{y}" width="280" height="118" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
            text(480, y + 24, title, 14, ink, anchor="start", weight=700),
            text(480, y + 60, "DSP B が落札し、支払うのは", 12, INK, anchor="start"),
            text(720, y + 60, pay, 22, ink, anchor="end", weight=700),
            text(480, y + 94, note, 12, MUTED, anchor="start"),
        ])

    b.append(card(36, "セカンドプライス", "301 円", "2 位（300 円）＋ 1 円", "sell"))
    b.append(card(176, "ファーストプライス（現在の主流）", "450 円", "自分の入札額をそのまま支払う", "market"))
    write("fig-auction-types.svg", svg(W, H, b, "セカンドプライスとファーストプライスの支払額の違い"))


def fig_bid_shading():
    W, H = 760, 400
    v = 450.0
    win = lambda b_: 1 / (1 + math.exp(-(b_ - 290) / 45))  # noqa: E731  勝率の例
    gx0, gx1, gy0, gy1 = 80, 660, 300, 50
    X = lambda b_: gx0 + b_ / v * (gx1 - gx0)  # noqa: E731
    Yy = lambda yen: gy0 - yen / v * (gy0 - gy1)  # noqa: E731  左軸（円）
    Yp = lambda p: gy0 - p * (gy0 - gy1)  # noqa: E731  右軸（勝率）
    out = []
    for yen in range(0, 451, 90):
        out.append(f'<line x1="{gx0}" y1="{Yy(yen):.1f}" x2="{gx1}" y2="{Yy(yen):.1f}" stroke="{LINE}" stroke-width="1"/>')
        out.append(text(gx0 - 8, Yy(yen), f"{yen}", 11, MUTED, anchor="end"))
    for p in (0, 0.5, 1.0):
        out.append(text(gx1 + 8, Yp(p), f"{int(p*100)}%", 11, ACCENT["market"], anchor="start"))
    for bb in range(0, 451, 90):
        out.append(text(X(bb), gy0 + 16, f"{bb}", 11, MUTED))
    out.append(text((gx0 + gx1) / 2, gy0 + 38, "入札額 b（円 CPM）　※ 評価額 v = 450 円", 12, INK))
    out.append(text(gx0 - 8, 30, "円", 11, MUTED, anchor="end"))
    out.append(text(gx1 + 8, 30, "勝率", 11, ACCENT["market"], anchor="start"))

    pts = [i * 2.5 for i in range(int(v / 2.5) + 1)]
    profit = " ".join(f"{X(p):.1f},{Yy(v - p):.1f}" for p in pts)
    winp = " ".join(f"{X(p):.1f},{Yp(win(p)):.1f}" for p in pts)
    ev = [(p, win(p) * (v - p)) for p in pts]
    evs = " ".join(f"{X(p):.1f},{Yy(e):.1f}" for p, e in ev)
    bstar, estar = max(ev, key=lambda t: t[1])
    out.append(f'<polyline points="{profit}" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>')
    out.append(f'<polyline points="{winp}" fill="none" stroke="{ACCENT["market"]}" stroke-width="2.5"/>')
    out.append(f'<polygon points="{X(0):.1f},{Yy(0):.1f} {evs} {X(v):.1f},{Yy(0):.1f}" fill="#4f46e5" fill-opacity="0.10"/>')
    out.append(f'<polyline points="{evs}" fill="none" stroke="{ACCENT["buy"]}" stroke-width="3.5"/>')
    # 最適点
    out.append(f'<line x1="{X(bstar):.1f}" y1="{Yy(estar):.1f}" x2="{X(bstar):.1f}" y2="{gy0}" stroke="{ACCENT["buy"]}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    out.append(f'<circle cx="{X(bstar):.1f}" cy="{Yy(estar):.1f}" r="6" fill="{ACCENT["buy"]}"/>')
    out.append(text(X(bstar), Yy(estar) - 22, f"最適な入札額 ≈ {bstar:.0f} 円", 13, ROLE["buy"][2], weight=700))
    # 凡例
    lx, ly = 0, 370
    legend = [
        (f'stroke="{ACCENT["buy"]}" stroke-width="3.5"', "期待利益 ＝ 勝率 ×（v − b）"),
        (f'stroke="{ACCENT["market"]}" stroke-width="2.5"', "勝率（右軸）"),
        (f'stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"', "勝ったときの利益 v − b"),
    ]
    for (st, lab), lx in zip(legend, (70, 330, 490)):
        out.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+28}" y2="{ly}" {st}/>')
        out.append(text(lx + 36, ly, lab, 12, INK, anchor="start"))
    write("fig-bid-shading.svg", svg(W, H, out, "ビッドシェーディング：期待利益が最大になる入札額"))
    return bstar


def fig_waterfall_vs_hb():
    W, H = 760, 390
    b = []
    # 左：ウォーターフォール
    b.append(text(190, 32, "ウォーターフォール（従来）", 15, INK, weight=700))
    b.append(box(110, 52, 160, 40, "広告リクエスト", "user", 13))
    steps = [("SSP A（フロア 300 円）", 118), ("SSP B（フロア 200 円）", 196), ("SSP C（フロア 100 円）", 274)]
    prev = 92
    for label, y in steps:
        b.append(arrow(190, prev, 190, y - 2, "muted"))
        b.append(box(90, y, 200, 44, label, "sell", 13))
        b.append(arrow(290, y + 22, 330, y + 22, "good", 1.5))
        b.append(text(336, y + 22, "売れたら終了", 11, ROLE["good"][2], anchor="start"))
        prev = y + 44
    b.append(text(200, 179, "売れなければ次へ", 11, MUTED, anchor="start"))
    b.append(text(190, 346, "順番に問い合わせるので遅く、", 12, ROLE["alert"][2]))
    b.append(text(190, 366, "後ろの SSP の高値を取りこぼす", 12, ROLE["alert"][2]))
    b.append(f'<line x1="410" y1="30" x2="410" y2="370" stroke="{LINE}" stroke-width="1.5"/>')
    # 右：ヘッダービディング
    b.append(text(585, 32, "ヘッダービディング（現在）", 15, INK, weight=700))
    b.append(box(505, 52, 160, 40, "Prebid.js など", "market", 13))
    xs = [440, 545, 650]
    bids = [("SSP A", "300 円", "sell"), ("SSP B", "500 円", "good"), ("SSP C", "250 円", "sell")]
    for x, (n, p, role) in zip(xs, bids):
        b.append(arrow(585, 92, x + 45, 136, "market", 1.5))
        b.append(box(x, 138, 90, 56, n, role, 13, sub=p))
        b.append(arrow(x + 45, 194, 585, 240, "muted", 1.5))
    b.append(box(495, 242, 180, 44, "アドサーバーで比較", "user", 13))
    b.append(arrow(585, 286, 585, 306, "good"))
    b.append(box(495, 308, 180, 40, "SSP B（500 円）を表示", "good", 13))
    b.append(text(585, 366, "全 SSP に同時に聞き、最高値を選ぶ", 12, ROLE["good"][2]))
    write("fig-waterfall-vs-hb.svg", svg(W, H, b, "ウォーターフォールとヘッダービディングの比較"))


def fig_bid_pipeline():
    W, H = 760, 220
    b = []
    cards = [
        ("① 価値を計算", "600 円", "pCTR × pCVR\n× 目標CPA × 1000", "buy"),
        ("② ペーシング", "540 円", "予算消化の調整\n× 0.9", "buy"),
        ("③ シェーディング", "380 円", "ファーストプライス\n対策で引き下げ", "buy"),
        ("④ フロア判定", "OK", "380 円 ≧ 100 円\n（フロア）", "market"),
        ("入札", "380 円", "Bid Response\nを返す", "good"),
    ]
    w, gap, x = 130, 22, 11
    for i, (title, val, note, role) in enumerate(cards):
        fill, stroke, ink = ROLE[role]
        b.append(f'<rect x="{x}" y="40" width="{w}" height="140" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(text(x + w / 2, 62, title, 13, ink, weight=700))
        b.append(text(x + w / 2, 102, val, 24, ink, weight=700))
        b.append(text(x + w / 2, 148, note, 11, INK))
        if i < len(cards) - 1:
            b.append(arrow(x + w + 2, 110, x + w + gap - 2, 110, "ink", 2))
        x += w + gap
    b.append(text(380, 202, "※ 数値は説明用の一例", 11, MUTED))
    write("fig-bid-pipeline.svg", svg(W, H, b, "DSP が入札額を決めるまでの流れ"))


def fig_supply_chain():
    W, H = 760, 400
    MONO = "font-family=\"'Source Code Pro',Consolas,Menlo,monospace\""
    b = []
    y = 40
    nodes = [(20, 140, "媒体社", "news.example.jp", "sell"), (210, 140, "SSP A", "ssp-a.example", "sell"),
             (400, 140, "SSP B", "ssp-b.example", "sell"), (590, 150, "DSP", "入札するか判断", "buy")]
    for x, w, n, sub, role in nodes:
        b.append(box(x, y, w, 60, n, role, 15, sub=sub))
    for x in (160, 350, 540):
        b.append(arrow(x + 4, y + 30, x + 46, y + 30, "ink"))
    b.append(text(375, 26, "SSP A が SSP B に再販", 11, MUTED))

    def card(x, yy, w, h, title, lines, role="user"):
        fill, stroke, ink = ROLE[role]
        out = [f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
               text(x + 14, yy + 20, title, 12, ink, anchor="start", weight=700)]
        for i, ln in enumerate(lines):
            out.append(text(x + 14, yy + 46 + i * 22, ln, 12, INK, anchor="start", extra=MONO))
        return "\n".join(out)

    b.append(card(420, 140, 320, 96, "schain（Bid Request 内の販売経路の記録）",
                  ["[0] asi: ssp-a.example  sid: 1111", "[1] asi: ssp-b.example  sid: 2222"], "market"))
    b.append(arrow(560, 102, 560, 138, "market", 1.5))
    b.append(card(20, 262, 250, 96, "news.example.jp/ads.txt",
                  ["ssp-a.example, 1111, DIRECT", "ssp-b.example, 2222, RESELLER"]))
    b.append(card(290, 262, 250, 96, "各 SSP の sellers.json",
                  ["ssp-a: 1111 = news.example.jp", "ssp-b: 2222 = SSP A（仲介）"]))
    b.append(arrow(90, 102, 90, 260, "muted", 1.5, dashed=True))
    b.append(text(98, 180, "媒体社が公開", 11, MUTED, anchor="start"))
    b.append(arrow(280, 102, 380, 260, "muted", 1.5, dashed=True))
    b.append(text(336, 170, "各 SSP が公開", 11, MUTED, anchor="start"))
    b.append(box(560, 262, 180, 96, "DSP が照合", "good", 15, sub="経路はすべて正規？"))
    b.append(arrow(650, 238, 650, 260, "good", 1.5))
    b.append(text(380, 382, "各ノードは「広告システム（asi）＋その中の販売者アカウント（sid）」の組", 12, MUTED))
    write("fig-supply-chain.svg", svg(W, H, b, "ads.txt・sellers.json・SupplyChain Object による販売経路の検証"))


def fig_funnel():
    W, H = 760, 270
    b = []
    stages = [
        ("インプレッション（表示）", "1,000,000 回", 680, "user"),
        ("クリック", "5,000 回", 470, "buy"),
        ("コンバージョン（購入）", "100 件", 260, "good"),
    ]
    y = 30
    for i, (name, val, w, role) in enumerate(stages):
        fill, stroke, ink = ROLE[role]
        nw = stages[i + 1][2] if i + 1 < len(stages) else w - 120
        x0, x1 = 380 - w / 2, 380 + w / 2
        n0, n1 = 380 - nw / 2, 380 + nw / 2
        b.append(f'<polygon points="{x0},{y} {x1},{y} {n1},{y+56} {n0},{y+56}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(text(380, y + 20, name, 13, ink, weight=700))
        b.append(text(380, y + 40, val, 15, ink, weight=700))
        y += 56
        if i < len(stages) - 1:
            rate = ["CTR 0.5%", "CVR 2%"][i]
            b.append(label_tag(380 + w / 2 - 10, y + 8, rate, "market", 11))
            y += 16
    b.append(text(380, 252, "※ 幅は実際の比率ではなくイメージ", 11, MUTED))
    write("fig-funnel.svg", svg(W, H, b, "広告のファネル：表示からコンバージョンまで"))


def fig_money_flow():
    W, H = 760, 250
    b = []
    parts = [
        ("媒体社", 52, "good"), ("SSP", 13, "sell"), ("データ・計測", 5, "user"),
        ("DSP", 15, "buy"), ("広告代理店", 15, "market"),
    ]
    x0, x1, y = 40, 720, 90
    sx = (x1 - x0) / 100
    x = x0
    b.append(text(380, 36, "広告主が支払った 100 円の行き先（イメージ）", 15, INK, weight=700))
    for name, v, role in parts:
        fill, stroke, ink = ROLE[role]
        w = v * sx
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="56" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        b.append(text(x + w / 2, y + 28, f"{v} 円", 14 if v >= 10 else 11, ink, weight=700))
        if v >= 10:
            b.append(text(x + w / 2, y + 76, name, 12, ink, weight=700))
        else:
            b.append(text(x + w / 2, y + 76, name, 11, ink))
        x += w
    # 中間コストの括弧
    mid0 = x0 + 52 * sx
    b.append(f'<path d="M {mid0:.1f} 186 L {mid0:.1f} 196 L {x1} 196 L {x1} 186" fill="none" stroke="{ACCENT["alert"]}" stroke-width="1.5"/>')
    b.append(text((mid0 + x1) / 2, 214, "中間コスト 48 円（いわゆる「アドテク税」）", 12, ROLE["alert"][2], weight=700))
    b.append(text(380, 236, "※ 割合は取引によって大きく異なります", 11, MUTED))
    write("fig-money-flow.svg", svg(W, H, b, "広告費 100 円の行き先"))


if __name__ == "__main__":
    fig_ecosystem()
    fig_timeline()
    fig_auction_types()
    print("optimal bid:", round(fig_bid_shading()))
    fig_waterfall_vs_hb()
    fig_bid_pipeline()
    fig_supply_chain()
    fig_funnel()
    fig_money_flow()

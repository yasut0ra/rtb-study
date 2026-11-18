"""RTB オークション・シミュレーター

オークション方式（セカンドプライス / ファーストプライス）やフロアプライスによって、
媒体社の収益と DSP の利益がどう変わるかを比べる学習用スクリプトです。

使い方:
    python auction_simulator.py
    python auction_simulator.py --bidders 6 --auctions 50000 --seed 1

Python 3.8 以降、標準ライブラリのみで動きます。

前提（シンプルにするための仮定）:
    - 各 DSP の「評価額（払ってもいい上限）」は 0〜1000 円 CPM の一様分布
    - 各 DSP は互いの評価額を知らない
"""

from __future__ import annotations

import argparse
import random
import statistics
from dataclasses import dataclass

MAX_VALUE = 1000  # 評価額の上限（円 CPM）
BAR = "■"


@dataclass
class Result:
    name: str
    revenue: float  # 媒体社の平均収益（円 CPM）
    surplus: float  # 勝った DSP の平均利益（評価額 − 支払額）
    fill_rate: float  # 広告が売れた割合


def draw_values(rng: random.Random, n: int) -> list[float]:
    return [rng.uniform(0, MAX_VALUE) for _ in range(n)]


def run_auction(values: list[float], bids: list[float], rule: str, floor: float = 0.0):
    """1回のオークションを実行し、(支払額, 勝者の利益) を返す。売れなければ None。"""
    eligible = [(b, v) for b, v in zip(bids, values) if b >= floor]
    if not eligible:
        return None
    eligible.sort(reverse=True)
    win_bid, win_value = eligible[0]
    if rule == "second":
        second = eligible[1][0] if len(eligible) > 1 else floor
        price = max(second, floor)
    else:
        price = win_bid
    return price, win_value - price


def simulate(name, rng, n_bidders, n_auctions, rule, bid_fn, floor=0.0) -> Result:
    revenues, surpluses, sold = [], [], 0
    for _ in range(n_auctions):
        values = draw_values(rng, n_bidders)
        bids = [bid_fn(v) for v in values]
        outcome = run_auction(values, bids, rule, floor)
        if outcome is None:
            revenues.append(0.0)
            continue
        price, surplus = outcome
        sold += 1
        revenues.append(price)
        surpluses.append(surplus)
    return Result(
        name=name,
        revenue=statistics.fmean(revenues),
        surplus=statistics.fmean(surpluses) if surpluses else 0.0,
        fill_rate=sold / n_auctions,
    )


def bar(value: float, scale: float, width: int = 30) -> str:
    return BAR * max(0, round(value / scale * width))


def section(title: str) -> None:
    print()
    print("=" * 64)
    print(f" {title}")
    print("=" * 64)


def compare_auction_types(rng, n, auctions) -> None:
    section(f"① オークション方式の比較（DSP {n} 社）")
    shade = (n - 1) / n  # 一様分布のときの理論上の最適シェーディング率
    results = [
        simulate("セカンドプライス（正直に入札）", rng, n, auctions, "second", lambda v: v),
        simulate("ファーストプライス（正直に入札）", rng, n, auctions, "first", lambda v: v),
        simulate(f"ファーストプライス（{shade:.0%} にシェーディング）", rng, n, auctions, "first",
                 lambda v: v * shade),
    ]
    scale = max(r.revenue for r in results)
    for r in results:
        print(f"\n {r.name}")
        print(f"   媒体社の収益 {r.revenue:7.1f} 円  {bar(r.revenue, scale)}")
        print(f"   DSP の利益   {r.surplus:7.1f} 円  {bar(r.surplus, scale)}")
    print(
        "\n 💡 ポイント"
        "\n  - ファーストプライスで正直に入札すると、DSP の利益はゼロ（払いすぎ）。"
        "\n  - シェーディングすると、媒体社の収益はセカンドプライスとほぼ同じになる。"
        "\n    （経済学の「収益等価定理」。前提が崩れると成り立たないこともある）"
    )


def compare_floors(rng, n, auctions) -> None:
    section(f"② フロアプライスの効果（セカンドプライス、DSP {n} 社）")
    print("\n フロア   収益（円）                                 Fill Rate")
    results = [
        (floor, simulate("", rng, n, auctions, "second", lambda v: v, floor))
        for floor in (0, 200, 400, 500, 600, 800, 950)
    ]
    scale = max(r.revenue for _, r in results)
    best = max(results, key=lambda x: x[1].revenue)[0]
    for floor, r in results:
        mark = " ← 最大" if floor == best else ""
        print(f"  {floor:4d}円  {r.revenue:6.1f} {bar(r.revenue, scale):30s}  {r.fill_rate:6.1%}{mark}")
    print(
        "\n 💡 ポイント"
        "\n  - フロアを上げると、ある程度までは収益が増える（安売りを防げる）。"
        "\n  - 上げすぎると売れ残り（Fill Rate 低下）が増えて、収益が下がる。"
    )


def optimal_shading(rng, n, auctions, my_value: float = 600.0) -> None:
    section(f"③ DSP A の最適な入札額（評価額 {my_value:.0f} 円、ファーストプライス）")
    # 他の DSP は理論上の最適シェーディングで入札していると仮定し、
    # 「他社の最高入札額」の分布を過去データとして集める
    shade = (n - 1) / n
    history = [max(v * shade for v in draw_values(rng, n - 1)) for _ in range(auctions)]

    print("\n 入札額   勝率     期待利益 = 勝率 × (評価額 − 入札額)")
    rows = []
    for b in range(0, int(my_value) + 1, 50):
        win_rate = sum(1 for h in history if h < b) / len(history)
        rows.append((b, win_rate, win_rate * (my_value - b)))
    scale = max(r[2] for r in rows) or 1
    best = max(rows, key=lambda r: r[2])[0]
    for b, wr, ep in rows:
        mark = " ← 最適" if b == best else ""
        print(f"  {b:4d}円  {wr:6.1%}  {ep:6.1f}円 {bar(ep, scale, 25)}{mark}")
    print(
        "\n 💡 ポイント"
        "\n  - 入札額を下げると勝ったときの利益は増えるが、勝率が下がる。"
        "\n  - DSP は過去の勝敗データから勝率を推定し、期待利益が最大の入札額を選ぶ。"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="RTB オークション・シミュレーター")
    parser.add_argument("--bidders", type=int, default=4, help="入札する DSP の数（2 以上）")
    parser.add_argument("--auctions", type=int, default=20000, help="シミュレーションするオークション回数")
    parser.add_argument("--seed", type=int, default=42, help="乱数シード")
    args = parser.parse_args()
    if args.bidders < 2:
        parser.error("--bidders は 2 以上にしてください")

    rng = random.Random(args.seed)
    print(f"評価額: 0〜{MAX_VALUE} 円 CPM の一様分布 / オークション {args.auctions:,} 回")
    compare_auction_types(rng, args.bidders, args.auctions)
    compare_floors(rng, args.bidders, args.auctions)
    optimal_shading(rng, args.bidders, args.auctions)
    print()


if __name__ == "__main__":
    main()

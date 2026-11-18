"""
把卡牌資料轉成 pandas DataFrame，計算所有分析指標。
"""

import pandas as pd
from src.cards import (
    load_cards, base_power, effect_bonus, power_score,
    balance_score, deviation, keyword_tags, archetype, status_label,
    BALANCE_BASELINE, OVERPOWERED_THRESHOLD, UNDERPOWERED_THRESHOLD,
)


def build_dataframe(cards: list[dict] = None) -> pd.DataFrame:
    if cards is None:
        cards = load_cards()

    rows = []
    for c in cards:
        bp  = base_power(c)
        eb  = effect_bonus(c)
        ps  = power_score(c)
        bs  = balance_score(c)
        dev = deviation(c)
        rows.append({
            "名稱":     c["name"],
            "費用":     c["cost"],
            "攻擊":     c["atk"],
            "生命":     c["hp"],
            "攻血比":   f"{c['atk']}/{c['hp']}",
            "基礎強度": round(bp, 2),
            "效果加值": round(eb, 2),
            "總強度":   round(ps, 2),
            "費效比":   round(bs, 2),
            "偏差":     round(dev, 4),
            "偏差%":    f"{dev:+.0%}",
            "牌型":     archetype(c),
            "關鍵字":   "、".join(keyword_tags(c)) or "—",
            "狀態":     status_label(c),
            "raw":      c,
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("費效比", ascending=False).reset_index(drop=True)
    df.index += 1  # 從 1 開始
    return df


def summary(df: pd.DataFrame) -> dict:
    """全局統計摘要"""
    overpowered  = df[df["費效比"] >= OVERPOWERED_THRESHOLD]
    underpowered = df[df["費效比"] <= UNDERPOWERED_THRESHOLD]
    balanced     = df[(df["費效比"] > UNDERPOWERED_THRESHOLD) &
                      (df["費效比"] < OVERPOWERED_THRESHOLD)]

    # 平衡指數：越接近 10 代表所有卡費效比越集中
    # 用變異係數（標準差 / 平均值）的倒數轉換
    cv = df["費效比"].std() / df["費效比"].mean()
    balance_index = round(max(0, 10 - cv * 20), 1)

    return {
        "total":         len(df),
        "overpowered":   overpowered,
        "underpowered":  underpowered,
        "balanced":      balanced,
        "avg_balance":   round(df["費效比"].mean(), 2),
        "std_balance":   round(df["費效比"].std(), 2),
        "balance_index": balance_index,
        "archetype_dist": df["牌型"].value_counts().to_dict(),
    }


def print_report(df: pd.DataFrame) -> None:
    s = summary(df)
    w = 66

    print("╔" + "═" * w + "╗")
    print("║" + "  Iron & Gears 卡牌平衡分析 ── Phase 1 靜態報告".center(w) + "║")
    print("╚" + "═" * w + "╝")
    print()

    # ── 全部卡牌排名表 ──
    print("━" * (w + 2))
    print("  全部卡牌費效比排名（基準線 = 1.80 ≡ 普通的自走齒輪）")
    print("━" * (w + 2))
    header = f"  {'排':>2}  {'卡牌名稱':<12}  {'費':>2}  {'攻/血':>5}  {'基礎':>5}  {'效果':>5}  {'總強':>5}  {'費效比':>5}  {'偏差':>6}  {'牌型':<6}  {'狀態'}"
    print(header)
    print("  " + "─" * (w - 2))

    for rank, row in df.iterrows():
        flag = "⚠" if "過強" in row["狀態"] else ("↓" if "偏弱" in row["狀態"] else " ")
        line = (
            f"  {rank:>2}  {row['名稱']:<12}  {row['費用']:>2}  "
            f"{row['攻血比']:>5}  {row['基礎強度']:>5.1f}  {row['效果加值']:>5.1f}  "
            f"{row['總強度']:>5.1f}  {row['費效比']:>5.2f}  {row['偏差%']:>6}  "
            f"{row['牌型']:<6} {flag}"
        )
        print(line)

    print()

    # ── 整體統計 ──
    print("━" * (w + 2))
    print("  整體統計")
    print("━" * (w + 2))
    print(f"  卡牌總數：{s['total']} 張")
    print(f"  平均費效比：{s['avg_balance']:.2f}  ｜  標準差：{s['std_balance']:.2f}")
    print(f"  平衡指數：{s['balance_index']} / 10.0  （數值越高，卡牌間費效比越集中）")
    print(f"  ⚠ 可能過強（費效比 ≥ {OVERPOWERED_THRESHOLD:.2f}）：{len(s['overpowered'])} 張")
    print(f"  ↓ 可能偏弱（費效比 ≤ {UNDERPOWERED_THRESHOLD:.2f}）：{len(s['underpowered'])} 張")
    print(f"  ✓ 平衡範圍：{len(s['balanced'])} 張")
    print()

    # ── 牌型分布 ──
    print("━" * (w + 2))
    print("  牌型分布")
    print("━" * (w + 2))
    for arch, count in sorted(s["archetype_dist"].items(), key=lambda x: -x[1]):
        bar = "█" * count
        print(f"  {arch:<6} {bar} ({count})")
    print()

    # ── 關鍵發現 ──
    print("━" * (w + 2))
    print("  關鍵發現")
    print("━" * (w + 2))

    if len(s["overpowered"]):
        print("\n  ⚠  以下卡牌費效比顯著高於基準線，建議重新審視：")
        for _, row in s["overpowered"].iterrows():
            print(f"     • {row['名稱']:<12}  費效比 {row['費效比']:.2f}  ({row['偏差%']})")
            _suggest_nerf(row)

    if len(s["underpowered"]):
        print("\n  ↓  以下卡牌費效比低於基準線，可能在模擬中使用率偏低：")
        for _, row in s["underpowered"].iterrows():
            print(f"     • {row['名稱']:<12}  費效比 {row['費效比']:.2f}  ({row['偏差%']})")

    print()
    print("  ⚙  注意：效果加值為理論估算，部分情境性效果（如 savefuel、healfriendly）")
    print("     實際價值高度依賴遊戲情境，需等 Phase 3 模擬校準。")
    print()


def _suggest_nerf(row: pd.Series) -> None:
    c = row["raw"]
    suggestions = []
    bs = row["費效比"]
    target_bs = OVERPOWERED_THRESHOLD - 0.05

    if c["cost"] == 1 and bs > 2.5:
        suggestions.append(f"調整方向：費用 1→2（調整後費效比估算 ≈ {row['總強度']/2:.2f}）")
    elif c["atk"] > 0:
        suggestions.append(f"調整方向：攻擊 {c['atk']}→{c['atk']-1}（-0.06 費效比）")
    elif c["hp"] > 1:
        suggestions.append(f"調整方向：生命 {c['hp']}→{c['hp']-1}（-0.04 費效比）")

    for s in suggestions:
        print(f"       → {s}")

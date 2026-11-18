"""
產生三張分析圖表，存入 outputs/charts/。
需要 matplotlib + seaborn。
"""

import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # 無 GUI 模式，避免 macOS 視窗問題
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# ── 中文字體設定 ──────────────────────────────────────
def _setup_font() -> None:
    import matplotlib.font_manager as fm
    preferred = ["PingFang SC", "Heiti TC", "STHeiti", "Arial Unicode MS", "SimHei"]
    available = {f.name for f in fm.fontManager.ttflist}
    chosen = next((f for f in preferred if f in available), None)
    if chosen:
        plt.rcParams["font.sans-serif"] = [chosen, "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False


_setup_font()

# ── 顏色主題 ──────────────────────────────────────────
C_OVERPOWER  = "#E05050"   # 紅：過強
C_BALANCED   = "#50A878"   # 綠：平衡
C_UNDERPOWER = "#5090D0"   # 藍：偏弱
C_NEUTRAL    = "#B07830"   # 金：背景強調
BG           = "#100804"
TEXT         = "#F0E0C0"


def _card_color(balance_score: float, threshold_over: float, threshold_under: float) -> str:
    if balance_score >= threshold_over:
        return C_OVERPOWER
    if balance_score <= threshold_under:
        return C_UNDERPOWER
    return C_BALANCED


def plot_balance_scores(df, output_dir: Path) -> Path:
    """
    圖一：費效比橫條圖（從高到低），用顏色標示過強/偏弱。
    """
    from src.cards import BALANCE_BASELINE, OVERPOWERED_THRESHOLD, UNDERPOWERED_THRESHOLD

    n = len(df)
    fig, ax = plt.subplots(figsize=(11, max(7, n * 0.28)))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor("#1a100a")

    names    = df["名稱"].tolist()
    scores   = df["費效比"].tolist()
    colors   = [_card_color(s, OVERPOWERED_THRESHOLD, UNDERPOWERED_THRESHOLD) for s in scores]
    y_pos    = np.arange(len(names))

    bars = ax.barh(y_pos, scores, color=colors, edgecolor="none", height=0.65)

    # 數值標籤
    for bar, score, dev in zip(bars, scores, df["偏差%"].tolist()):
        ax.text(bar.get_width() + 0.04, bar.get_y() + bar.get_height() / 2,
                f"{score:.2f}  ({dev})", va="center", ha="left",
                color=TEXT, fontsize=8.5)

    # 基準線
    ax.axvline(BALANCE_BASELINE, color="#E0A020", linewidth=1.5,
               linestyle="--", label=f"基準線 {BALANCE_BASELINE:.2f}")
    ax.axvline(OVERPOWERED_THRESHOLD, color=C_OVERPOWER, linewidth=1,
               linestyle=":", alpha=0.7, label=f"過強門檻 {OVERPOWERED_THRESHOLD:.2f}")
    ax.axvline(UNDERPOWERED_THRESHOLD, color=C_UNDERPOWER, linewidth=1,
               linestyle=":", alpha=0.7, label=f"偏弱門檻 {UNDERPOWERED_THRESHOLD:.2f}")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, color=TEXT, fontsize=10)
    ax.set_xlabel("費效比（Power Score ÷ 費用）", color=TEXT, fontsize=10)
    ax.set_title("Iron & Gears ｜ 卡牌費效比排名", color=TEXT, fontsize=13, pad=12)
    ax.tick_params(colors=TEXT)
    ax.spines[:].set_color("#3a2010")
    ax.set_xlim(0, max(scores) + 0.6)

    legend = ax.legend(loc="lower right", facecolor="#2a1810", edgecolor="#3a2010",
                       labelcolor=TEXT, fontsize=8)

    fig.tight_layout()
    out = output_dir / "chart_01_balance_scores.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return out


def plot_power_breakdown(df, output_dir: Path) -> Path:
    """
    圖二：每張卡的強度來源分解（基礎數值 vs 效果加值）。
    """
    fig, ax = plt.subplots(figsize=(13, max(7, len(df) * 0.25)))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor("#1a100a")

    # 按費用排序顯示
    df_sorted = df.sort_values("費用").reset_index(drop=True)
    names  = df_sorted["名稱"].tolist()
    base   = df_sorted["基礎強度"].tolist()
    effect = df_sorted["效果加值"].tolist()
    x_pos  = np.arange(len(names))

    bars1 = ax.bar(x_pos, base,   color="#7a5020", label="基礎數值（攻擊+生命）", width=0.6)
    bars2 = ax.bar(x_pos, effect, bottom=base, color="#E0A020", label="效果加值", width=0.6, alpha=0.85)

    # 費用標籤
    for i, (b, e, cost) in enumerate(zip(base, effect, df_sorted["費用"].tolist())):
        total = b + e
        ax.text(i, total + 0.2, f"{total:.1f}", ha="center", va="bottom",
                color=TEXT, fontsize=7.5, fontweight="bold")
        ax.text(i, -1.0, f"{cost}費", ha="center", va="top",
                color=C_NEUTRAL, fontsize=7.5)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(names, rotation=35, ha="right", color=TEXT, fontsize=9)
    ax.set_ylabel("強度分數", color=TEXT, fontsize=10)
    ax.set_title("Iron & Gears ｜ 卡牌強度來源分解", color=TEXT, fontsize=13, pad=12)
    ax.tick_params(colors=TEXT)
    ax.spines[:].set_color("#3a2010")
    ax.set_ylim(-2, max(b + e for b, e in zip(base, effect)) + 2)

    legend = ax.legend(facecolor="#2a1810", edgecolor="#3a2010",
                       labelcolor=TEXT, fontsize=9)

    fig.tight_layout()
    out = output_dir / "chart_02_power_breakdown.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return out


def plot_cost_vs_power(df, output_dir: Path) -> Path:
    """
    圖三：費用 vs 總強度散點圖。
    每個點大小 = HP，顏色 = 牌型。
    加入 baseline 趨勢線（balance = 1.80 → power = 1.80 * cost）。
    """
    ARCHETYPE_COLORS = {
        "快攻": "#E05050",
        "中速": "#E0A020",
        "控制": "#5090D0",
        "資源": "#70C070",
        "清場": "#C050C0",
        "後期": "#50C0C0",
    }

    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor("#1a100a")

    archetypes = df["牌型"].unique()
    for arch in archetypes:
        sub = df[df["牌型"] == arch]
        color = ARCHETYPE_COLORS.get(arch, "#aaaaaa")
        sizes = (sub["生命"] * 30).tolist()
        ax.scatter(sub["費用"], sub["總強度"],
                   s=sizes, c=color, alpha=0.85,
                   edgecolors="#ffffff", linewidths=0.4,
                   label=arch, zorder=3)

    # 卡牌名稱標註
    for _, row in df.iterrows():
        ax.annotate(row["名稱"], (row["費用"], row["總強度"]),
                    textcoords="offset points", xytext=(5, 3),
                    color=TEXT, fontsize=7, alpha=0.85)

    # Baseline 趨勢線：power = 1.80 × cost
    costs = np.linspace(0.5, 11, 100)
    ax.plot(costs, 1.80 * costs, "--", color="#E0A020", linewidth=1.5,
            label="基準線（費效比 = 1.80）", zorder=2)

    # Overpowered 帶：power > 2.25 × cost
    ax.fill_between(costs, 2.25 * costs, 4.0 * costs,
                    color=C_OVERPOWER, alpha=0.06, zorder=1)
    ax.text(1.0, 3.8, "過強區", color=C_OVERPOWER, fontsize=8, alpha=0.6)

    ax.set_xlabel("費用", color=TEXT, fontsize=11)
    ax.set_ylabel("總強度分數", color=TEXT, fontsize=11)
    ax.set_title("Iron & Gears ｜ 費用 vs 強度（點大小 = HP）", color=TEXT, fontsize=13, pad=12)
    ax.tick_params(colors=TEXT)
    ax.spines[:].set_color("#3a2010")
    ax.set_xlim(0, 11)
    ax.set_ylim(0, max(df["總強度"]) + 2)

    legend = ax.legend(facecolor="#2a1810", edgecolor="#3a2010",
                       labelcolor=TEXT, fontsize=9, loc="upper left")

    fig.tight_layout()
    out = output_dir / "chart_03_cost_vs_power.png"
    fig.savefig(out, dpi=140, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return out


def save_all_charts(df, output_dir: Path = None) -> list[Path]:
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "outputs" / "charts"
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = [
        plot_balance_scores(df, output_dir),
        plot_power_breakdown(df, output_dir),
        plot_cost_vs_power(df, output_dir),
    ]
    return paths

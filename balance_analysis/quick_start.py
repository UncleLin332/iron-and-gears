"""
Phase 1 入口：執行靜態卡牌平衡分析，輸出報告與三張圖表。

使用方式：
    cd balance_analysis
    python quick_start.py
"""

import sys
from pathlib import Path

# 確保 src/ 可被 import
sys.path.insert(0, str(Path(__file__).parent))

from src.cards import load_cards
from src.analyzer import build_dataframe, print_report
from src.visualizer import save_all_charts

CHARTS_DIR = Path(__file__).parent / "outputs" / "charts"


def main():
    print("\n載入卡牌資料…")
    cards = load_cards()
    print(f"✓ 共載入 {len(cards)} 張卡牌\n")

    df = build_dataframe(cards)
    print_report(df)

    print("產生圖表…")
    try:
        paths = save_all_charts(df, CHARTS_DIR)
        print(f"\n✓ 圖表已存入 outputs/charts/")
        for p in paths:
            print(f"   {p.name}")
    except Exception as e:
        print(f"\n⚠ 圖表產生失敗（{e}）")
        print("  請確認已安裝 matplotlib：pip install matplotlib")

    print()


if __name__ == "__main__":
    main()

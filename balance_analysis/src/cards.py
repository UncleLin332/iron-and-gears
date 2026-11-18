"""
卡牌資料模型與 Power Score 計算。

KEYWORD_POWER 是每個效果的「估算費用等價值」，
這些數值是理論估算，會在 Phase 3 模擬完成後進行校準。
"""

import json
from pathlib import Path

# ──────────────────────────────────────────────
#  效果估算值（單位：費用等價）
# ──────────────────────────────────────────────
KEYWORD_POWER = {
    # 部署效果 (battlecry)
    "draw1":        1.5,   # 抽1張牌 — 資源優勢，效果強
    "fuel1":        1.0,   # +1燃料 — 當回合節奏優勢
    "dmg2rand":     1.5,   # 對隨機敵方造成2傷 — 清除輔助
    "healfriendly": 1.2,   # 友方回復全血 — 情境性強
    "destroyhigh":  3.0,   # 摧毀攻擊≥5的敵方 — 強力單體移除
    "destroyall":   5.5,   # 摧毀所有敵方 — 終極清場，極高價值
    # 報廢效果 (deathrattle)
    "summon11":     1.0,   # 召喚1/1 — 一個小體
    "dmg3rand":     1.5,   # 對隨機敵方造成2傷（已調整）— 死亡觸發清除
    "draw2":        3.0,   # 抽2張牌 — 強力資源補充
    # 回合結束效果 (end_of_turn)
    "savefuel":     2.0,   # 儲存最多3燃料 — 後期爆發，情境性強
    "heal2self":    0.8,   # 自身回復2血 — 累積韌性，適合坦克
    "eot_draw1":    2.0,   # 每回合抽1張牌 — 持續資源補充，高價值
    # 新增報廢效果
    "dr_draw1":     1.5,   # 報廢：抽1張牌
    # 新增部署效果
    "dmg1all":      2.5,   # 對所有敵方手下各造成1傷 — 小AOE，清場輔助
}

TAUNT_POWER = 1.2   # 攔截的估算費用等價值

# 基準線：balance_score = 1.80 代表「標準平衡」
# 根據「普通的自走齒輪」(1費1/1) 標定：power/cost = 1.8/1 = 1.80
BALANCE_BASELINE = 1.80

# 警示門檻
OVERPOWERED_THRESHOLD  = BALANCE_BASELINE * 1.25   # balance > 2.25 → 可能過強
UNDERPOWERED_THRESHOLD = BALANCE_BASELINE * 0.90   # balance < 1.62 → 可能偏弱


def load_cards(json_path: str | Path = None) -> list[dict]:
    if json_path is None:
        json_path = Path(__file__).parent.parent / "data" / "cards.json"
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def base_power(card: dict) -> float:
    """純數值強度：攻擊力 + 生命值（生命略低估）"""
    return card["atk"] * 1.0 + card["hp"] * 0.8


def effect_bonus(card: dict) -> float:
    """所有效果的總估算價值"""
    bonus = 0.0
    if card.get("taunt"):
        bonus += TAUNT_POWER
    if card.get("battlecry") and card.get("bc_type"):
        bonus += KEYWORD_POWER.get(card["bc_type"], 0)
    if card.get("deathrattle") and card.get("dr_type"):
        bonus += KEYWORD_POWER.get(card["dr_type"], 0)
    if card.get("end_of_turn") and card.get("eot_type"):
        bonus += KEYWORD_POWER.get(card["eot_type"], 0)
    return bonus


def power_score(card: dict) -> float:
    """總強度分數 = 數值強度 + 效果強度"""
    return base_power(card) + effect_bonus(card)


def balance_score(card: dict) -> float:
    """費用效率 = power / cost（越高越強）"""
    return power_score(card) / max(card["cost"], 1)


def deviation(card: dict) -> float:
    """與基準線的偏差百分比，0% = 標準平衡"""
    return (balance_score(card) - BALANCE_BASELINE) / BALANCE_BASELINE


def keyword_tags(card: dict) -> list[str]:
    tags = []
    if card.get("taunt"):
        tags.append("攔截")
    if card.get("battlecry"):
        tags.append("部署")
    if card.get("deathrattle"):
        tags.append("報廢")
    if card.get("end_of_turn"):
        tags.append("回合結束")
    return tags


def archetype(card: dict) -> str:
    """簡單牌型分類"""
    bc = card.get("bc_type", "")
    dr = card.get("dr_type", "")
    has_taunt = card.get("taunt", False)

    if bc in ("destroyall", "destroyhigh"):
        return "清場"
    if bc in ("draw1",) or dr in ("draw2",):
        return "資源"
    if has_taunt and card["hp"] >= 5:
        return "控制"
    if card["cost"] <= 2:
        return "快攻"
    if card["cost"] >= 7:
        return "後期"
    return "中速"


def status_label(card: dict) -> str:
    bs = balance_score(card)
    if bs >= OVERPOWERED_THRESHOLD:
        return "⚠ 可能過強"
    if bs <= UNDERPOWERED_THRESHOLD:
        return "↓ 可能偏弱"
    return "✓ 平衡"

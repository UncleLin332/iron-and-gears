"""
Phase 3 多 AI 策略模組。

根據論文啟示（Emergent Complexity via Multi-Agent Competition）：
- 只用單一 AI 策略的模擬結果不可信
- 需要多元 AI 互打，才能發現真正的 meta 問題

實作三種核心 AI 策略，供 Phase 3 的 simulator.py 使用。
每種 AI 在出牌順序、攻擊目標選擇、保守/激進程度上各不相同。

設計依據：
- AggressiveAI  → 對應快攻牌型，優先出低費牌、直接攻擊英雄
- ControlAI     → 對應控制牌型，優先出攔截牌、清除場面
- BalancedAI    → 對應中速牌型，在兩者之間動態決策
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import random


# ──────────────────────────────────────────────
#  共用型別（Phase 2 Game Engine 建好後會用 import）
# ──────────────────────────────────────────────
# 以下型別是佔位符，Phase 2 完成後替換為正式類別

@dataclass
class CardStub:
    name: str
    cost: int
    atk: int
    hp: int
    max_hp: int = 0
    taunt: bool = False
    battlecry: bool = False
    bc_type: str = ""
    deathrattle: bool = False
    dr_type: str = ""
    end_of_turn: bool = False
    eot_type: str = ""
    tribe: str = ""
    has_attacked: bool = False
    is_sick: bool = True

@dataclass
class PlayerStub:
    name: str
    hp: int = 30
    fuel: int = 0
    deck: list = field(default_factory=list)
    hand: list = field(default_factory=list)
    board: list = field(default_factory=list)


# ──────────────────────────────────────────────
#  基礎 AI 類別
# ──────────────────────────────────────────────

class BaseAI:
    """所有 AI 策略的基類，定義共同介面。"""

    name: str = "BaseAI"

    def choose_card_to_play(self, player: PlayerStub, enemy: PlayerStub) -> Optional[CardStub]:
        """從手牌中選一張要出的牌。回傳 None 表示不出牌。"""
        affordable = [c for c in player.hand if c.cost <= player.fuel]
        if not affordable or len(player.board) >= 7:
            return None
        return self._select_card(affordable, player, enemy)

    def choose_attack_target(
        self, attacker: CardStub, enemy: PlayerStub
    ) -> tuple[Optional[CardStub], bool]:
        """
        選擇攻擊目標。
        回傳 (target_minion, attack_face)
        attack_face=True 表示直攻英雄。
        """
        taunts = [c for c in enemy.board if c.taunt]
        pool = taunts if taunts else enemy.board
        return self._select_target(attacker, pool, enemy)

    def _select_card(self, affordable: list, player: PlayerStub, enemy: PlayerStub) -> CardStub:
        raise NotImplementedError

    def _select_target(
        self, attacker: CardStub, pool: list, enemy: PlayerStub
    ) -> tuple[Optional[CardStub], bool]:
        raise NotImplementedError


# ──────────────────────────────────────────────
#  策略一：AggressiveAI（快攻型）
# ──────────────────────────────────────────────

class AggressiveAI(BaseAI):
    """
    快攻 AI：優先低費牌快速鋪場，盡早直攻英雄。

    出牌邏輯：
    - 優先有 battlecry 的低費牌
    - 其次是攻擊力最高的牌
    - 盡量在回合早期把燃料用光

    攻擊邏輯：
    - 若場面沒有攔截，直接攻英雄
    - 若有攔截，選攻擊力最低的攔截牌（最快打完）
    """

    name = "AggressiveAI"

    def _select_card(self, affordable: list, player: PlayerStub, enemy: PlayerStub) -> CardStub:
        # 按「攻擊力 DESC，費用 ASC」排序
        affordable.sort(key=lambda c: (-c.atk, c.cost))
        return affordable[0]

    def _select_target(
        self, attacker: CardStub, pool: list, enemy: PlayerStub
    ) -> tuple[Optional[CardStub], bool]:
        # 如果場上沒有攔截，直攻英雄
        if not [c for c in enemy.board if c.taunt] and pool == enemy.board:
            if enemy.hp <= attacker.atk:
                return None, True  # 可以直接殺
            return None, True  # 快攻 AI 總是優先打臉

        # 有攔截：打攻擊力最低的（最快清掉）
        if pool:
            target = min(pool, key=lambda c: c.atk)
            return target, False
        return None, True


# ──────────────────────────────────────────────
#  策略二：ControlAI（控制型）
# ──────────────────────────────────────────────

class ControlAI(BaseAI):
    """
    控制 AI：優先清除威脅，保持場面優勢，大卡後期收尾。

    出牌邏輯：
    - 優先有攔截（taunt）的牌
    - 其次是能清場的 battlecry 牌（destroyall/destroyhigh/dmg1all）
    - 最後才是高費大型手下

    攻擊邏輯：
    - 優先殺傷最高的敵方手下（最大威脅優先）
    - 只在對手已無手下時才攻英雄
    """

    name = "ControlAI"
    CLEAR_TYPES = {"destroyall", "destroyhigh", "dmg1all", "dmg2rand", "dmg3rand"}

    def _select_card(self, affordable: list, player: PlayerStub, enemy: PlayerStub) -> CardStub:
        # 優先有攔截
        taunts = [c for c in affordable if c.taunt]
        if taunts:
            return max(taunts, key=lambda c: c.hp)

        # 其次有清場 battlecry
        clears = [c for c in affordable if c.bc_type in self.CLEAR_TYPES]
        if clears and enemy.board:
            return max(clears, key=lambda c: c.cost)

        # 其次最高費用（大型手下）
        return max(affordable, key=lambda c: c.cost)

    def _select_target(
        self, attacker: CardStub, pool: list, enemy: PlayerStub
    ) -> tuple[Optional[CardStub], bool]:
        if not pool:
            return None, True

        # 優先殺掉能殺的
        killable = [t for t in pool if t.hp <= attacker.atk]
        if killable:
            return max(killable, key=lambda c: c.atk), False

        # 殺不掉：打攻擊力最高的（降低受傷風險）
        return max(pool, key=lambda c: c.atk), False


# ──────────────────────────────────────────────
#  策略三：BalancedAI（平衡型 / 中速）
# ──────────────────────────────────────────────

class BalancedAI(BaseAI):
    """
    平衡 AI：根據場面狀態動態在激進/保守間切換。

    評估「場面優勢指數」= 我方場面總 ATK+HP - 對方場面總 ATK+HP
    - 場面優勢大 → 激進打臉
    - 場面劣勢 → 保守清場
    - 均勢 → 出最高費效比的牌

    這是最接近「真實玩家決策」的 AI。
    """

    name = "BalancedAI"

    def _board_advantage(self, player: PlayerStub, enemy: PlayerStub) -> int:
        my_score    = sum(c.atk + c.hp for c in player.board)
        enemy_score = sum(c.atk + c.hp for c in enemy.board)
        return my_score - enemy_score

    def _select_card(self, affordable: list, player: PlayerStub, enemy: PlayerStub) -> CardStub:
        adv = self._board_advantage(player, enemy)

        if adv > 4:
            # 場面佔優：出費效比最高的（保持優勢）
            return max(affordable, key=lambda c: (c.atk + c.hp) / max(c.cost, 1))
        elif adv < -4:
            # 場面劣勢：優先攔截或清場
            taunts = [c for c in affordable if c.taunt]
            if taunts:
                return max(taunts, key=lambda c: c.hp)
            return max(affordable, key=lambda c: c.cost)
        else:
            # 均勢：費效比最高
            return max(affordable, key=lambda c: (c.atk + c.hp) / max(c.cost, 1))

    def _select_target(
        self, attacker: CardStub, pool: list, enemy: PlayerStub
    ) -> tuple[Optional[CardStub], bool]:
        if not pool:
            return None, True

        adv = sum(c.atk + c.hp for c in [attacker]) - sum(c.atk + c.hp for c in pool) / max(len(pool), 1)

        if adv > 0 and enemy.hp <= 10:
            # 對手血少：試圖打臉
            taunts_present = any(c.taunt for c in enemy.board)
            if not taunts_present:
                return None, True

        # 否則：殺能殺的，或打最高攻擊的
        killable = [t for t in pool if t.hp <= attacker.atk]
        if killable:
            return max(killable, key=lambda c: c.atk), False
        return max(pool, key=lambda c: c.atk), False


# ──────────────────────────────────────────────
#  AI 工廠
# ──────────────────────────────────────────────

AI_REGISTRY = {
    "aggressive": AggressiveAI,
    "control":    ControlAI,
    "balanced":   BalancedAI,
}

def get_ai(strategy: str = "balanced") -> BaseAI:
    """根據策略名稱回傳對應 AI 實例。"""
    cls = AI_REGISTRY.get(strategy, BalancedAI)
    return cls()


# ──────────────────────────────────────────────
#  快速驗證
# ──────────────────────────────────────────────

if __name__ == "__main__":
    for name, cls in AI_REGISTRY.items():
        ai = cls()
        print(f"✓ {ai.name} loaded")
    print(f"\n可用 AI 策略：{list(AI_REGISTRY.keys())}")
    print("Phase 2 完成後，將這裡的 CardStub/PlayerStub 替換為 cards.py 的正式類別")

# Iron & Gears 卡牌平衡分析系統 — 分階段計畫

更新日期：2026-06-09

---

## 可行性評估

**結論：完全可行，而且你已經完成最難的部分了。**

你目前在 `index.html` 裡已經有：

| 已有 | 對應 Python 需求 |
|---|---|
| `TEMPLATES` 卡牌資料 | 直接轉成 Python dict / dataclass |
| 戰鬥規則（combat、kill、deathrattle） | 用 Python 重新實作，速度快 100 倍 |
| AI 邏輯（aiPlay、aiAttackAll） | 直接移植，甚至可以做更強的 AI |
| 效果代碼系統（bcType / drType / eotType） | 很容易擴充 |
| 費用、攻擊、生命、關鍵字 | 直接拿來做統計特徵 |

**最大優勢：** Python 跑 10,000 場模擬大概只要幾秒鐘，瀏覽器跑同樣場數至少要幾小時。

---

## 專案結構

```
boardgame/
└── balance_analysis/
    ├── README.md
    ├── requirements.txt
    ├── data/
    │   └── cards.json              ← 從 index.html 匯出的卡牌資料
    ├── src/
    │   ├── cards.py                ← 卡牌 dataclass 與效果系統
    │   ├── game.py                 ← Python 版遊戲引擎
    │   ├── simulator.py            ← 大量對戰模擬器
    │   ├── analyzer.py             ← 統計分析與平衡分數
    │   └── visualizer.py          ← matplotlib / plotly 圖表
    ├── notebooks/
    │   └── exploration.ipynb       ← Jupyter 互動分析
    └── dashboard/
        └── app.py                  ← Streamlit 視覺化儀表板
```

---

## 第一階段：卡牌資料分析（建議起點）

**目標：** 不跑任何模擬，只用數學評估每張卡的理論強度。

### 核心概念：Card Power Score

```python
def card_power_score(card):
    score = 0
    score += card['atk'] * 1.0   # 攻擊力
    score += card['hp']  * 0.8   # 生命值（防守價值略低）
    if card.get('taunt'):         score += 1.2  # 攔截
    if card.get('battlecry'):
        bcType = card.get('bcType', '')
        if bcType == 'draw1':       score += 1.5
        if bcType == 'fuel1':       score += 1.0
        if bcType == 'dmg2rand':    score += 1.5
        if bcType == 'healfriendly': score += 1.2
        if bcType == 'destroyhigh': score += 3.0
        if bcType == 'destroyall':  score += 5.0
    if card.get('deathrattle'):
        drType = card.get('drType', '')
        if drType == 'summon11':    score += 1.0
        if drType == 'dmg3rand':    score += 2.0
        if drType == 'draw2':       score += 3.0
    if card.get('endOfTurn'):
        eotType = card.get('eotType', '')
        if eotType == 'savefuel':   score += 2.0
        if eotType == 'heal2self':  score += 0.8
    return score

def balance_score(card):
    """費用效率：越高越強，1.0 是理論平衡點"""
    return card_power_score(card) / max(card['cost'], 1)
```

### 輸出範例

```
卡牌名稱           費用  攻擊  生命  Power  Balance
普通的自走齒輪      1     1     1    1.8    1.80  ← 剛好合理
蒸氣飛艇            1     1     1    3.3    3.30  ← 有抽牌，爆強
工坊防禦核心        7     4     8    13.0   1.86  ← 大卡但合理
核子平行迫擊炮      8     7     7    19.2   2.40  ← 可能太強
```

### 分析圖表（Phase 1 輸出）

- **費用 vs Power Score 散點圖**：找出高於回歸線的超模卡
- **Balance Score 橫條圖**：一眼看出哪張卡效率最高
- **關鍵字價值分解圖**：每個效果貢獻了多少 power

---

## 第二階段：Python 遊戲引擎

**目標：** 把 `index.html` 的 JS 遊戲邏輯用 Python 重新實作，為大量模擬做準備。

### 核心架構

```python
from dataclasses import dataclass, field
from typing import Optional
import random

@dataclass
class Card:
    name: str
    cost: int
    atk: int
    hp: int
    max_hp: int = 0
    text: str = ""
    taunt: bool = False
    battlecry: bool = False
    bc_type: str = ""
    deathrattle: bool = False
    dr_type: str = ""
    end_of_turn: bool = False
    eot_type: str = ""
    has_attacked: bool = False
    is_sick: bool = True   # 召喚失調

@dataclass
class Player:
    name: str
    hp: int = 30
    fuel: int = 0
    max_fuel: int = 0
    deck: list = field(default_factory=list)
    hand: list = field(default_factory=list)
    board: list = field(default_factory=list)
    fatigue: int = 0

class GameEngine:
    def __init__(self, deck_a, deck_b):
        self.player = Player("Player", deck=deck_a)
        self.ai = Player("AI", deck=deck_b)
        self.turn = 1
        self.log = []
    
    def run_game(self):
        """執行完整一局，回傳 'player' 或 'ai'"""
        ...
```

### 重點：AI 策略等級

根據研究論文（Emergent Complexity, MARL Review），必須使用**多種 AI 策略**互打，才能發現真正的 meta 問題：

```python
# 已實作於 src/ai_strategies.py
from src.ai_strategies import AggressiveAI, ControlAI, BalancedAI, get_ai

# AggressiveAI  — 優先低費鋪場，直攻英雄
# ControlAI     — 優先攔截/清場，大卡後期收尾
# BalancedAI    — 根據場面優勢動態決策（最接近真實玩家）
```

**為什麼需要多種 AI（論文依據）：**
- *Emergent Complexity*：只對抗單一策略會讓模擬收斂到假 meta，真正危險的 combo 不會被發現
- *MARL Review*：Population-based training 要求對手多元化，才能揭示跨策略的平衡問題

---

## 第三階段：大量模擬器（多 AI 版）

**目標：** 三種 AI 策略 9 種對戰組合，各跑 3000 場，共 27,000 場，統計每張卡的真實跨策略表現。

### 模擬器核心

```python
def simulate(n_games=3000, ai_a='aggressive', ai_b='control'):
    ai_player = get_ai(ai_a)
    ai_enemy  = get_ai(ai_b)
    results = {
        'winner': [], 'turns': [],
        'cards_played': [],   # 每局哪些牌被出過
        'cards_killed': [],   # 每局哪些牌被消滅
        'ai_matchup': f'{ai_a}_vs_{ai_b}',
    }
    for _ in range(n_games):
        engine = GameEngine(shuffle(deck.copy()), shuffle(deck.copy()),
                            player_ai=ai_player, enemy_ai=ai_enemy)
        result = engine.run_game()
        results['winner'].append(result.winner)
        results['turns'].append(result.turns)
        results['cards_played'].extend(result.cards_played)
    return pd.DataFrame(results)

# 執行 9 種對戰組合
STRATEGIES = ['aggressive', 'control', 'balanced']
all_results = []
for ai_a in STRATEGIES:
    for ai_b in STRATEGIES:
        all_results.append(simulate(3000, ai_a, ai_b))
full_df = pd.concat(all_results)
```

### 新增：族群共鳴追蹤

Phase 3 要額外追蹤族群共鳴效果的觸發率，評估各族群是否平衡：

```python
# 追蹤每次族群共鳴觸發
tribe_synergy_log = {
    '天穹': {'triggers': 0, 'wins_with': 0},
    '地下': {'triggers': 0, 'wins_with': 0},
    '破浪': {'triggers': 0, 'wins_with': 0},
    '發條': {'triggers': 0, 'wins_with': 0},
    '林大師': {'triggers': 0, 'wins_with': 0},
}
```

### 統計輸出範例

```
卡牌             出場率   勝場率   平均存活回合   跨策略偏差
蒸汽狙擊手        82%      61%       2.1            低（各策略間勝率差 < 8%）
工坊防禦核心      45%      73%       4.2            中（控制 AI 勝率 85% vs 快攻 AI 60%）
普通的自走齒輪    95%      48%       1.4            低（炮灰，但各策略一致）
不穩定電能炸彈    67%      55%       0.8            高（對快攻AI有奇效）← 值得關注

族群共鳴觸發分析：
天穹族   觸發 847 次，勝率 +12%   → 可能過強
地下族   觸發 234 次，勝率 +3%    → 平衡
破浪族   觸發 156 次，勝率 +5%    → 平衡
發條族   觸發 412 次，勝率 +8%    → 合理
```

### 關鍵分析：哪些卡組合最危險

```python
def find_dangerous_combos(games_df, min_winrate=0.65):
    """找出兩張卡同時在場時勝率異常高的組合"""
    combos = []
    for game in games_df:
        for pair in combinations(game.cards_in_winning_board, 2):
            combos.append(pair)
    return analyze_combo_winrates(combos, min_winrate)
```

---

## 第四階段：Streamlit 視覺化儀表板

**目標：** 做成一個可互動的網頁工具。

### 功能清單

```
📊 概覽頁
├── 所有卡牌的 Balance Score 橫條圖
├── 費用分布圓餅圖
└── 效果類型分布

⚔️ 模擬頁
├── 選擇牌組 A vs 牌組 B
├── 設定模擬場數（100 / 1000 / 10000）
├── 跑完後顯示：勝率、平均回合數、關鍵卡牌
└── 勝率走勢折線圖（每100場一個點）

🃏 卡牌分析頁
├── 搜尋/篩選卡牌
├── 點擊卡牌看詳細統計
├── 費用 vs 強度散點圖（可選 X / Y 軸）
└── 與其他卡牌比較

⚠️ 危險組合頁
├── 顯示勝率 > 閾值的卡牌組合
└── Nerf 建議（自動推算數值調整）

🔮 新卡預測頁
├── 輸入新卡數值
├── 自動計算 Power Score
├── 預測加入後對 meta 的影響
└── Danger Level 警示
```

### 啟動方式

```bash
cd balance_analysis
pip install -r requirements.txt
streamlit run dashboard/app.py
```

---

## 第五階段（進階）：新卡發行預測系統

**目標：** 輸入一張尚未發布的新卡，預測它是否會搞壞 meta。

### 預測流程

```python
def evaluate_new_card(new_card, existing_cards, n_sim=5000):
    """
    1. 把新卡加入卡池
    2. 重跑 5000 場模擬
    3. 比較加入前後各張卡的勝率變化
    4. 若任何卡的勝率變化超過 ±10%，發出警告
    """
    baseline = simulate(n_sim, existing_cards)
    with_new  = simulate(n_sim, existing_cards + [new_card])
    
    delta = compare_winrates(baseline, with_new)
    return {
        'new_card_winrate': delta[new_card.name],
        'meta_disruption': delta.max(),
        'danger_level': classify_danger(delta),
        'recommendations': suggest_nerf(new_card, delta),
    }
```

### 自動 Nerf 建議

```python
def suggest_nerf(card, winrate_delta):
    suggestions = []
    if winrate_delta > 0.10:
        if card.atk > 2:
            suggestions.append(f"ATK: {card.atk} → {card.atk - 1}")
        if card.battlecry and card.bc_type in ['destroyall', 'destroyhigh']:
            suggestions.append(f"Cost: {card.cost} → {card.cost + 1}")
    return suggestions
```

---

## 第六階段（最高級）：Meta 演化模擬

**目標：** 模擬「玩家會如何適應 meta」，預測環境的自然演化。

### 概念

```python
def simulate_meta_evolution(n_generations=20, n_games_per_gen=1000):
    """
    每一代：
    1. 所有卡組互打
    2. 勝率高的卡組下一代更常被使用
    3. 玩家開始加入「剋制強卡」的卡牌
    4. Meta 逐漸收斂或持續演化
    """
    population = generate_initial_decks()
    history = []
    for gen in range(n_generations):
        results = run_tournament(population)
        history.append(results)
        population = evolve_population(population, results)
    return history
```

### 輸出：Meta 演化圖

```
回合   快攻佔比   控制佔比   大型手下佔比
1      40%        30%        30%
5      55%        25%        20%    ← 快攻主導
10     35%        45%        20%    ← 控制反制快攻
15     30%        30%        40%    ← 後期大卡重新崛起
20     25%        35%        40%    ← 環境穩定
```

---

## 建議執行順序

```
Week 1  第一階段：卡牌資料 + Power Score 計算
Week 2  第二階段：Python 遊戲引擎（最花時間）
Week 3  第三階段：跑 10,000 場模擬 + 基礎統計
Week 4  第四階段：Streamlit Dashboard
之後    第五、六階段看狀況，可以各花 1-2 週
```

---

## 技術棧

| 用途 | 套件 |
|---|---|
| 資料處理 | `pandas`, `numpy` |
| 圖表 | `matplotlib`, `seaborn`, `plotly` |
| 互動儀表板 | `streamlit` |
| 機率模擬 | Python `random`, `itertools` |
| 資料驗證 | `dataclasses`, `pydantic`（可選） |
| Notebook 探索 | `jupyter` |

```bash
# requirements.txt
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
plotly>=5.14
streamlit>=1.24
jupyter
```

---

## 最低可行版本（第一天就能跑起來）

就算只做這樣，也已經非常有價值：

```python
# balance_analysis/quick_start.py
import pandas as pd
import matplotlib.pyplot as plt

CARDS = [
    {"name":"原型蒸汽壓路機", "cost":4, "atk":4, "hp":5},
    {"name":"熱心的工坊學徒", "cost":2, "atk":2, "hp":2, "deathrattle":True},
    # ... 其他卡牌
]

df = pd.DataFrame(CARDS)
df['power'] = df['atk'] + df['hp'] * 0.8
df['efficiency'] = df['power'] / df['cost']

df.sort_values('efficiency', ascending=False).plot.barh(x='name', y='efficiency')
plt.title('Card Efficiency (Power / Cost)')
plt.tight_layout()
plt.show()
```

這 20 行就能看到你的第一張卡牌平衡圖。

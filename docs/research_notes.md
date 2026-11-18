# Iron & Gears 研究筆記

整理日期：2026-06-11

---

## 論文清單

| 檔案 | 標題 | 年份 | 關聯性 |
|---|---|---|---|
| `2502.07128v2.pdf` | Cardiverse: Harnessing LLMs for Novel Card Game Prototyping | 2025 | Phase 5 新卡生成 |
| `A_Comprehensive_Review...pdf` | Comprehensive Review of MARL in Video Games | 2025 | Phase 3 模擬設計 |
| `EMERGENT COMPLEXITY...pdf` | Emergent Complexity via Multi-Agent Competition | 2018 | Phase 3 AI 多元化 |
| `Steinboeck...pdf` | Game Design Patterns in Digital Card Games | 2017 | 遊戲設計改善 |

---

## 論文一：Steinböck — 數位卡牌遊戲設計模式（最直接相關）

### 核心主張
卡牌遊戲的平衡與趣味來自「設計模式的組合方式」，而非單一數值調整。Pattern 組合有乘法效應。

### 11 大設計模式分類
1. **Continuity patterns** — 回合制、事件觸發、跳入式
2. **Player interaction patterns** — 出牌、虛張聲勢、釣魚
3. **Trick patterns** — 王牌剋制、戰鬥、揭露、跟牌
4. **Pile patterns** — 手牌、抽牌堆、棄牌堆、得分堆
5. **Card patterns** — 花色、點數、萬能牌、**Combo 組合**
6. **Marking patterns** — 選擇、計數
7. **Deck patterns** — 標準牌堆、**組牌（Deck-building）**
8. **Ranking patterns** — 排名機制
9. **Meta-patterns** — 只出手牌、故事模式、非同步遊戲

### Iron & Gears 現況對照

| 模式 | 現況 | 缺少/改善方向 |
|---|---|---|
| Draw Pile + Hand + Battlefield | ✅ 已有 | — |
| Turn-based continuity | ✅ 已有 | — |
| Cost/Resource system | ✅ 已有 | — |
| Battlecry/Deathrattle combo | ✅ 基礎有 | 缺乏**跨卡互動**的 Combo |
| Mulligan / Starting hand control | ❌ 沒有 | 玩家沒有前期決策 → **已加入** |
| Tribe / Counter synergy | ❌ 沒有 | 沒有族群剋制 → **已加入族群共鳴** |
| Information asymmetry | 部分有 | 沒有「窺視手牌」類卡牌 |
| Deck-building | ❌ 純隨機 | 玩家組牌是最高影響力的改善 |
| Graveyard interactions | ❌ 沒有 | 報廢效果目前只是單次觸發 |

### 對本專案的直接行動
1. ✅ **換牌階段（Mulligan）** — 已實作：遊戲開始前可更換最多 3 張手牌
2. ✅ **族群共鳴（Tribe Synergy）** — 已實作：20 張卡加入族群標籤，同族群第二張上場時抽牌
3. 🔜 **未來優先考慮**：讓玩家在遊戲開始前選擇 5 張「必帶牌」，其餘隨機補足

---

## 論文二：Emergent Complexity via Multi-Agent Competition（OpenAI, 2018）

### 核心發現
> 「環境複雜度 ≠ 行為複雜度；競爭壓力本身就是課程設計。」

簡單規則 + 競爭選擇 → 自然產生複雜策略，不需要手動設計複雜度。

### 關鍵實驗結論
- 訓練時只對抗最強對手 → 某一方早期主導，導致另一方停止進步
- **訓練時對抗歷史上所有不同強度的對手** → 雙方持續進步，出現更多元策略
- Dense reward 早期 + Sparse reward 後期的組合學習效果最佳
- 出現了「設計師沒有設計的行為」：躲避、誘騙、防守陣型

### 對 Phase 3 模擬的直接啟示
1. **必須使用多種 AI 策略**，不能只跑一種 greedy AI
2. **AI 對手池要包含過去所有版本**，防止一種策略主導整個評估
3. **如果模擬只出現一種 meta** → 說明牌庫設計缺乏多元性，需要補充新牌型

---

## 論文三：MARL Review（IEEE, 2025）

### 核心主張
多智能體強化學習（MARL）中，Self-play 是讓 AI 發現遊戲平衡問題的黃金標準。AlphaGo、AlphaStar、OpenAI Five 都基於此原理。

### 對本專案最有用的三個概念

**1. Population-based Training（族群訓練）**
多個 AI 族群同時互打，而不是兩個固定 AI。能發現更廣泛的 meta 問題。

**2. CTDE（Centralized Training, Decentralized Execution）**
訓練時可以看全局狀態，執行時只用部分資訊。→ 分析時允許 AI 看對手所有牌，但決策時只用正常規則。

**3. Credit Assignment**
評估時要區分「這場勝利是哪張牌造成的」。→ Phase 3 要追蹤每張牌的實際貢獻，不只記錄勝敗。

### Phase 3 實作建議
- 至少實作 3 種 AI 策略（見 `balance_analysis_plan.md` 的 Phase 3 章節）
- 每種 AI 策略打 3000+ 場，確保統計顯著性
- 追蹤每張牌的「勝場出現率」和「敗場出現率」，計算真正的貢獻分

---

## 論文四：Cardiverse（2025）— 未來參考用

### 核心架構
LLM → 自動生成卡牌設計 → 模擬評估 → 淘汰過強/過弱 → 輸出平衡候選卡牌

### 對本專案的啟示
1. 驗證了「模擬篩選新卡」的方向完全正確（他們用 LLM 生成，我們用人工設計）
2. Self-reflection validation 的概念：用模擬結果反過來校準效果估算值（即 Phase 3 之後反饋給 KEYWORD_POWER）
3. **Phase 5 可以考慮**：用 LLM API 生成候選新卡 → 用 Phase 3 模擬評估 → 人工審查

---

## 行動優先序

| 優先度 | 行動 | 來自哪篇論文 |
|---|---|---|
| ✅ 已完成 | 加入 Mulligan 換牌階段 | Steinböck |
| ✅ 已完成 | 加入族群共鳴系統 | Steinböck |
| 🔜 Phase 3 | 實作三種 AI 策略：快攻/控制/平衡 | Emergent Complexity |
| 🔜 Phase 3 | Population-based evaluation | MARL Review |
| 🔜 Phase 3 | 追蹤每張牌的實際貢獻分 | MARL Review |
| 🔮 Phase 5 | 用模擬回調校準 KEYWORD_POWER 值 | Cardiverse |
| 🔮 未來 | 加入組牌選擇（Deck-building lite） | Steinböck |

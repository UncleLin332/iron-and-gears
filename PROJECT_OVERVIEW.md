# Iron & Gears 專案統整

更新日期：2026-06-09

## 專案概述

這個專案是一個以《鐵律與齒輪 / Iron & Gears》為主題的單人卡牌對戰原型。玩法方向接近爐石式手下交換遊戲：玩家「林工程師」對戰「自動化AI」，雙方有生命值、燃料、牌庫、手牌、戰場、疲勞傷害與卡牌效果。

目前專案主體是純前端 HTML/CSS/JavaScript，不需要建置流程即可在瀏覽器中開啟。

## 開啟遊戲

直接用瀏覽器開啟 `index.html`。

若要用本機伺服器測試，可在專案根目錄執行：

```bash
python3 -m http.server 8765
```

再開啟：`http://localhost:8765/`

---

## 資料夾結構

```
boardgame/
├── index.html              ← 主遊戲檔案（唯一需要更新的 HTML）
├── ADD_CARD_GUIDE.md       ← 新增卡牌流程指南
├── PROJECT_OVERVIEW.md     ← 本文件
│
├── assets/
│   ├── card-art/           ← 卡牌 PNG 圖片（共 16 張）
│   └── music/              ← 音樂引擎與編曲
│       ├── music.js
│       └── music2.js
│
├── scripts/
│   └── build_card_catalog.mjs   ← 產生 Excel 卡牌目錄的工具
│
├── outputs/
│   └── card_catalog/
│       └── iron_and_gears_card_catalog.xlsx  ← 自動產生的卡牌清單
│
├── docs/                   ← 設計筆記與歷史記錄
│   ├── knowledge/
│   ├── update_history/
│   └── PNG檔案新增方法.md
│
└── archive/                ← 早期版本（不需更動）
    ├── iron_and_gears_version2.html ~ version6.html
    └── prototype/
```

---

## 主要檔案說明

### index.html

目前唯一的主線遊戲版本。包含：

- 遊戲 UI、CSS 樣式
- `const TEMPLATES = [...]`：卡牌資料（第 170 行附近）
- `const CARD_ART = {...}`：卡名對應圖片路徑（第 749 行附近）
- 遊戲邏輯、AI、卡牌效果、動畫
- 透過 `<script src="assets/music/music.js">` 載入音樂引擎

### assets/card-art/

存放卡牌 PNG 圖片，目前共 16 張：

```
原型蒸氣壓路機.png  熱心的工坊學徒.png  報廢蒸氣巨獸.png  王牌拆解手.png
巨型時鐘巨靈.png    普通的自走齒輪.png  蒸氣飛艇.png      機油回收幫浦.png
不穩定電能炸彈.png  壓力閥盾衛.png      齒輪超載者.png    蒸氣狙擊手.png
自動化維修機.png    巨型合金破城者.png  工坊防禦核心.png  核子平行迫擊炮.png
```

新增卡圖只需把 PNG 放進這個資料夾，再在 `index.html` 的 `CARD_ART` 加一行即可。

### assets/music/

- `music.js`：Web Audio 引擎，建立 AudioContext、節點、合成音色。
- `music2.js`：目前版本的編曲與旋律排程。

---

## 遊戲規則與功能

- 玩家與 AI 各 30 點生命。
- 每回合燃料上限逐步增加，最多 10。
- 牌庫、手牌、抽牌、手牌上限與疲勞傷害。
- 場上手下最多 7 個。
- 手下召喚失調與每回合攻擊一次限制。
- 攔截（必須優先攻擊機制）。
- AI 自動出牌與選擇攻擊目標。
- 勝負畫面與重新開始。
- 遊戲紀錄 log、傷害飄字、卡牌放大預覽、背景音樂開關。

---

## 卡牌資料

卡牌資料集中在 `index.html` 內的 `const TEMPLATES = [...]`，共 16 張，從全部模板隨機抽取組成 30 張牌庫。

### 原版六張

原型蒸汽壓路機、熱心的工坊學徒、報廢蒸氣巨獸、王牌拆解手、巨型時鐘巨靈、普通的自走齒輪

### 新增十張

蒸氣飛艇、機油回收幫浦、不穩定電能炸彈、壓力閥盾衛、齒輪超載者、蒸汽狙擊手、自動化維修機、巨型合金破城者、工坊防禦核心、核子平行迫擊炮

---

## 卡牌效果系統

| 種類 | 開關欄位 | 代碼欄位 | 現有代碼 |
|---|---|---|---|
| 部署（battlecry） | `battlecry:true` | `bcType` | `draw1` / `fuel1` / `dmg2rand` / `healfriendly` / `destroyall` / `destroyhigh` |
| 報廢（deathrattle） | `deathrattle:true` | `drType` | `summon11` / `dmg3rand` / `draw2` |
| 回合結束（endOfTurn） | `endOfTurn:true` | `eotType` | `savefuel` / `heal2self` |
| 攔截 | `taunt:true` | — | — |

詳細新增流程見 `ADD_CARD_GUIDE.md`。

---

## Excel 卡牌目錄

`outputs/card_catalog/iron_and_gears_card_catalog.xlsx` 由 `scripts/build_card_catalog.mjs` 自動產生，**不是手動維護的檔案**。

新增卡牌後執行：

```bash
node scripts/build_card_catalog.mjs
```

---

## 部署注意事項

若要上傳到 GitHub Pages、Netlify、Vercel 等靜態空間，需一起部署：
- `index.html`
- `assets/` 資料夾（含 `card-art/` 與 `music/`）

目前卡圖使用中文檔名，瀏覽器可以處理。若未來遇到 URL 編碼問題，可考慮改為英文小寫路徑（如 `steam-sniper.png`）並同步更新 `CARD_ART`。

---

## 附屬專案：卡牌平衡分析系統（Python）

詳細計畫見 [`docs/balance_analysis_plan.md`](docs/balance_analysis_plan.md)。

**目標：** 用 Python 模擬大量對戰，找出過強/過弱的卡牌，並預測新卡對 meta 的影響。

### 六個階段概覽

| 階段 | 內容 | 技術 | 預計時間 |
|---|---|---|---|
| 1 | 卡牌資料分析、Power Score、效率圖 | pandas, matplotlib | Week 1 |
| 2 | Python 版遊戲引擎（移植 JS 邏輯） | dataclasses, Python | Week 2 |
| 3 | 10,000 場自動模擬、勝率統計、危險 combo 偵測 | random, pandas | Week 3 |
| 4 | Streamlit 互動儀表板 | streamlit, plotly | Week 4 |
| 5 | 新卡發行預測、自動 Nerf 建議 | 統計分析 | 之後 |
| 6 | Meta 演化模擬（AI 自己形成環境） | 演化演算法 | 之後 |

### 最低可行版本（Day 1 就能跑）

```bash
cd balance_analysis
pip install pandas matplotlib
python quick_start.py
```

20 行 Python 就能輸出第一張卡牌效率圖。

### 專案資料夾

```
balance_analysis/
├── data/cards.json
├── src/cards.py  game.py  simulator.py  analyzer.py
├── notebooks/exploration.ipynb
└── dashboard/app.py
```

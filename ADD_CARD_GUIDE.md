# 新增卡牌流程指南

更新對象：`index.html`

---

## 概覽

新增一張卡牌最多需要修改 **3 個地方**（純數值卡只需要 2 個），完成後還需要重新產生 Excel 目錄：

| 步驟 | 位置 | 必要？ |
|---|---|---|
| 把 PNG 放進 `assets/card-art/` | 資料夾操作 | 有圖才需要 |
| `TEMPLATES` 加一行 | `index.html` 第 170 行附近 | **必要** |
| `CARD_ART` 加一行 | `index.html` 第 749 行附近 | 有 PNG 才需要 |
| 對應 `switch` 加 `case` | 第 398 / 425 / 474 行 | 用新效果代碼才需要 |
| 重新執行 build script 產生 Excel | `scripts/build_card_catalog.mjs` | 要更新目錄才需要 |

卡牌從全部模板隨機抽取組成 30 張牌庫，新增後無需其他設定即會出現在遊戲中。

---

## 第一步：準備 PNG 圖片（可選）

把卡圖放進 `assets/card-art/` 資料夾，檔名建議直接使用卡牌中文名：

```
assets/card-art/新卡牌名稱.png
```

沒有 PNG 也沒關係，系統會自動以 SVG 佔位圖代替，樣式由 `portrait` 欄位決定。

---

## 第二步：在 `TEMPLATES` 加一筆卡牌資料

位置：`index.html` 第 170 行的 `const TEMPLATES = [...]`

```js
{ name:"新卡牌名稱", cost:3, atk:3, hp:4, text:"效果說明文字",
  portrait:"worker",
  tribe:"天穹",              // 可選，沒有族群就省略
  battlecry:true, bcType:"draw1"   // 有效果才加，沒有就全部不寫
},
```

### 族群（tribe）系統

加入 `tribe` 欄位後，當玩家部署第二張相同族群的手下時會自動觸發**族群共鳴**：抽一張牌。

| 族群名稱 | 現有成員 | 特色 |
|---|---|---|
| `"天穹"` | 天穹補給站、天穹工程師·艾莉、天穹建築師·戈登、天穹聯邦學院、天穹導航員·奧莉薇亞、聯邦首席機關師·諾拉 | 資源型，多 eot_draw1 |
| `"地下"` | 坑道照明工·索羅、地下甜點師·瑪拉、地下大廚·霍夫、地底偵查官·瓦萊麗 | 快攻型，低費鋪場 |
| `"破浪"` | 破浪號大副·凱特、黃銅破浪號、黑煙港的走私巨頭、聲納監聽官·薇薇安 | 海洋/港口主題，中後期 |
| `"發條"` | 多工發條助理、黃銅發條執事、發條先知·卡斯托爾、發條先知·波魯克斯 | 機械主題，均衡 |
| `"林大師"` | 林大師的機械寵物、龍紋機關師·林大師 | 稀有傳說組合，觸發強力但難湊齊 |

新設計一個族群建議至少有 **3–4 張成員**，才能讓族群共鳴在隨機牌庫中合理觸發。

### 可用的 `portrait` 值

| 值 | 外觀風格 |
|---|---|
| `gear` | 灰藍色、齒輪符號 |
| `worker` | 深綠色、人形輪廓 |
| `roller` | 棕橙色、壓路機輪廓 |
| `beast` | 深藍紫、怪物輪廓 |
| `wrench` | 深紅色、扳手符號 |
| `clock` | 深紫色、時鐘符號 |

### 卡牌效果欄位對照

| 效果種類 | 開關欄位 | 代碼欄位 | 現有代碼 |
|---|---|---|---|
| 部署（battlecry） | `battlecry:true` | `bcType:"..."` | `draw1` / `fuel1` / `dmg2rand` / `healfriendly` / `destroyall` / `destroyhigh` |
| 報廢（deathrattle） | `deathrattle:true` | `drType:"..."` | `summon11` / `dmg3rand` / `draw2` |
| 回合結束（endOfTurn） | `endOfTurn:true` | `eotType:"..."` | `savefuel` / `heal2self` |
| 攔截（taunt） | `taunt:true` | —（不需要代碼） | — |

效果可以組合，例如同時有攔截與報廢效果：

```js
{ name:"不穩定電能炸彈", cost:2, atk:0, hp:2,
  text:"攔截，報廢：對隨機敵方手下造成 3 傷害",
  portrait:"gear",
  taunt:true, deathrattle:true, drType:"dmg3rand"
},
```

---

## 第三步：在 `CARD_ART` 加圖片路徑（有圖時才需要）

位置：`index.html` 第 749 行附近的 `const CARD_ART = {...}`

```js
"新卡牌名稱": "assets/card-art/新卡牌名稱.png",
```

若沒有加這行，會自動 fallback 到 SVG 佔位圖，不會出錯。

---

## 第四步：新增全新效果邏輯（用新代碼才需要）

若 `bcType` / `drType` / `eotType` 使用了現有清單以外的代碼，需要在對應函式的 `switch` 裡加一個 `case`。

### 部署效果 — `doBattlecry()`（第 425 行附近）

```js
case 'heal3hero':
  owner.hp = Math.min(owner.hp + 3, 30);
  log(`💚 ${c.name} 部署效果：英雄回復 3 點生命！`, tag);
  break;
```

### 報廢效果 — `killCard()`（第 398 行附近）

```js
case 'summon22':
  if(owner.board.length < 7) {
    const t = makeCard({name:"強化陷阱", cost:0, atk:2, hp:2, text:"", portrait:"gear"});
    t.isSick = true; owner.board.push(t);
    log(`⚙ ${c.name} 報廢效果：召喚一個2/2強化陷阱！`, tag);
  }
  break;
```

### 回合結束效果 — `handleEndOfTurnEffects()`（第 474 行附近）

```js
case 'dmg1allenemy':
  for(const t of [...enemy.board]) {
    t.hp -= 1;
    if(t.hp <= 0) { log(`💀 ${t.name} 報廢了！`, "death"); killCard(t, enemy, who); }
  }
  log(`🔥 ${c.name} 回合結束：對所有敵方手下造成 1 點傷害！`, tag);
  break;
```

---

## 完整範例：從零新增一張卡

以「蒸氣哨兵」為例：3 費、2/4、攔截、報廢抽一張牌。

**1. 放入圖片：**
```
assets/card-art/蒸氣哨兵.png
```

**2. 在 `TEMPLATES` 新增：**
```js
{ name:"蒸氣哨兵", cost:3, atk:2, hp:4, text:"攔截，報廢：抽一張牌",
  portrait:"beast",
  taunt:true, deathrattle:true, drType:"draw1dr"
},
```

**3. 在 `CARD_ART` 新增：**
```js
"蒸氣哨兵": "assets/card-art/蒸氣哨兵.png",
```

**4. 在 `killCard()` 加新 `case`（`draw1` 是部署代碼，報廢用不同命名以示區別）：**
```js
case 'draw1dr':
  drawCard(owner, true);
  log(`📥 ${c.name} 報廢效果：抽了一張牌！`, tag);
  break;
```

---

## 第五步：重新產生 Excel 卡牌目錄

新增卡牌後，在專案根目錄執行：

```bash
node scripts/build_card_catalog.mjs
```

`outputs/card_catalog/iron_and_gears_card_catalog.xlsx` 即會包含最新的卡牌清單與統計摘要。

---

## 注意事項

- **Excel 目錄不會自動同步**：需要手動執行 script 才會更新。
- **場上手下上限**：`summon` 類報廢效果必須先檢查 `owner.board.length < 7`，否則會超出上限。
- **`isSick`**：召喚出來的手下若要讓它當回合無法攻擊，記得設定 `trap.isSick = true`。
- **效果代碼命名**：部署與報廢的「抽一張牌」建議用不同代碼名（如 `draw1` vs `draw1dr`）避免 `switch` 混用。

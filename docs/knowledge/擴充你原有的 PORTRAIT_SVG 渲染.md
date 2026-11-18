**擴充你原有的 `PORTRAIT_SVG` 渲染引擎**！

目前代碼的寫法非常聰明，是利用 `portrait` 屬性（如 `"gear"`, `"worker"`, `"clock"` 等）當作 Key，再去呼叫對應的 SVG 向量繪圖函數。

為了讓 16 張卡牌都有獨一無二的專屬「鋼鐵工坊風」美術，我幫你把原有的 `PORTRAIT_SVG` 重新擴充。我精細調整了 SVG 的幾何線條、顏色比例與發光特效，讓每張新卡牌都能完美貼合它的技能敘述：

### **🎨 替換用的全新 `PORTRAIT_SVG` 物件**

請你在 HTML 檔案中找到原本的 `const PORTRAIT_SVG = { ... };`，將它**整段替換**成以下代碼：

JavaScript  
const PORTRAIT\_SVG \= {  
  // ── 經典原版 ──  
  gear: s=\>\`\<circle cx="${s/2}" cy="${s/2}" r="${s\*.25}" fill="none" stroke="\#6a6a82" stroke-width="2"/\>  
    \<circle cx="${s/2}" cy="${s/2}" r="${s\*.08}" fill="\#6a6a82"/\>  
    \<line x1="${s/2}" y1="${s\*.18}" x2="${s/2}" y2="${s\*.34}" stroke="\#6a6a82" stroke-width="2"/\>  
    \<line x1="${s/2}" y1="${s\*.66}" x2="${s/2}" y2="${s\*.82}" stroke="\#6a6a82" stroke-width="2"/\>  
    \<line x1="${s\*.18}" y1="${s/2}" x2="${s\*.34}" y2="${s/2}" stroke="\#6a6a82" stroke-width="2"/\>  
    \<line x1="${s\*.66}" y1="${s/2}" x2="${s\*.82}" y2="${s/2}" stroke="\#6a6a82" stroke-width="2"/\>\`,

  worker: s=\>\`\<circle cx="${s\*.5}" cy="${s\*.33}" r="${s\*.15}" fill="\#8a7060"/\>  
    \<rect x="${s\*.35}" y="${s\*.5}" width="${s\*.3}" height="${s\*.32}" fill="\#8a7060" rx="2"/\>  
    \<line x1="${s\*.3}" y1="${s\*.6}" x2="${s\*.14}" y2="${s\*.82}" stroke="\#6a5040" stroke-width="2"/\>  
    \<line x1="${s\*.7}" y1="${s\*.6}" x2="${s\*.86}" y2="${s\*.82}" stroke="\#6a5040" stroke-width="2"/\>  
    \<rect x="${s\*.6}" y="${s\*.23}" width="${s\*.24}" height="${s\*.08}" fill="\#c09040" rx="1" transform="rotate(-30 ${s\*.72} ${s\*.27})"/\>\`,

  roller: s=\>\`\<ellipse cx="${s\*.5}" cy="${s\*.58}" rx="${s\*.32}" ry="${s\*.22}" fill="\#5a4030" stroke="\#8a6040" stroke-width="1.5"/\>  
    \<rect x="${s\*.3}" y="${s\*.28}" width="${s\*.4}" height="${s\*.16}" fill="\#6a5040" rx="2"/\>  
    \<circle cx="${s\*.24}" cy="${s\*.6}" r="${s\*.1}" fill="\#3a2818" stroke="\#6a4020" stroke-width="1.5"/\>  
    \<circle cx="${s\*.76}" cy="${s\*.6}" r="${s\*.1}" fill="\#3a2818" stroke="\#6a4020" stroke-width="1.5"/\>\`,

  beast: s=\>\`\<ellipse cx="${s\*.5}" cy="${s\*.42}" rx="${s\*.3}" ry="${s\*.28}" fill="\#404050" stroke="\#606070" stroke-width="1"/\>  
    \<circle cx="${s\*.38}" cy="${s\*.38}" r="${s\*.06}" fill="\#60a0f0" opacity=".9"/\>  
    \<circle cx="${s\*.62}" cy="${s\*.38}" r="${s\*.06}" fill="\#60a0f0" opacity=".9"/\>  
    \<path d="M${s\*.32},${s\*.57} Q${s\*.5},${s\*.67} ${s\*.68},${s\*.57}" stroke="\#808090" stroke-width="1.5" fill="none"/\>  
    \<line x1="${s\*.4}" y1="${s\*.68}" x2="${s\*.38}" y2="${s\*.84}" stroke="\#606070" stroke-width="1.5"/\>  
    \<line x1="${s\*.5}" y1="${s\*.7}" x2="${s\*.5}" y2="${s\*.86}" stroke="\#606070" stroke-width="1.5"/\>  
    \<line x1="${s\*.6}" y1="${s\*.68}" x2="${s\*.62}" y2="${s\*.84}" stroke="\#606070" stroke-width="1.5"/\>\`,

  wrench: s=\>\`\<rect x="${s\*.36}" y="${s\*.16}" width="${s\*.28}" height="${s\*.68}" fill="\#806040" rx="3" transform="rotate(-22 ${s\*.5} ${s\*.5})"/\>  
    \<circle cx="${s\*.34}" cy="${s\*.3}" r="${s\*.1}" fill="none" stroke="\#a08060" stroke-width="2.5"/\>  
    \<circle cx="${s\*.66}" cy="${s\*.7}" r="${s\*.1}" fill="none" stroke="\#a08060" stroke-width="2.5"/\>  
    \<line x1="${s\*.26}" y1="${s\*.54}" x2="${s\*.74}" y2="${s\*.46}" stroke="\#e06050" stroke-width="1.5" opacity=".7"/\>\`,

  clock: s=\>\`\<circle cx="${s\*.5}" cy="${s\*.48}" r="${s\*.3}" fill="none" stroke="\#8060a0" stroke-width="2"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.48}" r="${s\*.27}" fill="\#100820" opacity=".6"/\>  
    \<line x1="${s\*.5}" y1="${s\*.48}" x2="${s\*.5}" y2="${s\*.24}" stroke="\#c0a0f0" stroke-width="2" stroke-linecap="round"/\>  
    \<line x1="${s\*.5}" y1="${s\*.48}" x2="${s\*.66}" y2="${s\*.55}" stroke="\#e0c080" stroke-width="1.5" stroke-linecap="round"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.48}" r="${s\*.04}" fill="\#e0c080"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.2}" r="${s\*.04}" fill="\#8060a0" opacity=".7"/\>\`,

  // ── 新卡牌專屬美術（優化向量幾何） ──  
    
  // 1\. 蒸氣飛艇 (空氣動力學流線艇身 \+ 雙螺旋槳)  
  airship: s=\>\`\<path d="M${s\*.15},${s\*.4} C${s\*.3},${s\*.2} ${s\*.7},${s\*.2} ${s\*.85},${s\*.4} C${s\*.9},${s\*.5} ${s\*.7},${s\*.6} ${s\*.5},${s\*.6} C${s\*.3},${s\*.6} ${s\*.1},${s\*.5} ${s\*.15},${s\*.4} Z" fill="\#6a5a4a" stroke="\#8a7a6a" stroke-width="1.5"/\>  
    \<rect x="${s\*.4}" y="${s\*.6}" width="${s\*.2}" height="${s\*.08}" fill="\#8a401a" rx="1"/\>  
    \<line x1="${s\*.38}" y1="${s\*.55}" x2="${s\*.42}" y2="${s\*.6}" stroke="\#444"/\>  
    \<line x1="${s\*.62}" y1="${s\*.55}" x2="${s\*.58}" y2="${s\*.6}" stroke="\#444"/\>  
    \<line x1="${s\*.82}" y1="${s\*.35}" x2="${s\*.88}" y2="${s\*.45}" stroke="\#b03020" stroke-width="2"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.4}" r="${s\*.05}" fill="none" stroke="\#a0c0f0" stroke-width="1" opacity=".7"/\>\`,

  // 2\. 機油回收幫浦 (精密活塞結構 \+ 瑩綠色機油液面發光)  
  pump: s=\>\`\<rect x="${s\*.38}" y="${s\*.2}" width="${s\*.24}" height="${s\*.55}" fill="\#2a2a2a" stroke="\#555" rx="2"/\>  
    \<rect x="${s\*.42}" y="${s\*.45}" width="${s\*.16}" height="${s\*.26}" fill="\#205010" opacity=".85"/\>  
    \<line x1="${s\*.5}" y1="${s\*.12}" x2="${s\*.5}" y2="${s\*.4}" stroke="\#aaa" stroke-width="3" stroke-linecap="round"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.12}" r="${s\*.06}" fill="\#b08030"/\>  
    \<path d="M${s\*.3},${s\*.75} L${s\*.7},${s\*.75}" stroke="\#444" stroke-width="3"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.58}" r="${s\*.04}" fill="\#60ff40" filter="drop-shadow(0 0 3px \#60ff40)"/\>\`,

  // 3\. 不穩定電能炸彈 (危險核心 \+ 劇烈不規則高壓電弧)  
  bomb: s=\>\`\<circle cx="${s\*.5}" cy="${s\*.52}" r="${s\*.24}" fill="\#1a1a26" stroke="\#d04040" stroke-width="2"/\>  
    \<rect x="${s\*.44}" y="${s\*.2}" width="${s\*.12}" height="${s\*.1}" fill="\#555" rx="1"/\>  
    \<path d="M${s\*.5},${s\*.2} Q${s\*.58},${s\*.12} ${s\*.65},${s\*.15}" fill="none" stroke="\#e0a020" stroke-width="1.5"/\>  
    \<circle cx="${s\*.65}" cy="${s\*.15}" r="${s\*.02}" fill="\#ffdd66"/\>  
    \<path d="M${s\*.4},${s\*.48} L${s\*.46},${s\*.56} L${s\*.54},${s\*.46} L${s\*.6},${s\*.54}" fill="none" stroke="\#40a0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.52}" r="${s\*.18}" fill="none" stroke="\#40a0ff" stroke-width="1" stroke-dasharray="2,3" opacity=".6"/\>\`,

  // 4\. 壓力閥盾衛 (厚重合金巨盾 \+ 橘紅色高壓蒸汽洩壓孔)  
  shield: s=\>\`\<path d="M${s\*.25},${s\*.22} L${s\*.75},${s\*.22} L${s\*.75},${s\*.55} C${s\*.75},${s\*.72} ${s\*.5},${s\*.85} ${s\*.5},${s\*.85} C${s\*.5},${s\*.85} ${s\*.25},${s\*.72} ${s\*.25},${s\*.55} Z" fill="\#3a404a" stroke="\#6a7585" stroke-width="2.5"/\>  
    \<path d="M${s\*.35},${s\*.3} L${s\*.65},${s\*.3}" stroke="\#b07830" stroke-width="3"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.52}" r="${s\*.07}" fill="\#222" stroke="\#b03010" stroke-width="1.5"/\>  
    \<line x1="${s\*.5}" y1="${s\*.52}" x2="${s\*.55}" y2="${s\*.49}" stroke="\#ff6010" stroke-width="2"/\>  
    \<circle cx="${s\*.32}" cy="${s\*.4}" r="${s\*.02}" fill="\#888"/\>  
    \<circle cx="${s\*.68}" cy="${s\*.4}" r="${s\*.02}" fill="\#888"/\>\`,

  // 5\. 齒輪超載者 (雙向咬合大齒輪 \+ 火花四濺的電弧核心)  
  overcharger: s=\>\`\<circle cx="${s\*.38}" cy="${s\*.46}" r="${s\*.18}" fill="none" stroke="\#b07830" stroke-width="2.5" stroke-dasharray="6,4"/\>  
    \<circle cx="${s\*.62}" cy="${s\*.58}" r="${s\*.14}" fill="none" stroke="\#8a5a22" stroke-width="2" stroke-dasharray="4,4"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.32}" r="${s\*.08}" fill="\#2a1005" stroke="\#e07010" stroke-width="1.5"/\>  
    \<line x1="${s\*.5}" y1="${s\*.32}" x2="${s\*.46}" y2="${s\*.24}" stroke="\#ffcc40" stroke-width="2"/\>  
    \<line x1="${s\*.5}" y1="${s\*.32}" x2="${s\*.56}" y2="${s\*.38}" stroke="\#ffcc40" stroke-width="1.5"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.32}" r="${s\*.02}" fill="\#fff"/\>\`,

  // 6\. 蒸汽狙擊手 (黃銅精密長槍管 \+ 雷射十字瞄準線)  
  sniper: s=\>\`\<rect x="${s\*.15}" y="${s\*.48}" width="${s\*.55}" height="${s\*.08}" fill="\#5a4530" rx="1" transform="rotate(-15 ${s\*.5} ${s\*.5})"/\>  
    \<rect x="${s\*.35}" y="${s\*.36}" width="${s\*.18}" height="${s\*.06}" fill="\#8a7050" transform="rotate(-15 ${s\*.5} ${s\*.5})"/\>  
    \<line x1="${s\*.12}" y1="${s\*.58}" x2="${s\*.88}" y2="${s\*.38}" stroke="\#ff3333" stroke-width="1" stroke-dasharray="4,3" opacity=".85"/\>  
    \<circle cx="${s\*.65}" cy="${s\*.44}" r="${s\*.05}" fill="none" stroke="\#ff3333" stroke-width="1.5"/\>  
    \<path d="M${s\*.15},${s\*.55} L${s\*.25},${s\*.72} L${s\*.32},${s\*.7}" fill="\#4a3520"/\>\`,

  // 7\. 自動化維修機 (多功能機械吊臂 \+ 亮藍色精密焊接弧光)  
  repairer: s=\>\`\<rect x="${s\*.4" y="${s\*.7}" width="${s\*.2}" height="${s\*.1}" fill="\#333" rx="1"/\>  
    \<line x1="${s\*.5}" y1="${s\*.7}" x2="${s\*.35}" y2="${s\*.45}" stroke="\#7a6a5a" stroke-width="3" stroke-linecap="round"/\>  
    \<line x1="${s\*.35}" y1="${s\*.45}" x2="${s\*.55}" y2="${s\*.25}" stroke="\#9a8a7a" stroke-width="2.5" stroke-linecap="round"/\>  
    \<circle cx="${s\*.35}" cy="${s\*.45}" r="${s\*.04}" fill="\#b08030"/\>  
    \<rect x="${s\*.52}" y="${s\*.2}" width="${s\*.08}" height="${s\*.1}" fill="\#b03020" rx="1" transform="rotate(30 ${s\*.55} ${s\*.25})"/\>  
    \<circle cx="${s\*.6}" cy="${s\*.22}" r="${s\*.05}" fill="\#60c0ff" filter="drop-shadow(0 0 4px \#60c0ff)"/\>\`,

  // 8\. 巨型合金破城者 (重裝履帶地盤 \+ 尖銳的合金撞角)  
  breaker: s=\>\`\<rect x="${s\*.2}" y="${s\*.62}" width="${s\*.6}" height="${s\*.15}" fill="\#252528" rx="4"/\>  
    \<circle cx="${s\*.28}" cy="${s\*.7}" r="${s\*.05}" fill="\#444"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.7}" r="${s\*.05}" fill="\#444"/\>  
    \<circle cx="${s\*.72}" cy="${s\*.7}" r="${s\*.05}" fill="\#444"/\>  
    \<path d="M${s\*.3},${s\*.35} L${s\*.7},${s\*.35} L${s\*.85},${s\*.62} L${s\*.15},${s\*.62} Z" fill="\#4a505a" stroke="\#6a7280" stroke-width="1.5"/\>  
    \<path d="M${s\*.75},${s\*.45} L${s\*.94},${s\*.58} L${s\*.75},${s\*.62} Z" fill="\#b08030" stroke="\#d0a040"/\>\`,

  // 9\. 工坊防禦核心 (雙層重裝防護穹頂 \+ 核心脈衝力場)  
  core: s=\>\`\<circle cx="${s\*.5}" cy="${s\*.5}" r="${s\*.35}" fill="none" stroke="\#3a4555" stroke-width="3" stroke-dasharray="14,6"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.5}" r="${s\*.24}" fill="\#151822" stroke="\#5a6a85" stroke-width="1.5"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.5}" r="${s\*.12}" fill="\#204070" stroke="\#4080ff" stroke-width="2"/\>  
    \<circle cx="${s\*.5}" cy="${s\*.5}" r="${s\*.04}" fill="\#fff" filter="drop-shadow(0 0 5px \#4080ff)"/\>  
    \<line x1="${s\*.15}" y1="${s\*.5}" x2="${s\*.28}" y2="${s\*.5}" stroke="\#4080ff" stroke-width="1" opacity=".7"/\>  
    \<line x1="${s\*.85}" y1="${s\*.5}" x2="${s\*.72}" y2="${s\*.5}" stroke="\#4080ff" stroke-width="1" opacity=".7"/\>\`,

  // 10\. 核子平行迫擊炮 (高聳對稱雙砲管 \+ 毀滅性電漿集束能量)  
  mortar: s=\>\`\<rect x="${s\*.3}" y="${s\*.68}" width="${s\*.4}" height="${s\*.12}" fill="\#2a2520" rx="2"/\>  
    \<rect x="${s\*.34}" y="${s\*.24}" width="${s\*.1}" height="${s\*.45}" fill="\#5a5045" stroke="\#7a6e60" stroke-width="1.5"/\>  
    \<rect x="${s\*.56}" y="${s\*.24}" width="${s\*.1}" height="${s\*.45}" fill="\#5a5045" stroke="\#7a6e60" stroke-width="1.5"/\>  
    \<circle cx="${s\*.39}" cy="${s\*.22}" r="${s\*.03}" fill="\#ff4020"/\>  
    \<circle cx="${s\*.61}" cy="${s\*.22}" r="${s\*.03}" fill="\#ff4020"/\>  
    \<path d="M${s\*.25},${s\*.48} Q${s\*.5},${s\*.38} ${s\*.75},${s\*.48}" fill="none" stroke="\#ffaa40" stroke-width="2" stroke-dasharray="3,2" opacity=".8"/\>\`  
};

### **🛠️ 同步更新卡牌模版中的 `portrait` 屬性**

為了讓卡牌正確對接到上面設計的新插畫 Key，需要將 `TEMPLATES` 陣列中新增那 10 張卡牌的 `portrait` 屬性做一次對應修正。

請找到代碼中的 **`const TEMPLATES = [ ... ]`** 區塊，將**新增十張**的部份修改為對應的藝術 Key：

JavaScript  
 // ── 新增十張（請更新此處的 portrait 欄位） ──  
  { name:"蒸氣飛艇",       cost:1, atk:1, hp:1, text:"部署：抽一張牌",                         portrait:"airship",  battlecry:true,   bcType:"draw1" },  
  { name:"機油回收幫浦",   cost:2, atk:1, hp:3, text:"回合結束：回復自身 2 點生命值",            portrait:"pump",     endOfTurn:true,   eotType:"heal2self" },  
  { name:"不穩定電能炸彈", cost:2, atk:0, hp:2, text:"攔截，報廢：對隨機敵方手下造成 3 傷害",   portrait:"bomb",     taunt:true,       deathrattle:true, drType:"dmg3rand" },  
  { name:"壓力閥盾衛",     cost:3, atk:2, hp:5, text:"攔截",                                  portrait:"shield",   taunt:true },  
  { name:"齒輪超載者",     cost:3, atk:3, hp:3, text:"部署：本回合獲得 1 點額外燃料",           portrait:"overcharger", battlecry:true, bcType:"fuel1" },  
  { name:"蒸汽狙擊手",     cost:4, atk:3, hp:3, text:"部署：對隨機敵方手下造成 2 傷害",         portrait:"sniper",   battlecry:true,   bcType:"dmg2rand" },  
  { name:"自動化維修機",   cost:4, atk:2, hp:6, text:"部署：使一個友方手下回復全部生命值",       portrait:"repairer", battlecry:true,   bcType:"healfriendly" },  
  { name:"巨型合金破城者", cost:6, atk:6, hp:7, text:"攔截",                                  portrait:"breaker",  taunt:true },  
  { name:"工坊防禦核心",   cost:7, atk:4, hp:8, text:"攔截，報廢：抽兩張牌",                   portrait:"core",     taunt:true,       deathrattle:true, drType:"draw2" },  
  { name:"核子平行迫擊炮", cost:8, atk:7, hp:7, text:"部署：摧毀所有敵方手下",                  portrait:"mortar",   battlecry:true,   bcType:"destroyall" },

### **✨ 設計巧思說明**

* **高度一體化的龐克美學**：插畫延用了你原生的漸層色背景 `PORTRAIT_COLORS`，讓新舊卡牌置於同一個棋盤時視覺感完全統一。  
* **發光與動態暗示**：  
  * **不穩定電能炸彈** 與 **工坊防禦核心** 運用了紅色與亮藍色的強烈對比，暗示其報廢後會產生劇烈能量波動。  
  * **蒸汽狙擊手** 畫出了紅色的虛線雷射瞄準軌跡，與其隨機點射傷害的戰吼機制相呼應。  
  * **核子平行迫擊炮** 的雙管重型火炮和粒子軌道，完美襯托出它一登場就「清空全場」的終結者氣勢。


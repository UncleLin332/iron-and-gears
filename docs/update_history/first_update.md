// 請將這 10 張卡牌新增到遊戲中  
const NEW\_TEMPLATES \= \[  
  // 1\. 低費過牌與鋪場  
  { name: “蒸氣飛艇", cost: 1, atk: 1, hp: 1, text: "部署：抽一張牌", portrait: "gear", battlecry: true },  
  { name: "機油回收幫浦", cost: 2, atk: 1, hp: 3, text: "回合結束：回復自身 2 點生命值", portrait: "worker", endOfTurn: true },  
  { name: "不穩定的電能炸彈", cost: 2, atk: 0, hp: 2, text: "攔截，報廢：對隨機敵方手下造成 3 點傷害", portrait: "gear", taunt: true, deathrattle: true },

  // 2\. 中費戰術與反制  
  { name: "壓力閥盾衛", cost: 3, atk: 2, hp: 5, text: "攔截", portrait: "beast", taunt: true },  
  { name: "齒輪超載者", cost: 3, atk: 3, hp: 3, text: "部署：本回合獲得 1 點額外燃料", portrait: "worker", battlecry: true },  
  { name: "蒸汽狙擊手", cost: 4, atk: 3, hp: 3, text: "部署：對一個隨機敵方手下造成 2 點傷害", portrait: "wrench", battlecry: true },  
  { name: "自動化維修機", cost: 4, atk: 2, hp: 6, text: "部署：使一個友方手下回復全部生命值", portrait: "clock", battlecry: true },

  // 3\. 高費威脅與核心  
  { name: "巨型合金破城者", cost: 6, atk: 6, hp: 7, text: "攔截", portrait: "roller", taunt: true },  
  { name: "工坊防禦核心", cost: 7, atk: 4, hp: 8, text: "攔截，報廢：抽兩張牌", portrait: "clock", taunt: true, deathrattle: true },  
  { name: “核子平行迫擊炮", cost: 8, atk: 7, hp: 7, text: "部署：摧毀所有敵方手下", portrait: "beast", battlecry: true }  
\];  

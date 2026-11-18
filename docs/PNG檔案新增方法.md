1. 在 CSS 加一個圖片樣式，讓 PNG 填滿卡牌頭像區：

.portrait-img {  
  width: 100%;  
  height: 100%;  
  display: block;  
  object-fit: cover;  
  object-position: center;  
}

2. 在原本 PORTRAIT\_SVG 下方新增卡圖對照表：

const CARD\_ART \= {  
  "蒸汽狙擊手": "character art/蒸氣狙擊手.png",  
};

3. 新增一個渲染函式：如果卡名有對應 PNG，就用 \<img\>；沒有就回到原本 SVG。

function portraitArt(card, s) {  
  const art \= CARD\_ART\[card.name\];  
  if (\!art) return portraitSvg(card, s);  
  return \`\<img class="portrait-img" src="${art}" alt="${card.name}"\>\`;  
}

4. 把兩個原本呼叫 portraitSvg(...) 的地方改成 portraitArt(...)：

\<div class\="card-portrait-mini"\>${portraitArt(c,54)}\</div\>  
\<div class\="hand-portrait"\>${portraitArt(c,48)}\</div\>

之後要替換其它卡，只要在 CARD\_ART 加一行即可，例如：

const CARD\_ART \= {  
  "蒸汽狙擊手": "character art/蒸氣狙擊手.png",  
  "機油回收幫浦": "character art/機油回收幫浦.png",  
};  

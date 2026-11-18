// 🎼 重新編排：洗腦系 · 蒸汽龐克工坊狂想曲（32拍極速齒輪圓舞曲）
function scheduleMusicStep(step, time) {
  // 1. 沉重且洗腦的低音與和弦走向（每4拍一個和弦循環：Am -> Dm -> G -> C -> F -> Bdim -> E -> E）
  // 採用經典的「五度循環圈」，這是音樂史上最洗腦、最富有戲劇前進感的和弦進行！
  const bassPattern = [
    110.00, 110.00, 110.00, 110.00, // A minor (鋼鐵工坊的甦醒)
    146.83, 146.83, 146.83, 146.83, // D minor (齒輪開始咬合)
    98.00,  98.00,  98.00,  98.00,  // G major  (蒸氣壓力湧入)
    130.81, 130.81, 130.81, 130.81, // C major  (核心光芒四射)
    87.31,  87.31,  87.31,  87.31,  // F major  (傳動軸全力運轉)
    123.47, 123.47, 123.47, 123.47, // B diminished (機械過熱的緊迫感)
    164.81, 164.81, 164.81, 164.81, // E major  (安全閥強力壓制)
    82.41,  82.41,  164.81, 220.00  // E -> Am  (準備重啟循環)
  ];
  
  // 2. 核心洗腦主旋律：帶有切分音與跳躍感，像精準計算的發條玩偶在跳舞
  // 0 代表休止符，讓旋律有呼吸和頓點，聽起來會更彈跳、更魔性
  const melodyPattern = [
    // ── 第一樂段：主題登場 ──
    220.0, 0, 261.6, 293.7, 329.6, 0, 220.0, 329.6, // Am: 經典爬升
    349.2, 0, 293.7, 0,     293.7, 349.2, 392.0, 440.0, // Dm: 迴轉前進
    392.0, 0, 246.9, 293.7, 293.7, 0, 196.0, 293.7, // G:  跳躍齒輪
    329.6, 0, 261.6, 0,     261.6, 329.6, 349.2, 392.0, // C:  穩健運轉
    
    // ── 第二樂段：高潮與發條拉緊 ──
    349.2, 0, 218.3, 261.6, 261.6, 0, 349.2, 0,     // F:  突變動能
    493.9, 0, 293.7, 349.2, 349.2, 493.9, 523.3, 493.9, // Bdim: 尖銳的金屬摩擦
    440.0, 0, 329.6, 0,     392.0, 0, 329.6, 0,     // E:  過熱警報 (440 -> 329 -> 392 -> 329)
    415.3, 440.0, 493.9, 523.3, 587.3, 0, 0, 0      // E7: 發條瞬間釋放！極速下行準備重頭來過
  ];

  // 3. 發條八音盒伴奏（Arpeggio）：在主旋律休息時填補空間，讓音樂聽起來有源源不絕的「發條噠噠聲」
  const arpeggioPattern = [
    440, 523, 440, 523, 587, 659, 587, 659,
    392, 494, 392, 494, 523, 587, 523, 587
  ];

  const barStep = step % 64; // 將循環擴展至 64 步（完整 4 個小節，16拍 × 4）
  const chordIndex = (step / 2) % bassPattern.length | 0;
  
  // ── 聲部一：沉重的蒸汽鋼鐵低音（雙倍厚度鋸齒波） ──
  if (step % 2 === 0) {
    const currentBass = bassPattern[chordIndex];
    scheduleTone(currentBass, time, 0.22, "sawtooth", 0.05);
    // 疊加低八度，讓鋼鐵沉重感更穩固
    scheduleTone(currentBass / 2, time, 0.22, "triangle", 0.04);
  }
  
  // ── 聲部二：魔性洗腦主旋律（使用方波，帶點老舊電子管與風琴的綜合質感） ──
  const currentMelodyFreq = melodyPattern[barStep];
  if (currentMelodyFreq > 0) {
    // 主音
    scheduleTone(currentMelodyFreq, time, 0.16, "square", 0.026);
    // 微幅超前的高音泛音，模擬銅管樂器的明亮感
    scheduleTone(currentMelodyFreq * 2, time + 0.005, 0.08, "triangle", 0.01);
  }
  
  // ── 聲部三：背景發條八音盒（在特定小節亂入，增加層次感） ──
  if (barStep >= 32 && step % 2 === 1) {
    const arpFreq = arpeggioPattern[step % arpeggioPattern.length];
    scheduleTone(arpFreq, time, 0.06, "square", 0.008);
  }
  
  // ── 聲部四：工業打擊樂（維持原本優秀的蒸汽與鐵鎚基底） ──
  if (step % 4 === 0) {
    // 鐵鎚重擊
    scheduleTone(60, time, 0.1, "triangle", 0.07, Music.master);
  }
  
  if (step % 8 === 4) {
    // 大閥門排氣：咻──
    scheduleSteamVent(time, 0.2, 0.04);
  } else if (step % 2 === 1) {
    // 小齒輪嚙合聲與輕微漏氣
    if (step % 4 === 2) scheduleGearClang(time, 0.035);
    scheduleSteamVent(time, 0.03, 0.015);
  }
}

// 記得同步更新音樂引擎的循環長度！
function musicScheduler() {
  const secondsPerStep = 60 / Music.tempo / 4;
  while(Music.nextTime < Music.ctx.currentTime + Music.scheduleAhead) {
    scheduleMusicStep(Music.step, Music.nextTime);
    Music.step = (Music.step + 1) % 64; // 改為 64 步大循環
    Music.nextTime += secondsPerStep;
  }
}
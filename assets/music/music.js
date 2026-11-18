// ═══════════════════════════════════════
//  STEAMPUK INDUSTRIAL AUDIO ENGINE (V4)
// ═══════════════════════════════════════
const Music = {
  ctx:null, master:null, filter:null, delay:null, feedback:null,
  timer:null, step:0, nextTime:0, enabled:false, started:false,
  tempo:92, // 稍微放慢一點點，展現鋼鐵的沉重感
  lookahead:25, scheduleAhead:0.12,
};
window.Music = Music;

function initAudio() {
  if(Music.ctx) return;
  const AudioContext = window.AudioContext || window.webkitAudioContext;
  if(!AudioContext) {
    log("此瀏覽器不支援 Web Audio API，無法播放音樂。","sys");
    render();
    return;
  }
  const ctx = new AudioContext();
  const master = ctx.createGain();
  const filter = ctx.createBiquadFilter();
  const delay = ctx.createDelay(1);
  const feedback = ctx.createGain();
  
  master.gain.value = 0.16;
  
  // 工坊環境濾波器：讓整體聲音帶點悶沉的金屬房間感
  filter.type = "lowpass";
  filter.frequency.value = 1600;
  filter.Q.value = 1.2; // 增加一點共振，讓金屬感更明顯
  
  // 工坊長廊的迴音效果
  delay.delayTime.value = 0.32; // 稍微拉長迴音時間
  feedback.gain.value = 0.28;   // 讓殘響多延續一點點
  
  filter.connect(master);
  filter.connect(delay);
  delay.connect(feedback);
  feedback.connect(delay);
  delay.connect(master);
  master.connect(ctx.destination);
  
  Object.assign(Music, {ctx, master, filter, delay, feedback});
}

// 基礎音效生成：加入了發條搖擺不穩定感 (Detune)
function scheduleTone(freq, time, dur, type="sawtooth", gain=0.08, dest=Music.filter) {
  const ctx = Music.ctx;
  const osc = ctx.createOscillator();
  const amp = ctx.createGain();
  
  osc.type = type;
  osc.frequency.setValueAtTime(freq, time);
  
  // ⚙️ 蒸氣龐克發條細節：模擬機械磨損的微幅走音（增加神祕與老舊感）
  const wobble = (Math.random() * 20 - 10); // -10 到 +10 cents 的隨機微調
  osc.detune.setValueAtTime(wobble, time);
  osc.detune.linearRampToValueAtTime(wobble * -1, time + dur);

  amp.gain.setValueAtTime(0.0001, time);
  amp.gain.exponentialRampToValueAtTime(gain, time + 0.015);
  amp.gain.exponentialRampToValueAtTime(0.0001, time + dur);
  
  osc.connect(amp);
  amp.connect(dest);
  osc.start(time);
  osc.stop(time + dur + 0.04);
}

// 💨 改造：蒸氣閥噴氣音效 (Steam Vent Blow)
function scheduleSteamVent(time, dur=0.18, gain=0.06) {
  const ctx = Music.ctx;
  const len = Math.max(1, Math.floor(ctx.sampleRate * dur));
  const buffer = ctx.createBuffer(1, len, ctx.sampleRate);
  const data = buffer.getChannelData(0);
  
  // 白雜訊
  for(let i=0; i<len; i++) data[i] = (Math.random() * 2 - 1);
  
  const src = ctx.createBufferSource();
  const amp = ctx.createGain();
  const lp = ctx.createBiquadFilter();
  
  // 使用帶通濾波器調製，做出蒸氣噴出時「嘶──」的集中氣壓感
  lp.type = "bandpass";
  lp.frequency.setValueAtTime(1200, time);
  lp.frequency.exponentialRampToValueAtTime(400, time + dur); // 氣壓下降的動態
  lp.Q.value = 2.0;

  amp.gain.setValueAtTime(0.0001, time);
  amp.gain.linearRampToValueAtTime(gain, time + 0.02); // 快速噴出
  amp.gain.exponentialRampToValueAtTime(0.0001, time + dur); // 慢慢漏氣
  
  src.buffer = buffer;
  src.connect(lp);
  lp.connect(amp);
  amp.connect(Music.master); // 直接進 master 保持氣體乾淨度
  
  src.start(time);
  src.stop(time + dur);
}

// 🔨 改造：齒輪嚙合與打鐵聲 (Gear Clang)
function scheduleGearClang(time, gain=0.05) {
  const ctx = Music.ctx;
  // 透過多個互不協和的高頻不規則疊加，製造鐵器敲擊的「鏗鏘」金屬泛音
  const frequencies = [120, 310, 485, 873, 1245];
  
  frequencies.forEach((freq, index) => {
    const osc = ctx.createOscillator();
    const amp = ctx.createGain();
    
    // 越高頻衰減得越快
    const individualDur = 0.03 + (0.05 / (index + 1));
    const individualGain = gain * (1 / (index + 1));
    
    osc.type = index % 2 === 0 ? "triangle" : "square";
    osc.frequency.setValueAtTime(freq, time);
    
    amp.gain.setValueAtTime(individualGain, time);
    amp.gain.exponentialRampToValueAtTime(0.0001, time + individualDur);
    
    osc.connect(amp);
    amp.connect(Music.filter);
    osc.start(time);
    osc.stop(time + individualDur + 0.02);
  });
}

// 🎼 重新編排：蒸氣龐克進行曲（陰沉、機械化、規律、前進感）
function scheduleMusicStep(step, time) {
  // 小調和弦進行（A minor -> F major -> D minor -> E major），帶有維多利亞時代的歌劇神祕感
  const bassPattern = [
    110, 110, 110, 110, // A (第1-4拍)
    87.3, 87.3, 87.3, 87.3, // F (第5-8拍)
    73.4, 73.4, 73.4, 73.4, // D (第9-12拍)
    82.4, 82.4, 164.8, 82.4 // E (第13-16拍)
  ];
  
  // 齒輪組主旋律：斷奏、跳躍，像機械玩偶跳舞
  const melodyPattern = [
    220, 0, 261.6, 293.7, 329.6, 0, 261.6, 0,
    349.2, 0, 329.6, 293.7, 246.9, 0, 164.8, 0
  ];
  
  const barStep = step % 16;
  
  // 1. 沉重的蒸汽巨獸低音（每兩拍一下，用鋸齒波營造鋼鐵厚重感）
  if (step % 2 === 0) {
    const currentBass = bassPattern[(step / 2) % bassPattern.length | 0];
    scheduleTone(currentBass, time, 0.25, "sawtooth", 0.06);
  }
  
  // 2. 齒輪旋律（方波，聽起來像八音盒或發條裝置）
  if (melodyPattern[barStep] > 0) {
    scheduleTone(melodyPattern[barStep], time, 0.14, "square", 0.024);
  }
  
  // 3. 工業節奏組（打擊樂）
  if (barStep === 0 || barStep === 8) {
    // 強調重拍：大鐵鎚擊打（低頻三角波）
    scheduleTone(65, time, 0.12, "triangle", 0.08, Music.master);
  }
  
  if (barStep % 4 === 2) {
    // 弱拍：高頻齒輪咬合聲 (Clang)
    scheduleGearClang(time, 0.045);
  }
  
  if (barStep % 8 === 4) {
    // 週期性的氣閥過熱排氣！「咻──」
    scheduleSteamVent(time, 0.22, 0.045);
  } else if (barStep % 2 === 1) {
    // 微弱的小氣閥漏氣聲，填補節奏空隙
    scheduleSteamVent(time, 0.03, 0.02);
  }
}

function musicScheduler() {
  const secondsPerStep = 60 / Music.tempo / 4;
  while(Music.nextTime < Music.ctx.currentTime + Music.scheduleAhead) {
    scheduleMusicStep(Music.step, Music.nextTime);
    Music.step = (Music.step + 1) % 32; // 擴展到 32 拍的大循環
    Music.nextTime += secondsPerStep;
  }
}

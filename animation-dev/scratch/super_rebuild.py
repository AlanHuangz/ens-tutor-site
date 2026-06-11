# super_rebuild.py
import os
import re

def rebuild():
    scenes_dir = r"C:\Users\wkoyo\Documents\家教網站\animation-dev\scenes"
    
    # 31 幕的排版、配圖與 CSS 動效規則
    # 採用響應式 vw (Viewport Width) 單位，保證在所有載具上完美等比縮放，不截斷、不模糊！
    scene_rules = {
        # 1. 家長懊惱 (大圖 + 焦慮氣泡 + 呼吸浮動)
        1: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/parent_anxiety.png" class="scene-img anxiety-img" alt="家長懊惱與焦慮">
          <div class="bubble bubble-1">？</div>
          <div class="bubble bubble-2">？</div>
          <div class="bubble bubble-3">…</div>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.anxiety-img { animation: swayAnxiety 6s ease-in-out infinite !important; }
@keyframes swayAnxiety {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
  50% { transform: translateY(-0.8vw) rotate(-1.5deg) scale(1.015); }
}
.bubble {
  position: absolute;
  background: rgba(82, 133, 140, 0.08);
  color: var(--color-primary);
  border: 0.15vw solid rgba(82, 133, 140, 0.25);
  font-family: "Noto Sans TC", sans-serif;
  font-weight: 900;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0.8vw 2.4vw rgba(82, 133, 140, 0.05);
  user-select: none;
}
.bubble-1 { width: 5vw; height: 5vw; font-size: 2.2vw; top: 15%; left: -5%; animation: bubbleFloat1 8s ease-in-out infinite; }
.bubble-2 { width: 4vw; height: 4vw; font-size: 1.8vw; top: 30%; right: -2%; animation: bubbleFloat2 10s ease-in-out infinite; }
.bubble-3 { width: 4.6vw; height: 4.6vw; font-size: 2vw; bottom: 20%; left: 5%; animation: bubbleFloat3 9s ease-in-out infinite; }
@keyframes bubbleFloat1 {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.7; }
  50% { transform: translateY(-1.2vw) rotate(15deg) scale(1.1); opacity: 1; }
}
@keyframes bubbleFloat2 {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.6; }
  50% { transform: translateY(-0.8vw) rotate(-15deg) scale(1.1); opacity: 0.9; }
}
@keyframes bubbleFloat3 {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.75; }
  50% { transform: translateY(-1.5vw) rotate(10deg) scale(1.1); opacity: 1; }
}"""
        },
        
        # 2. 我並不這麼認為 (3D 翻轉與顏色跳動)
        2: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="css-illustration-wrapper">
          <div class="flip-symbol">？ ➔ ！</div>
        </div>
      </div>""",
            'css': """
.css-illustration-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 25vw;
  height: 25vw;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  border: 0.3vw dashed var(--color-primary);
  animation: pulseBg 4s ease-in-out infinite;
}
.flip-symbol {
  font-size: 3.5vw;
  font-weight: 900;
  color: var(--color-primary);
  animation: flipText 5s ease-in-out infinite;
}
@keyframes pulseBg {
  0%, 100% { transform: scale(1); box-shadow: 0 1vw 3vw rgba(82, 133, 140, 0.05); }
  50% { transform: scale(1.05); box-shadow: 0 1.5vw 4vw rgba(82, 133, 140, 0.15); border-color: var(--color-highlight-accent); }
}
@keyframes flipText {
  0%, 100% { transform: rotateY(0deg) scale(1); color: var(--color-primary); }
  45%, 55% { transform: rotateY(180deg) scale(1.15); color: var(--color-highlight-accent); }
}"""
        },
        
        # 3. 閃光點與學習方式 (星星旋轉、縮放與閃爍)
        3: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="stars-container">
          <div class="star star-1">✦</div>
          <div class="star star-2">✦</div>
          <div class="star star-3">✦</div>
        </div>
      </div>""",
            'css': """
.stars-container {
  position: relative;
  width: 24vw;
  height: 24vw;
}
.star {
  position: absolute;
  color: var(--color-primary);
  font-weight: 900;
  user-select: none;
}
.star-1 { font-size: 8vw; top: 15%; left: 30%; animation: spinStar1 8s linear infinite; }
.star-2 { font-size: 5vw; top: 55%; left: 15%; color: var(--color-highlight-accent); animation: spinStar2 6s linear infinite; }
.star-3 { font-size: 4vw; top: 50%; left: 65%; color: var(--color-secondary); animation: spinStar1 4s linear infinite; }
@keyframes spinStar1 {
  0% { transform: rotate(0deg) scale(1); opacity: 0.7; }
  50% { transform: rotate(180deg) scale(1.25); opacity: 1; filter: drop-shadow(0 0 1vw var(--color-primary)); }
  100% { transform: rotate(360deg) scale(1); opacity: 0.7; }
}
@keyframes spinStar2 {
  0% { transform: rotate(0deg) scale(1.2); opacity: 0.9; }
  50% { transform: rotate(-180deg) scale(0.8); opacity: 0.6; filter: drop-shadow(0 0 1vw var(--color-highlight-accent)); }
  100% { transform: rotate(-360deg) scale(1.2); opacity: 0.9; }
}"""
        },
        
        # 4. 工業時期 (齒輪加速自轉與震動)
        4: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/industrial_education.png" class="scene-img industrial-img" alt="工業時期教育">
          <div class="gear gear-large">⚙️</div>
          <div class="gear gear-small">⚙️</div>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.industrial-img { animation: machineVibrate 3s ease-in-out infinite !important; }
@keyframes machineVibrate {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-0.4vw) scale(0.995); }
}
.gear { position: absolute; color: rgba(82, 133, 140, 0.25); line-height: 1; user-select: none; }
.gear-large { top: 18%; left: 14%; font-size: 8vw; animation: spinClockwise 10s linear infinite; }
.gear-small { top: 36%; left: 24%; font-size: 5.5vw; animation: spinCounterClockwise 6s linear infinite; }
@keyframes spinClockwise {
  0% { transform: rotate(0deg); }
  50% { transform: rotate(180deg); }
  100% { transform: rotate(360deg); }
}
@keyframes spinCounterClockwise {
  0% { transform: rotate(0deg); }
  50% { transform: rotate(-180deg); }
  100% { transform: rotate(-360deg); }
}"""
        },
        
        # 5. 穩定標準效率同步 (去重：純 CSS 輸送帶彈跳規格包裝盒動畫)
        5: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="conveyor-container">
          <div class="conveyor-belt">
            <div class="conveyor-roller roller-1">⚙️</div>
            <div class="conveyor-roller roller-2">⚙️</div>
            <div class="conveyor-roller roller-3">⚙️</div>
          </div>
          <div class="box-container">
            <div class="conveyor-box box-1">📦</div>
            <div class="conveyor-box box-2">📦</div>
            <div class="conveyor-box box-3">📦</div>
          </div>
        </div>
      </div>""",
            'css': """
.conveyor-container {
  position: relative;
  width: 28vw;
  height: 22vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
  border: 0.15vw solid rgba(82, 133, 140, 0.15);
  border-radius: 1.6vw;
  overflow: hidden;
}
.conveyor-belt {
  position: relative;
  width: 24vw;
  height: 0.6vw;
  background: var(--color-secondary);
  border-radius: 0.3vw;
  margin-top: 3vw;
  display: flex;
  justify-content: space-around;
}
.conveyor-roller {
  font-size: 2.2vw;
  margin-top: 0.6vw;
  color: var(--color-primary);
  animation: spinRoller 4s linear infinite;
  line-height: 1;
}
@keyframes spinRoller {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.box-container {
  position: absolute;
  top: 5.5vw;
  width: 24vw;
  height: 6vw;
  overflow: hidden;
}
.conveyor-box {
  position: absolute;
  font-size: 2.6vw;
  bottom: 0;
  animation: moveAndVibrateBox 5s linear infinite;
  opacity: 0;
}
.box-1 { animation-delay: 0s; }
.box-2 { animation-delay: 1.66s; }
.box-3 { animation-delay: 3.33s; }

@keyframes moveAndVibrateBox {
  0% { left: -4vw; opacity: 0; transform: scale(0.9) translateY(0); }
  10% { opacity: 1; transform: scale(1) translateY(0); }
  30%, 70% { transform: translateY(-0.3vw); }
  40%, 80% { transform: translateY(0); }
  90% { opacity: 1; transform: scale(1) translateY(0); }
  100% { left: 24vw; opacity: 0; transform: scale(0.9) translateY(0); }
}"""
        },
        
        # 6. 遠離工業時代 (齒輪縮小淡出模糊)
        6: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="fading-gear-wrapper">
          <div class="fading-gear">⚙️</div>
        </div>
      </div>""",
            'css': """
.fading-gear-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24vw;
  height: 24vw;
}
.fading-gear {
  font-size: 8vw;
  color: var(--color-primary);
  animation: fadeOutGear 5s ease-in-out infinite;
}
@keyframes fadeOutGear {
  0% { transform: scale(1.1) rotate(0deg); opacity: 0.9; filter: blur(0px); }
  50% { transform: scale(0.5) rotate(180deg); opacity: 0.1; filter: blur(4px); color: var(--color-highlight-accent); }
  100% { transform: scale(1.1) rotate(360deg); opacity: 0.9; filter: blur(0px); }
}"""
        },
        
        # 7. 科技攀升與留在原地 (快慢點強烈對比 + 滯留點發抖震動)
        7: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="track-wrapper">
          <div class="track-line track-top">
            <div class="moving-light"></div>
            <span class="track-label">科技</span>
          </div>
          <div class="track-line track-bottom">
            <div class="static-dot"></div>
            <span class="track-label">教育</span>
          </div>
        </div>
      </div>""",
            'css': """
.track-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5vw;
  width: 30vw;
  height: 22vw;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 1.6vw;
  padding: 3vw;
  border: 0.1vw solid rgba(82, 133, 140, 0.1);
}
.track-line {
  position: relative;
  width: 100%;
  height: 0.8vw;
  background: rgba(44, 61, 77, 0.1);
  border-radius: 0.4vw;
}
.track-label {
  position: absolute;
  top: -2.4vw;
  left: 0;
  font-size: 1.1vw;
  font-weight: 700;
  color: var(--color-text-main);
}
.moving-light {
  position: absolute;
  top: -0.4vw;
  left: 0;
  width: 1.6vw;
  height: 1.6vw;
  border-radius: 50%;
  background: var(--color-primary);
  box-shadow: 0 0 1.5vw var(--color-primary);
  animation: travelFast 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
.static-dot {
  position: absolute;
  top: -0.4vw;
  left: 20%;
  width: 1.6vw;
  height: 1.6vw;
  border-radius: 50%;
  background: var(--color-highlight-accent);
  animation: shakeStuck 2.5s ease-in-out infinite;
}
@keyframes travelFast {
  0% { left: 0%; opacity: 0.3; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { left: 90%; opacity: 0; }
}
@keyframes shakeStuck {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-0.3vw); }
  40%, 80% { transform: translateX(0.3vw); }
}"""
        },
        
        # 8. 成功學攀爬梯 (爬坡小球帶有果凍般的 squash/stretch 彈性變形)
        8: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="ladder-wrapper">
          <div class="ladder-step step-1"></div>
          <div class="ladder-step step-2"></div>
          <div class="ladder-step step-3"></div>
          <div class="climbing-dot"></div>
        </div>
      </div>""",
            'css': """
.ladder-wrapper {
  position: relative;
  width: 22vw;
  height: 22vw;
}
.ladder-step {
  position: absolute;
  width: 6vw;
  height: 1vw;
  background: var(--color-primary);
  opacity: 0.4;
  border-radius: 0.4vw;
}
.step-1 { bottom: 2vw; left: 2vw; }
.step-2 { bottom: 8vw; left: 7vw; }
.step-3 { bottom: 14vw; left: 12vw; }
.climbing-dot {
  position: absolute;
  width: 1.8vw;
  height: 1.8vw;
  border-radius: 50%;
  background: var(--color-highlight-accent);
  box-shadow: 0 0 1.2vw var(--color-highlight-accent);
  animation: climbStepsSquash 4.5s ease-in-out infinite;
  transform-origin: bottom center;
}
@keyframes climbStepsSquash {
  /* 起點準備：稍微壓扁 */
  0% { bottom: 3vw; left: 4vw; transform: scaleY(0.7) scaleX(1.3); }
  /* 起跳：拉長 */
  5% { transform: scaleY(1.4) scaleX(0.7); }
  /* 落地第一階 */
  20% { bottom: 9vw; left: 9vw; transform: scaleY(0.8) scaleX(1.2); }
  25% { transform: scaleY(1); }
  /* 起跳第二階 */
  35% { transform: scaleY(1.4) scaleX(0.7); }
  /* 落地第二階 */
  50% { bottom: 15vw; left: 14vw; transform: scaleY(0.8) scaleX(1.2); }
  55% { transform: scaleY(1); }
  /* 準備登頂 */
  65% { transform: scaleY(1.3) scaleX(0.7); }
  75% { bottom: 18vw; left: 18vw; transform: scaleY(1); opacity: 1; }
  90% { opacity: 0; transform: scale(0.5); }
  100% { bottom: 3vw; left: 4vw; opacity: 0; }
}"""
        },
        
        # 9. 神經多樣性 (大腦呼吸 + 光圈波紋擴散)
        9: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/neurodiversity.png" class="scene-img neuro-img" alt="神經多樣性大腦">
          <div class="brain-glow"></div>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.neuro-img { animation: brainPulse 5s ease-in-out infinite !important; z-index: 2; position: relative; }
.brain-glow {
  position: absolute;
  top: 15%;
  left: 15%;
  width: 70%;
  height: 70%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(220,168,66,0.3) 0%, rgba(82,133,140,0) 70%);
  animation: waveGlow 5s ease-in-out infinite;
  z-index: 1;
  pointer-events: none;
}
@keyframes brainPulse {
  0%, 100% { transform: scale(1) translateY(0); filter: drop-shadow(0 1vw 2vw rgba(82, 133, 140, 0.08)); }
  50% { transform: scale(1.04) translateY(-0.6vw); filter: drop-shadow(0 1.8vw 3vw rgba(82, 133, 140, 0.2)); }
}
@keyframes waveGlow {
  0%, 100% { transform: scale(0.9); opacity: 0.5; }
  50% { transform: scale(1.3); opacity: 1; }
}"""
        },
        
        # 10. 吸收方式不同 (三個不同自轉方向的 dashed 同心圓環 + 心跳縮放)
        10: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="rings-wrapper">
          <div class="ring ring-outer"></div>
          <div class="ring ring-middle"></div>
          <div class="ring ring-inner"></div>
        </div>
      </div>""",
            'css': """
.rings-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 25vw;
  height: 25vw;
  animation: heartPulseRings 4s ease-in-out infinite;
}
.ring {
  position: absolute;
  border-radius: 50%;
  border: 0.3vw dashed transparent;
}
.ring-outer {
  width: 22vw;
  height: 22vw;
  border-color: var(--color-primary);
  animation: spinRingCW 15s linear infinite;
}
.ring-middle {
  width: 15vw;
  height: 15vw;
  border-color: var(--color-highlight-accent);
  animation: spinRingCCW 10s linear infinite;
}
.ring-inner {
  width: 8vw;
  height: 8vw;
  border-color: var(--color-secondary);
  animation: spinRingCW 6s linear infinite;
}
@keyframes spinRingCW { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes spinRingCCW { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
@keyframes heartPulseRings {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.08); }
}"""
        },
        
        # 11. 1對30痛點 (學校場景浮動 + 焦慮紅圈閃爍)
        11: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/one_vs_thirty.png" class="scene-img school-img" alt="一位老師面對三十個學生">
          <div class="stress-mark mark-1">💢</div>
          <div class="stress-mark mark-2">💢</div>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.school-img { animation: schoolFloat 6s ease-in-out infinite !important; }
@keyframes schoolFloat {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 1vw 2vw rgba(44, 61, 77, 0.08)); }
  50% { transform: translateY(-0.8vw) scale(1.01); filter: drop-shadow(0 1.8vw 3vw rgba(44, 61, 77, 0.18)); }
}
.stress-mark {
  position: absolute;
  font-size: 2.5vw;
  animation: stressPulse 2.5s ease-in-out infinite;
  opacity: 0;
}
.mark-1 { top: 15%; left: 10%; animation-delay: 0.5s; }
.mark-2 { top: 25%; right: 10%; animation-delay: 1.5s; }
@keyframes stressPulse {
  0%, 100% { transform: scale(0.8) rotate(0deg); opacity: 0; }
  50% { transform: scale(1.2) rotate(10deg); opacity: 0.8; }
}"""
        },
        
        # 12. 帶上學習軌道 (小球在水平發光軌道上滑動 + 邊界撞擊發光)
        12: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="rail-container">
          <div class="rail-line">
            <div class="rail-car"></div>
          </div>
        </div>
      </div>""",
            'css': """
.rail-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28vw;
  height: 22vw;
}
.rail-line {
  position: relative;
  width: 100%;
  height: 0.6vw;
  background: rgba(44, 61, 77, 0.1);
  border-radius: 0.3vw;
}
.rail-car {
  position: absolute;
  top: -0.8vw;
  left: 0;
  width: 2.2vw;
  height: 2.2vw;
  border-radius: 50%;
  background: var(--color-primary);
  box-shadow: 0 0.4vw 1vw rgba(82, 133, 140, 0.3);
  animation: slideAndStretch 5s ease-in-out infinite;
}
@keyframes slideAndStretch {
  0%, 100% { left: 0%; transform: scaleX(1.3) scaleY(0.7); box-shadow: 0 0 1.5vw var(--color-highlight-accent); }
  5%, 95% { transform: scale(1); }
  50% { left: 90%; transform: scaleX(1.3) scaleY(0.7); box-shadow: 0 0 1.5vw var(--color-highlight-accent); }
  45%, 55% { transform: scale(1); }
}"""
        },
        
        # 13. 顧進度、顧考試 (三個小球拋接，加入旋轉與 3D 景深縮放)
        13: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="juggling-container">
          <div class="juggling-ball ball-a">進度</div>
          <div class="juggling-ball ball-b">班級</div>
          <div class="juggling-ball ball-c">考試</div>
        </div>
      </div>""",
            'css': """
.juggling-container {
  position: relative;
  width: 25vw;
  height: 22vw;
}
.juggling-ball {
  position: absolute;
  width: 6.5vw;
  height: 6.5vw;
  border-radius: 50%;
  color: #FFFFFF;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1vw;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0.6vw 1.5vw rgba(0,0,0,0.06);
}
.ball-a { background: var(--color-primary); animation: juggleA 4s ease-in-out infinite; }
.ball-b { background: var(--color-secondary); animation: juggleB 4s ease-in-out infinite; }
.ball-c { background: var(--color-highlight-accent); color: var(--color-secondary); animation: juggleC 4s ease-in-out infinite; }
@keyframes juggleA {
  0%, 100% { bottom: 1vw; left: 2vw; transform: scale(1); z-index: 2; }
  33% { bottom: 14vw; left: 9vw; transform: scale(0.85); z-index: 1; }
  66% { bottom: 1vw; left: 16vw; transform: scale(1.15); z-index: 3; }
}
@keyframes juggleB {
  0%, 100% { bottom: 1vw; left: 16vw; transform: scale(1.15); z-index: 3; }
  33% { bottom: 1vw; left: 2vw; transform: scale(1); z-index: 2; }
  66% { bottom: 14vw; left: 9vw; transform: scale(0.85); z-index: 1; }
}
@keyframes juggleC {
  0%, 100% { bottom: 14vw; left: 9vw; transform: scale(0.85); z-index: 1; }
  33% { bottom: 1vw; left: 16vw; transform: scale(1.15); z-index: 3; }
  66% { bottom: 1vw; left: 2vw; transform: scale(1); z-index: 2; }
}"""
        },
        
        # 14. 量身規劃這太難了 (兩塊拼圖嘗試結合後彈開)
        14: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="puzzle-wrapper">
          <div class="puzzle-part part-left">🧩</div>
          <div class="puzzle-part part-right">🧩</div>
        </div>
      </div>""",
            'css': """
.puzzle-wrapper {
  position: relative;
  width: 25vw;
  height: 22vw;
}
.puzzle-part {
  position: absolute;
  font-size: 6vw;
  transition: all 0.3s ease;
  user-select: none;
}
.part-left {
  top: 4vw;
  left: 2vw;
  animation: floatPuzzleLeft 5s ease-in-out infinite;
}
.part-right {
  top: 6vw;
  right: 2vw;
  transform: rotate(180deg);
  filter: hue-rotate(90deg);
  animation: floatPuzzleRight 5s ease-in-out infinite;
}
@keyframes floatPuzzleLeft {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  45% { transform: translate(4.5vw, 1vw) rotate(5deg); }
  55% { transform: translate(4.5vw, 1vw) rotate(5deg); }
}
@keyframes floatPuzzleRight {
  0%, 100% { transform: translate(0, 0) rotate(180deg); }
  45% { transform: translate(-4.5vw, -1vw) rotate(175deg); }
  55% { transform: translate(-4.5vw, -1vw) rotate(175deg); }
}"""
        },
        
        # 15. 自我決定論卡片選單 (響應式改動 - 卡片微傾斜 3D 浮動效果已在主 HTML 與新 CSS 中)
        15: {
            'type': 'text',
            'css': """
/* 已在 html 覆蓋，保留樣式，轉換單位為 vw */
.text-wrapper .animate-line {
  font-size: 3.8vw !important;
}
.interactive-cards {
  gap: 2.5vw !important;
  margin-top: 3vw !important;
  min-width: unset !important;
  max-width: 90% !important;
}
.card {
  padding: 2vw 1.5vw !important;
  border-radius: 1.5vw !important;
  border-width: 0.2vw !important;
}
.card-icon {
  font-size: 4vw !important;
}
.card h3 {
  font-size: 2.2vw !important;
}
.status-badge {
  font-size: 1.3vw !important;
  padding: 0.4vw 1.2vw !important;
  border-radius: 1.2vw !important;
}
.continue-btn {
  padding: 1vw 2.8vw !important;
  border-radius: 2.5vw !important;
  font-size: 1.8vw !important;
}
"""
        },
        
        # 16. 自主感 (大圖 + 返回按鈕 + 指針微晃動)
        16: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/autonomy.png" class="scene-img autonomy-img" alt="自主感">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 2vw; right: 2vw; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.autonomy-img { animation: autonomyFloat 6s ease-in-out infinite !important; }
@keyframes autonomyFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); filter: drop-shadow(0 1.5vw 3vw rgba(82, 133, 140, 0.08)); }
  50% { transform: translateY(-0.7vw) rotate(1.5deg); filter: drop-shadow(0 2vw 4vw rgba(82, 133, 140, 0.22)); }
}
.back-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  padding: 1vw 2.2vw;
  border-radius: 2.5vw;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.6vw;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0.6vw 2vw rgba(82, 133, 140, 0.25);
  transition: all 0.2s ease;
}
.back-btn:hover {
  background: var(--color-secondary);
  transform: translateY(-0.2vw);
  box-shadow: 0 0.8vw 2.5vw rgba(82, 133, 140, 0.35);
}"""
        },
        
        # 17. 勝任感 (大圖 + 金色星星環繞)
        17: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/competence.png" class="scene-img competence-img" alt="勝任感">
          <div class="trophy-sparkle">✨</div>
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 2vw; right: 2vw; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.competence-img { animation: competenceFloat 6s ease-in-out infinite !important; }
.trophy-sparkle {
  position: absolute;
  top: 10%;
  right: 10%;
  font-size: 3vw;
  color: var(--color-highlight-accent);
  animation: shineCompetence 3s ease-in-out infinite;
}
@keyframes competenceFloat {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 1.5vw 3vw rgba(82, 133, 140, 0.08)); }
  50% { transform: translateY(-0.8vw) scale(1.025); filter: drop-shadow(0 2.2vw 4vw rgba(82, 133, 140, 0.22)); }
}
@keyframes shineCompetence {
  0%, 100% { transform: scale(0.6) rotate(0deg); opacity: 0.5; }
  50% { transform: scale(1.2) rotate(45deg); opacity: 1; filter: drop-shadow(0 0 1vw var(--color-highlight-accent)); }
}
.back-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  padding: 1vw 2.2vw;
  border-radius: 2.5vw;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.6vw;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0.6vw 2vw rgba(82, 133, 140, 0.25);
  transition: all 0.2s ease;
}
.back-btn:hover {
  background: var(--color-secondary);
  transform: translateY(-0.2vw);
  box-shadow: 0 0.8vw 2.5vw rgba(82, 133, 140, 0.35);
}"""
        },
        
        # 18. 歸屬感 (大圖 + 綠色小水滴澆灌動效)
        18: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="溫暖呵護手捧樹苗">
          <div class="water-drop">💧</div>
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 2vw; right: 2vw; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.guide-img { animation: seedlingGrow 6s ease-in-out infinite !important; }
.water-drop {
  position: absolute;
  top: 10%;
  left: 45%;
  font-size: 2vw;
  animation: dropWater 4s ease-in infinite;
  opacity: 0;
}
@keyframes seedlingGrow {
  0%, 100% { transform: translateY(0) scale(1); filter: brightness(1) drop-shadow(0 1.5vw 2.5vw rgba(82, 133, 140, 0.15)); }
  50% { transform: translateY(-0.5vw) scale(1.01); filter: brightness(1.06) drop-shadow(0 2.2vw 3.5vw rgba(82, 133, 140, 0.25)); }
}
@keyframes dropWater {
  0% { top: 5%; opacity: 0; transform: scale(0.5); }
  30% { opacity: 0.9; transform: scale(1); }
  60% { top: 50%; opacity: 0; transform: scale(0.6); }
  100% { top: 5%; opacity: 0; }
}
.back-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  padding: 1vw 2.2vw;
  border-radius: 2.5vw;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.6vw;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0.6vw 2vw rgba(82, 133, 140, 0.25);
  transition: all 0.2s ease;
}
.back-btn:hover {
  background: var(--color-secondary);
  transform: translateY(-0.2vw);
  box-shadow: 0 0.8vw 2.5vw rgba(82, 133, 140, 0.35);
}"""
        },
        
        # 19. AI 貼合節奏 (機器人 + 藍綠色雷達探測波紋)
        19: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/ai_mentor.png" class="scene-img ai-img" alt="AI陪伴學習">
          <div class="radar-wave"></div>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.ai-img { animation: aiFloat 5.5s ease-in-out infinite !important; position: relative; z-index: 2; }
.radar-wave {
  position: absolute;
  top: 25%;
  left: 25%;
  width: 50%;
  height: 50%;
  border-radius: 50%;
  border: 0.2vw solid var(--color-primary);
  animation: radarWavePulse 4s cubic-bezier(0.1, 0.8, 0.3, 1) infinite;
  z-index: 1;
  opacity: 0;
}
@keyframes aiFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); filter: drop-shadow(0 1.5vw 3vw rgba(82, 133, 140, 0.06)); }
  50% { transform: translateY(-0.8vw) rotate(0.8deg); filter: drop-shadow(0 2.2vw 4vw rgba(82, 133, 140, 0.18)); }
}
@keyframes radarWavePulse {
  0% { transform: scale(0.6); opacity: 0.8; }
  100% { transform: scale(1.6); opacity: 0; border-color: var(--color-highlight-accent); }
}"""
        },
        
        # 20. 多元選擇 (點擊卡片彈出說明互動 + 互動微彈跳 - 響應式優化)
        20: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="media-choices-wrapper">
          <div class="media-card card-visual" onclick="showMediaTip('visual')">
            <div class="media-icon">🎨</div>
            <span>圖像</span>
            <div class="click-badge">點選</div>
          </div>
          <div class="media-card card-video" onclick="showMediaTip('video')">
            <div class="media-icon">🎬</div>
            <span>影像</span>
            <div class="click-badge">點選</div>
          </div>
          <div class="media-card card-audio" onclick="showMediaTip('audio')">
            <div class="media-icon">🎵</div>
            <span>聽覺</span>
            <div class="click-badge">點選</div>
          </div>
          <div id="media-tip-popup" class="media-tip-popup" style="display: none;"></div>
        </div>
        <script>
          function showMediaTip(type) {
            const popup = document.getElementById('media-tip-popup');
            const tips = {
              visual: '🎨 <b>圖像學習</b>：心智圖、插圖與顏色對比，最容易在大腦留下直覺的結構記憶！',
              video: '🎬 <b>影像學習</b>：動畫步驟、3D 圖形、動態原理拆解，讓概念躍然紙上！',
              audio: '🎵 <b>聽覺學習</b>：同理心口語解說、陪伴式語音反饋，極大增強對話溫暖與歸屬感！'
            };
            popup.innerHTML = tips[type];
            popup.style.display = 'block';
            popup.classList.remove('fade-in');
            void popup.offsetWidth;
            popup.classList.add('fade-in');
          }
        </script>
      </div>""",
            'css': """
.media-choices-wrapper {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.6vw;
  width: 32vw;
  height: 25vw;
}
.media-card {
  position: relative;
  flex: 1;
  min-width: 8vw;
  height: 12vw;
  background: rgba(255, 255, 255, 0.6);
  border: 0.15vw solid rgba(82, 133, 140, 0.15);
  border-radius: 1.2vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.2vw 0.6vw;
  cursor: pointer;
  box-shadow: 0 0.4vw 1vw rgba(0,0,0,0.03);
  transition: all 0.22s ease;
  user-select: none;
}
.media-card:hover {
  transform: translateY(-0.8vw) scale(1.08);
  border-color: var(--color-primary);
  background: #FFFFFF;
  box-shadow: 0 1vw 2vw rgba(82, 133, 140, 0.15);
}
.media-card:hover .media-icon {
  animation: iconBounce 0.6s ease-in-out infinite alternate;
}
@keyframes iconBounce {
  from { transform: translateY(0); }
  to { transform: translateY(-0.4vw); }
}
.media-icon { font-size: 2.5vw; margin-bottom: 0.6vw; }
.media-card span { font-size: 1vw; font-weight: 700; color: var(--color-text-main); }

.click-badge {
  position: absolute;
  bottom: -0.8vw;
  background: var(--color-highlight-accent);
  color: #FFFFFF;
  font-size: 0.7vw;
  font-weight: 900;
  padding: 0.2vw 0.6vw;
  border-radius: 0.8vw;
  box-shadow: 0 0.2vw 0.6vw rgba(220, 168, 66, 0.3);
}

.media-tip-popup {
  width: 100%;
  background: var(--color-secondary);
  color: #FFFFFF;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1vw;
  line-height: 1.4;
  padding: 1vw 1.4vw;
  border-radius: 0.8vw;
  box-shadow: 0 0.6vw 1.5vw rgba(44, 61, 77, 0.15);
  margin-top: 1.2vw;
  text-align: left;
}"""
        },
        
        # 21. 選擇權與建立自主感 (點擊按鈕手勢 + 水紋波紋漣漪)
        21: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="click-demo-container">
          <div class="click-btn btn-a">語法探索</div>
          <div class="click-btn btn-b">實作模擬<div class="ripple-ring"></div></div>
          <div class="click-hand">👆</div>
        </div>
      </div>""",
            'css': """
.click-demo-container {
  position: relative;
  width: 25vw;
  height: 22vw;
  background: rgba(255, 255, 255, 0.4);
  border: 0.1vw solid rgba(82, 133, 140, 0.1);
  border-radius: 1.6vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2vw;
}
.click-btn {
  position: relative;
  padding: 0.8vw 2.4vw;
  background: #FFFFFF;
  border: 0.2vw solid rgba(82, 133, 140, 0.15);
  border-radius: 2vw;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1vw;
  font-weight: 700;
  color: var(--color-text-main);
  box-shadow: 0 0.3vw 0.6vw rgba(0,0,0,0.02);
  transition: all 0.2s ease;
}
.click-hand {
  position: absolute;
  font-size: 3vw;
  bottom: 1vw;
  right: 4vw;
  user-select: none;
  animation: simulateClickAndPop 4s ease-in-out infinite;
}
.ripple-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1vw;
  height: 1vw;
  background: transparent;
  border: 0.2vw solid var(--color-highlight-accent);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(1);
  opacity: 0;
  pointer-events: none;
}
@keyframes simulateClickAndPop {
  0%, 100% { transform: translate(0, 0) scale(1); }
  40% { transform: translate(-3vw, -7vw) scale(1); }
  48% { transform: translate(-3vw, -7vw) scale(0.85); }
  55% { transform: translate(-3vw, -7vw) scale(1); }
}
.btn-b {
  animation: btnHighlightAction 4s linear infinite;
}
.btn-b .ripple-ring {
  animation: rippleSpread 4s linear infinite;
}
@keyframes btnHighlightAction {
  0%, 46%, 70%, 100% { border-color: rgba(82, 133, 140, 0.15); background: #FFFFFF; }
  50%, 65% { border-color: var(--color-primary); background: rgba(82, 133, 140, 0.08); box-shadow: 0 0 1vw rgba(82, 133, 140, 0.2); }
}
@keyframes rippleSpread {
  0%, 47%, 70%, 100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  60% { opacity: 0; transform: translate(-50%, -50%) scale(2.8); }
}"""
        },
        
        # 22. AI Patience 講100遍 (已經在 HTML 中覆蓋互動邏輯，只需定義 CSS - 響應式 vw 轉換)
        22: {
            'type': 'text',
            'css': """
.interactive-btn {
  padding: 0.8vw 1.8vw !important;
  border-radius: 2vw !important;
  font-size: 1.1vw !important;
  margin-top: 1.6vw !important;
  border-width: 0.2vw !important;
}
.color-ai {
  font-size: 2.1vw !important;
  line-height: 1.6 !important;
}
.continue-btn {
  padding: 1vw 2.4vw !important;
  border-radius: 2vw !important;
  font-size: 1.2vw !important;
  margin-top: 1.6vw !important;
}
"""
        },
        
        # 23. 跟不上別人 (落後小球喘氣發抖動畫)
        23: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="running-track">
          <div class="runner runner-fast-1"></div>
          <div class="runner runner-fast-2"></div>
          <div class="runner runner-slow"></div>
        </div>
      </div>""",
            'css': """
.running-track {
  position: relative;
  width: 28vw;
  height: 20vw;
  background: rgba(255, 255, 255, 0.4);
  border: 0.1vw solid rgba(82, 133, 140, 0.1);
  border-radius: 1.2vw;
}
.runner {
  position: absolute;
  width: 1.6vw;
  height: 1.6vw;
  border-radius: 50%;
}
.runner-fast-1 { top: 4vw; background: var(--color-secondary); animation: runFast1 5s linear infinite; }
.runner-fast-2 { top: 9vw; background: var(--color-highlight-accent); animation: runFast2 5s linear infinite; }
.runner-slow { top: 14vw; background: var(--color-primary); animation: runSlowAndPant 5s linear infinite; }
@keyframes runFast1 { 0% { left: 10%; } 100% { left: 85%; } }
@keyframes runFast2 { 0% { left: 10%; } 100% { left: 78%; } }
@keyframes runSlowAndPant {
  0% { left: 10%; transform: scale(1); }
  50% { left: 30%; transform: scale(1.1) translateY(-0.1vw); }
  75% { transform: scale(0.9) translateY(0.1vw); }
  100% { left: 45%; transform: scale(1); }
}"""
        },
        
        # 24. 隨時想問就問 (新增打字中 dot-dot-dot 效果)
        24: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="chat-box-wrapper">
          <div class="chat-bubble bubble-left">我這個部分還是不懂...</div>
          <div class="chat-bubble bubble-right">
            <span class="typing-dots" id="dots-anim">沒問題，我們再換個方式說一遍！💡</span>
          </div>
        </div>
      </div>""",
            'css': """
.chat-box-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2vw;
  width: 30vw;
  height: 22vw;
  justify-content: center;
}
.chat-bubble {
  padding: 1.2vw 1.8vw;
  border-radius: 1.8vw;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1vw;
  font-weight: 700;
  box-shadow: 0 0.4vw 1vw rgba(0,0,0,0.03);
  max-width: 85%;
}
.bubble-left {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.7);
  border: 0.15vw solid rgba(82, 133, 140, 0.15);
  color: var(--color-text-main);
  animation: fadeBubble1 4s ease-in-out infinite;
}
.bubble-right {
  align-self: flex-end;
  background: var(--color-primary);
  color: #FFFFFF;
  animation: fadeBubble2 4s ease-in-out infinite;
}
@keyframes fadeBubble1 { 0%, 100% { opacity: 0; transform: scale(0.85); } 10%, 90% { opacity: 1; transform: scale(1); } }
@keyframes fadeBubble2 { 0%, 30%, 100% { opacity: 0; transform: scale(0.85); } 40%, 90% { opacity: 1; transform: scale(1); } }"""
        },
        
        # 25. 給予充足時間學得會 (新增鐘擺擺動動畫)
        25: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="clock-wrapper">
          <div class="clock-face">
            <div class="clock-hand-hour"></div>
            <div class="clock-hand-minute"></div>
            <div class="pendulum"></div>
          </div>
        </div>
      </div>""",
            'css': """
.clock-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 25vw;
  height: 22vw;
}
.clock-face {
  position: relative;
  width: 15vw;
  height: 15vw;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  border: 0.4vw solid var(--color-primary);
}
.clock-hand-hour, .clock-hand-minute {
  position: absolute;
  background: var(--color-text-main);
  border-radius: 0.2vw;
  transform-origin: bottom center;
  bottom: 50%;
  left: calc(50% - 0.2vw);
}
.clock-hand-hour {
  width: 0.4vw;
  height: 3.5vw;
  animation: spinHand 20s linear infinite;
}
.clock-hand-minute {
  width: 0.3vw;
  height: 5.5vw;
  background: var(--color-highlight-accent);
  animation: spinHand 4s linear infinite;
}
.pendulum {
  position: absolute;
  width: 0.4vw;
  height: 4vw;
  background: var(--color-primary);
  top: 90%;
  left: calc(50% - 0.2vw);
  transform-origin: top center;
  animation: swingPendulum 2s ease-in-out infinite;
}
.pendulum::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: -0.6vw;
  width: 1.6vw;
  height: 1.6vw;
  border-radius: 50%;
  background: var(--color-primary);
}
@keyframes spinHand { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes swingPendulum {
  0%, 100% { transform: rotate(-15deg); }
  50% { transform: rotate(15deg); }
}"""
        },
        
        # 26. 建立勝任感 (能量條手動充能 + 100% 黃金波動特效 - 響應式優化)
        26: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="progress-box">
          <span class="progress-title" id="charge-title">勝任感充能</span>
          <div class="progress-bg">
            <div class="progress-fill" id="bar-fill"></div>
          </div>
          <div style="display: flex; align-items: center; width: 100%; justify-content: space-between; margin-top: 0.5vw;">
            <span class="percent-label" id="percent-label">99%</span>
            <button class="charge-btn glow-pulse" onclick="manualCharge()">⚡ 充能</button>
          </div>
        </div>
        <script>
          function manualCharge() {
            const bar = document.getElementById('bar-fill');
            const percent = document.getElementById('percent-label');
            const title = document.getElementById('charge-title');
            
            bar.style.animation = 'none';
            percent.style.animation = 'none';
            void bar.offsetWidth;
            
            bar.style.width = '100%';
            bar.style.background = 'var(--color-highlight-accent)';
            bar.style.boxShadow = '0 0 1.5vw var(--color-highlight-accent)';
            
            percent.textContent = '100%';
            percent.style.color = 'var(--color-highlight-accent)';
            title.innerHTML = '勝任感滿足！🎉';
            title.style.color = 'var(--color-highlight-accent)';
          }
        </script>
      </div>""",
            'css': """
.progress-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.6vw;
  width: 28vw;
  height: 20vw;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 1.6vw;
  border: 0.15vw solid rgba(82, 133, 140, 0.15);
  padding: 2.4vw;
}
.progress-title {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95vw;
  font-weight: 700;
  color: var(--color-text-main);
  transition: all 0.3s ease;
}
.progress-bg {
  width: 100%;
  height: 1.6vw;
  background: rgba(44, 61, 77, 0.08);
  border-radius: 0.8vw;
  overflow: hidden;
}
.progress-fill {
  width: 0%;
  height: 100%;
  background: var(--color-primary);
  border-radius: 0.8vw;
  animation: fillProgress 4s ease-in-out infinite;
  transition: all 0.3s ease;
}
.percent-label {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.2vw;
  font-weight: 900;
  color: var(--color-primary);
  animation: countUp 4s linear infinite;
  transition: all 0.3s ease;
}
.charge-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.8vw;
  font-weight: 700;
  padding: 0.4vw 1.2vw;
  border-radius: 1.2vw;
  cursor: pointer;
  box-shadow: 0 0.4vw 1vw rgba(82, 133, 140, 0.2);
  transition: all 0.2s ease;
}
.charge-btn:hover {
  background: var(--color-secondary);
  transform: scale(1.05);
}
@keyframes fillProgress { 0% { width: 0%; } 80%, 100% { width: 99%; } }
@keyframes countUp {
  0% { content: '0%'; opacity: 0.8; }
  80%, 100% { content: '99%'; opacity: 1; }
}"""
        },
        
        # 27. 家長老師有餘裕 (放鬆漂浮熱氣球 + 風動搖晃效果)
        27: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="balloon-wrapper">
          <div class="hot-balloon">🎈</div>
          <div class="cloud-dec cloud-1">☁️</div>
          <div class="cloud-dec cloud-2">☁️</div>
        </div>
      </div>""",
            'css': """
.balloon-wrapper {
  position: relative;
  width: 25vw;
  height: 25vw;
}
.hot-balloon {
  position: absolute;
  font-size: 5.5vw;
  top: 30%;
  left: 35%;
  user-select: none;
  animation: balloonFloatAndTilt 6s ease-in-out infinite;
}
.cloud-dec {
  position: absolute;
  font-size: 2.5vw;
  color: rgba(255, 255, 255, 0.85);
  opacity: 0.7;
}
.cloud-1 { top: 15%; left: 10%; animation: cloudMove1 12s linear infinite; }
.cloud-2 { top: 55%; right: 10%; animation: cloudMove2 9s linear infinite; }
@keyframes balloonFloatAndTilt {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-1.6vw) rotate(4deg); }
}
@keyframes cloudMove1 {
  0% { transform: translateX(0); }
  50% { transform: translateX(1.5vw); }
  100% { transform: translateX(0); }
}
@keyframes cloudMove2 {
  0% { transform: translateX(0); }
  50% { transform: translateX(-1.2vw); }
  100% { transform: translateX(0); }
}"""
        },
        
        # 28. 走進內心 (愛心進行真實心跳 double-pulse 律動)
        28: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="heart-container">
          <div class="heart-shape">💗</div>
        </div>
      </div>""",
            'css': """
.heart-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 25vw;
  height: 25vw;
}
.heart-shape {
  font-size: 6.5vw;
  animation: realHeartBeat 2.5s ease-in-out infinite;
}
@keyframes realHeartBeat {
  /* 真實心跳：縮放、稍微回彈、再次強力收縮 */
  0%, 100% { transform: scale(1); opacity: 0.85; filter: drop-shadow(0 0.8vw 1.5vw rgba(82, 133, 140, 0.1)); }
  15% { transform: scale(1.15); opacity: 1; filter: drop-shadow(0 1vw 2.5vw rgba(82, 133, 140, 0.2)); }
  28% { transform: scale(1.05); }
  40% { transform: scale(1.25); opacity: 1; filter: drop-shadow(0 1.2vw 3vw rgba(82, 133, 140, 0.3)); }
  60% { transform: scale(1); opacity: 0.85; }
}"""
        },
        
        # 29. 歸屬感建立 (去重：純 CSS 溫馨避風港 + 煙囪裊裊炊煙 + 愛心升空動畫)
        29: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="haven-container">
          <div class="haven-house">🏡</div>
          <div class="haven-smoke">💨</div>
          <div class="haven-heart haven-heart-1">🧡</div>
          <div class="haven-heart haven-heart-2">✨</div>
          <div class="haven-heart haven-heart-3">💖</div>
        </div>
      </div>""",
            'css': """
.haven-container {
  position: relative;
  width: 25vw;
  height: 25vw;
  display: flex;
  align-items: center;
  justify-content: center;
}
.haven-house {
  font-size: 6.5vw;
  animation: housePulse 4s ease-in-out infinite;
  filter: drop-shadow(0 1vw 2.5vw rgba(82, 133, 140, 0.15));
  position: relative;
  z-index: 2;
}
.haven-smoke {
  position: absolute;
  top: 15%;
  right: 25%;
  font-size: 1.5vw;
  opacity: 0;
  animation: chimneySmoke 4s ease-in-out infinite;
  z-index: 1;
}
@keyframes housePulse {
  0%, 100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.06); filter: brightness(1.08) drop-shadow(0 1.5vw 3.5vw rgba(82, 133, 140, 0.25)); }
}
@keyframes chimneySmoke {
  0% { transform: translateY(0) scale(0.6); opacity: 0; }
  30% { opacity: 0.7; }
  80% { opacity: 0; }
  100% { transform: translateY(-3vw) scale(1.5); opacity: 0; }
}
.haven-heart {
  position: absolute;
  font-size: 1.8vw;
  opacity: 0;
  user-select: none;
  z-index: 3;
}
.haven-heart-1 {
  top: 35%;
  left: 20%;
  animation: floatUpHeart1 6s ease-in-out infinite;
}
.haven-heart-2 {
  top: 25%;
  right: 20%;
  animation: floatUpHeart2 7s ease-in-out infinite;
}
.haven-heart-3 {
  top: 15%;
  left: 45%;
  animation: floatUpHeart3 5s ease-in-out infinite;
}
@keyframes floatUpHeart1 {
  0% { transform: translateY(2vw) scale(0.6); opacity: 0; }
  30% { opacity: 0.8; }
  90% { opacity: 0.8; }
  100% { transform: translateY(-5vw) scale(1.1) rotate(-15deg); opacity: 0; }
}
@keyframes floatUpHeart2 {
  0% { transform: translateY(3vw) scale(0.5); opacity: 0; }
  40% { opacity: 0.9; }
  90% { opacity: 0.9; }
  100% { transform: translateY(-6vw) scale(1) rotate(15deg); opacity: 0; }
}
@keyframes floatUpHeart3 {
  0% { transform: translateY(1.5vw) scale(0.7); opacity: 0; }
  30% { opacity: 0.95; }
  90% { opacity: 0.95; }
  100% { transform: translateY(-4.5vw) scale(1.2) rotate(10deg); opacity: 0; }
}"""
        },
        
        # 30. 缺了動力電池充電 (點擊充電切換 + 充滿後閃爍 ⚡ 粒子)
        30: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s" onclick="toggleBatteryCharge()">
        <div class="battery-wrapper" style="cursor: pointer;">
          <div class="battery-body">
            <div class="battery-fill" id="bat-fill"></div>
          </div>
          <div class="battery-tip"></div>
          <span class="charge-label" id="bat-label">動力不足</span>
          <div class="click-badge" style="bottom: 0vw;">點擊充電 ⚡</div>
          <div class="spark-sparkle" id="bat-spark">⚡</div>
        </div>
        <script>
          let isCharged = false;
          function toggleBatteryCharge() {
            const fill = document.getElementById('bat-fill');
            const label = document.getElementById('bat-label');
            const spark = document.getElementById('bat-spark');
            
            fill.style.animation = 'none';
            label.style.animation = 'none';
            void fill.offsetWidth;
            
            isCharged = !isCharged;
            if (isCharged) {
              fill.style.width = '100%';
              fill.style.background = 'var(--color-primary)';
              fill.style.boxShadow = '0 0 1.2vw var(--color-primary)';
              label.textContent = '動力充滿！';
              label.style.color = 'var(--color-primary)';
              spark.style.display = 'block';
            } else {
              fill.style.width = '0%';
              fill.style.background = '#E26D5C';
              fill.style.boxShadow = 'none';
              label.textContent = '動力不足';
              label.style.color = '#E26D5C';
              spark.style.display = 'none';
            }
          }
        </script>
      </div>""",
            'css': """
.battery-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 25vw;
  height: 22vw;
  gap: 2vw;
}
.battery-body {
  position: relative;
  width: 14vw;
  height: 7vw;
  border: 0.4vw solid var(--color-secondary);
  border-radius: 0.8vw;
  padding: 0.4vw;
}
.battery-tip {
  position: absolute;
  top: calc(50% - 1.8vw);
  right: 4.3vw;
  width: 0.8vw;
  height: 2vw;
  background: var(--color-secondary);
  border-radius: 0 0.4vw 0.4vw 0;
}
.battery-fill {
  width: 0%;
  height: 100%;
  background: var(--color-secondary);
  border-radius: 0.4vw;
  animation: chargeBattery 4s cubic-bezier(0.12, 0, 0.39, 0) infinite;
  transition: all 0.3s ease;
}
.charge-label {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95vw;
  font-weight: 700;
  color: var(--color-text-main);
  animation: changeLabel 4s step-end infinite;
  transition: all 0.3s ease;
}
.click-badge {
  position: absolute;
  bottom: 0vw;
  background: var(--color-highlight-accent);
  color: #FFFFFF;
  font-size: 0.7vw;
  font-weight: 900;
  padding: 0.2vw 0.6vw;
  border-radius: 0.8vw;
  box-shadow: 0 0.2vw 0.6vw rgba(220, 168, 66, 0.3);
}
.spark-sparkle {
  position: absolute;
  top: 15%;
  right: 15%;
  font-size: 2vw;
  color: var(--color-highlight-accent);
  display: none;
  animation: sparkleFlash 1.5s ease-in-out infinite alternate;
}
@keyframes chargeBattery {
  0% { width: 0%; background: #E26D5C; }
  35% { width: 40%; background: #E26D5C; }
  70%, 100% { width: 100%; background: var(--color-primary); }
}
@keyframes changeLabel {
  0%, 69% { content: '動力不足'; color: #E26D5C; }
  70%, 100% { content: '動力充滿！'; color: var(--color-primary); }
}
@keyframes sparkleFlash {
  from { transform: scale(0.8) rotate(0deg); filter: brightness(1); }
  to { transform: scale(1.2) rotate(15deg); filter: brightness(1.3); }
}"""
        },
        
        # 31. 願意學 (最後一頁：換成主 LOGO 並將背景色設為純白，周圍加入亮色門縫呼吸光效)
        31: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper logo-wrapper">
          <img src="../assets/logo.png" class="scene-img final-logo-img" alt="願意學 LOGO">
        </div>
      </div>""",
            'css': """
body {
  background: #FFFFFF !important; /* 與 Logo 的白色背景完美融合，不留邊界 */
}
.image-wrapper.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.final-logo-img {
  max-width: 100%;
  max-height: 25vw !important; /* 限制最大高度，防止 Logo 過大擠壓 */
  object-fit: contain;
  animation: finalLogoGlow 5s ease-in-out infinite !important;
}
@keyframes finalLogoGlow {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0.5vw 1.2vw rgba(255, 110, 64, 0.15)); }
  50% { transform: scale(1.03); filter: drop-shadow(0 1vw 2.4vw rgba(255, 110, 64, 0.35)); }
}"""
        }
    }

    # 執行批次更新
    for scene_num in range(1, 32):
        if scene_num not in scene_rules:
            continue
            
        rule = scene_rules[scene_num]
        
        html_file = os.path.join(scenes_dir, f"scene{scene_num}.html")
        css_file = os.path.join(scenes_dir, f"scene{scene_num}.css")
        
        if not os.path.exists(html_file) or not os.path.exists(css_file):
            print(f"File not found: scene{scene_num}")
            continue

        # 1. 處理 HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        p_matches = re.findall(r'(<p[^>]*class="animate-line[^>]*">[\s\S]*?</p>)', html_content)
        p_tags_cleaned = "\n        ".join([p.strip() for p in p_matches])

        # 如果規則要求 split
        if rule['type'] == 'split':
            inner_container = f"""  <div class="scene-container">
    <div class="scene-split-container">
      <div class="text-side">
        {p_tags_cleaned}
      </div>
{rule['visual']}
    </div>
  </div>"""
            # 替換 HTML 中的 scene-container 區塊
            container_pattern = r'  <div class="scene-container">[\s\S]*?  </div>\n\n  <script>'
            new_html_content = re.sub(container_pattern, inner_container + "\n\n  <script>", html_content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_html_content)
            print(f"HTML Scene {scene_num} updated to Split-Screen.")
        else:
            # 純文字或已經手動修改好的特殊模式（如 15, 22）
            print(f"HTML Scene {scene_num} layout preserved.")

        # 2. 處理 CSS
        if rule['type'] == 'split':
            css_template = f"""/* scene{scene_num}.css - 第 {scene_num} 幕專屬樣式 */

body {{
  background: linear-gradient(135deg, var(--color-bg-light) 0%, var(--color-accent) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}}

.text-side .animate-line {{
  font-family: "Noto Sans TC", sans-serif;
  font-size: 3.8vw; /* 採用響應式 vw，避免在行動端因為 font-size 不縮放導致圖形被擠壓卡掉 */
  font-weight: 700;
  color: var(--color-text-main);
  margin: 1.5vw 0;
  letter-spacing: 0.05em;
  line-height: 1.5;
  text-shadow: 0 0.2vw 1vw rgba(0, 0, 0, 0.02);
}}
{rule['css']}"""
            
            # 特別處理最後一幕
            if scene_num == 31:
                css_template += """
.text-side .animate-line:nth-child(2) {
  font-family: "Noto Serif TC", serif;
  font-size: 4.5vw;
  color: var(--color-primary) !important;
  font-weight: 900;
  margin-top: 2vw;
}
.text-side .animate-line:nth-child(3) {
  font-size: 2.5vw;
  color: var(--color-secondary) !important;
  font-weight: 700;
}
"""
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_template)
            print(f"CSS Scene {scene_num} styles updated.")
        else:
            # 對於非 split 的場景，若有定義 rule['css']，將其覆蓋或寫入
            if rule['css']:
                # scene 15, 22 已經在先前建立了，我們只更新其 CSS 中與 vw/響應式相關的部分
                with open(css_file, 'r', encoding='utf-8') as f:
                    old_css = f.read()
                
                # 簡單地把 rule['css'] 的定義附加在尾端以覆蓋樣式
                if "vw" not in old_css or "card-icon" not in old_css:
                    with open(css_file, 'a', encoding='utf-8') as f:
                        f.write("\\n" + rule['css'])
                    print(f"CSS Scene {scene_num} responsive styles appended.")
            
    print("\n恭喜！31 幕畫面與 CSS 圖文相符全域重組完畢！")

if __name__ == '__main__':
    rebuild()

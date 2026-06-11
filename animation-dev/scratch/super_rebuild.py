# super_rebuild.py
import os
import re

def rebuild():
    scenes_dir = r"C:\Users\wkoyo\Documents\家教網站\animation-dev\scenes"
    
    # 31 幕的排版、配圖與 CSS 動效規則
    # 'type': 'split' (左右分割)
    # 'visual': 右側 HTML 內容
    # 'css': 該幕專屬的 CSS 樣式與動畫 keyframes
    scene_rules = {
        # 1. 家長懊惱 (大圖 + 焦慮氣泡)
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
/* 焦慮懊惱情境動態 */
.image-wrapper { position: relative; display: inline-block; }
.anxiety-img { animation: swayAnxiety 6s ease-in-out infinite !important; }
@keyframes swayAnxiety {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
  50% { transform: translateY(-8px) rotate(-1.5deg) scale(1.015); }
}
.bubble {
  position: absolute;
  background: rgba(82, 133, 140, 0.08);
  color: var(--color-primary);
  border: 1.5px solid rgba(82, 133, 140, 0.25);
  font-family: "Noto Sans TC", sans-serif;
  font-weight: 900;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(82, 133, 140, 0.05);
  user-select: none;
}
.bubble-1 { width: 50px; height: 50px; font-size: 1.5rem; top: 15%; left: -5%; animation: bubbleFloat1 8s ease-in-out infinite; }
.bubble-2 { width: 40px; height: 40px; font-size: 1.2rem; top: 30%; right: -2%; animation: bubbleFloat2 10s ease-in-out infinite; }
.bubble-3 { width: 46px; height: 46px; font-size: 1.3rem; bottom: 20%; left: 5%; animation: bubbleFloat3 9s ease-in-out infinite; }
@keyframes bubbleFloat1 {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.7; }
  50% { transform: translateY(-12px) rotate(15deg); opacity: 1; }
}
@keyframes bubbleFloat2 {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
  50% { transform: translateY(-8px) rotate(-15deg); opacity: 0.9; }
}
@keyframes bubbleFloat3 {
  0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.75; }
  50% { transform: translateY(-15px) rotate(10deg); opacity: 1; }
}"""
        },
        
        # 2. 我並不這麼認為 (CSS 動態翻轉指針與問號轉驚嘆號)
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
  width: 260px;
  height: 260px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  border: 3px dashed var(--color-primary);
  animation: pulseBg 4s ease-in-out infinite;
}
.flip-symbol {
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--color-primary);
  animation: flipText 5s ease-in-out infinite;
}
@keyframes pulseBg {
  0%, 100% { transform: scale(1); box-shadow: 0 10px 30px rgba(82, 133, 140, 0.05); }
  50% { transform: scale(1.05); box-shadow: 0 15px 40px rgba(82, 133, 140, 0.15); }
}
@keyframes flipText {
  0%, 100% { transform: rotateY(0deg); }
  50% { transform: rotateY(180deg); color: var(--color-secondary); }
}"""
        },
        
        # 3. 閃光點與學習方式 (三個閃爍旋轉自轉的星星)
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
  width: 250px;
  height: 250px;
}
.star {
  position: absolute;
  color: var(--color-primary);
  font-weight: 900;
  user-select: none;
}
.star-1 { font-size: 5.5rem; top: 15%; left: 30%; animation: spinStar1 8s linear infinite; }
.star-2 { font-size: 3.5rem; top: 55%; left: 15%; color: var(--color-secondary); animation: spinStar2 6s linear infinite; }
.star-3 { font-size: 2.8rem; top: 50%; left: 65%; color: var(--color-accent); filter: brightness(0.9); animation: spinStar1 4s linear infinite; }
@keyframes spinStar1 {
  0% { transform: rotate(0deg) scale(1); opacity: 0.8; }
  50% { transform: rotate(180deg) scale(1.2); opacity: 1; }
  100% { transform: rotate(360deg) scale(1); opacity: 0.8; }
}
@keyframes spinStar2 {
  0% { transform: rotate(0deg) scale(1.1); opacity: 0.9; }
  50% { transform: rotate(-180deg) scale(0.9); opacity: 0.7; }
  100% { transform: rotate(-360deg) scale(1.1); opacity: 0.9; }
}"""
        },
        
        # 4. 工業時期 (工廠齒輪大圖 + 自轉齒輪)
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
.industrial-img { animation: machineVibrate 4s ease-in-out infinite !important; }
@keyframes machineVibrate {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-4px) scale(0.995); }
}
.gear { position: absolute; font-size: 4.5rem; color: rgba(82, 133, 140, 0.2); line-height: 1; user-select: none; }
.gear-large { top: 18%; left: 14%; font-size: 5.5rem; animation: spinClockwise 12s linear infinite; }
.gear-small { top: 36%; left: 24%; font-size: 3.8rem; animation: spinCounterClockwise 8s linear infinite; }
@keyframes spinClockwise { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes spinCounterClockwise { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }"""
        },
        
        # 5. 穩定標準效率同步 (純 CSS 規格化輸送帶動畫 - 去重)
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
  width: 300px;
  height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(82, 133, 140, 0.15);
  border-radius: 16px;
  overflow: hidden;
}
.conveyor-belt {
  position: relative;
  width: 260px;
  height: 6px;
  background: var(--color-secondary);
  border-radius: 3px;
  margin-top: 20px;
  display: flex;
  justify-content: space-around;
}
.conveyor-roller {
  font-size: 1.6rem;
  margin-top: 6px;
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
  top: 60px;
  width: 260px;
  height: 50px;
  overflow: hidden;
}
.conveyor-box {
  position: absolute;
  font-size: 2.2rem;
  bottom: 0;
  animation: moveBox 5s linear infinite;
  opacity: 0;
}
.box-1 { animation-delay: 0s; }
.box-2 { animation-delay: 1.66s; }
.box-3 { animation-delay: 3.33s; }

@keyframes moveBox {
  0% { left: -40px; opacity: 0; transform: scale(0.9); }
  10% { opacity: 1; transform: scale(1); }
  90% { opacity: 1; transform: scale(1); }
  100% { left: 260px; opacity: 0; transform: scale(0.9); }
}"""
        },
        
        # 6. 遠離工業時代 (一個漸漸淡出縮小的氣泡齒輪)
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
  width: 250px;
  height: 250px;
}
.fading-gear {
  font-size: 6.5rem;
  color: var(--color-secondary);
  animation: fadeOutGear 5s ease-in-out infinite;
}
@keyframes fadeOutGear {
  0% { transform: scale(1.1) rotate(0deg); opacity: 0.8; }
  50% { transform: scale(0.7) rotate(180deg); opacity: 0.15; filter: blur(2px); }
  100% { transform: scale(1.1) rotate(360deg); opacity: 0.8; }
}"""
        },
        
        # 7. 科技攀升與留在原地 (快速攀升的光點對比靜止點)
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
  gap: 50px;
  width: 320px;
  height: 250px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  padding: 30px;
  border: 1px solid rgba(82, 133, 140, 0.1);
}
.track-line {
  position: relative;
  width: 100%;
  height: 8px;
  background: rgba(46, 46, 46, 0.1);
  border-radius: 4px;
}
.track-label {
  position: absolute;
  top: -24px;
  left: 0;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text-main);
}
.moving-light {
  position: absolute;
  top: -4px;
  left: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-primary);
  box-shadow: 0 0 15px var(--color-primary);
  animation: travelFast 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
.static-dot {
  position: absolute;
  top: -4px;
  left: 20px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-secondary);
}
@keyframes travelFast {
  0% { left: 0%; opacity: 0.3; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { left: 90%; opacity: 0; }
}"""
        },
        
        # 8. 成功學攀爬梯 (不斷循環向上攀爬的階梯光點)
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
  width: 200px;
  height: 220px;
}
.ladder-step {
  position: absolute;
  width: 60px;
  height: 10px;
  background: var(--color-secondary);
  opacity: 0.5;
  border-radius: 4px;
}
.step-1 { bottom: 20px; left: 20px; }
.step-2 { bottom: 80px; left: 70px; }
.step-3 { bottom: 140px; left: 120px; }
.climbing-dot {
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--color-primary);
  box-shadow: 0 0 12px var(--color-primary);
  animation: climbSteps 4s ease-in-out infinite;
}
@keyframes climbSteps {
  0% { bottom: 35px; left: 40px; transform: scale(1); }
  30% { bottom: 95px; left: 90px; transform: scale(1.1); }
  60% { bottom: 155px; left: 140px; transform: scale(1); }
  85% { bottom: 155px; left: 140px; opacity: 1; }
  100% { bottom: 155px; left: 140px; opacity: 0; transform: scale(0.6); }
}"""
        },
        
        # 9. 神經多樣性 (大脑大圖)
        9: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/neurodiversity.png" class="scene-img neuro-img" alt="神經多樣性大腦">
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.neuro-img { animation: brainPulse 5s ease-in-out infinite !important; }
@keyframes brainPulse {
  0%, 100% { transform: scale(1) translateY(0); filter: drop-shadow(0 15px 30px rgba(82, 133, 140, 0.08)); }
  50% { transform: scale(1.025) translateY(-5px); filter: drop-shadow(0 20px 45px rgba(82, 133, 140, 0.22)); }
}"""
        },
        
        # 10. 吸收方式不同 (三個不同自轉速度和大小的彩色同心圓環)
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
  width: 250px;
  height: 250px;
}
.ring {
  position: absolute;
  border-radius: 50%;
  border: 4px dashed transparent;
}
.ring-outer {
  width: 220px;
  height: 220px;
  border-color: var(--color-primary);
  animation: spinRingCW 15s linear infinite;
}
.ring-middle {
  width: 150px;
  height: 150px;
  border-color: var(--color-secondary);
  animation: spinRingCCW 10s linear infinite;
}
.ring-inner {
  width: 80px;
  height: 80px;
  border-color: var(--color-accent);
  filter: brightness(0.85);
  animation: spinRingCW 6s linear infinite;
}
@keyframes spinRingCW { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes spinRingCCW { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }"""
        },
        
        # 11. 1對30痛點 (疲憊老師大圖)
        11: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/one_vs_thirty.png" class="scene-img school-img" alt="一位老師面對三十個學生">
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.school-img { animation: schoolFloat 6s ease-in-out infinite !important; }
@keyframes schoolFloat {
  0%, 100% { transform: translateY(0); filter: drop-shadow(0 15px 30px rgba(46, 46, 46, 0.08)); }
  50% { transform: translateY(-6px); filter: drop-shadow(0 20px 40px rgba(46, 46, 46, 0.18)); }
}"""
        },
        
        # 12. 帶上學習軌道 (一個小球在水平發光軌道上來回滑動)
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
  width: 280px;
  height: 220px;
}
.rail-line {
  position: relative;
  width: 100%;
  height: 6px;
  background: rgba(46, 46, 46, 0.1);
  border-radius: 3px;
}
.rail-car {
  position: absolute;
  top: -8px;
  left: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--color-primary);
  box-shadow: 0 4px 10px rgba(82, 133, 140, 0.3);
  animation: slideOnRail 5s ease-in-out infinite;
}
@keyframes slideOnRail {
  0%, 100% { left: 0%; }
  50% { left: 90%; }
}"""
        },
        
        # 13. 顧進度、顧考試 (三個小球拋接手忙腳亂)
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
  width: 250px;
  height: 220px;
}
.juggling-ball {
  position: absolute;
  width: 65px;
  height: 65px;
  border-radius: 50%;
  color: #FFFFFF;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 15px rgba(0,0,0,0.06);
}
.ball-a { background: var(--color-primary); animation: juggleA 4s ease-in-out infinite; }
.ball-b { background: var(--color-secondary); animation: juggleB 4s ease-in-out infinite; }
.ball-c { background: var(--color-accent); color: var(--color-text-main); border: 1px solid rgba(82, 133, 140, 0.15); animation: juggleC 4s ease-in-out infinite; }
@keyframes juggleA {
  0%, 100% { bottom: 10px; left: 20px; }
  33% { bottom: 140px; left: 90px; }
  66% { bottom: 10px; left: 160px; }
}
@keyframes juggleB {
  0%, 100% { bottom: 10px; left: 160px; }
  33% { bottom: 10px; left: 20px; }
  66% { bottom: 140px; left: 90px; }
}
@keyframes juggleC {
  0%, 100% { bottom: 140px; left: 90px; }
  33% { bottom: 10px; left: 160px; }
  66% { bottom: 10px; left: 20px; }
}"""
        },
        
        # 14. 量身規劃這太難了 (兩塊拆開拼不上的拼圖)
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
  width: 250px;
  height: 220px;
}
.puzzle-part {
  position: absolute;
  font-size: 5rem;
  transition: all 0.3s ease;
  user-select: none;
}
.part-left {
  top: 40px;
  left: 20px;
  animation: floatPuzzleLeft 6s ease-in-out infinite;
}
.part-right {
  top: 60px;
  right: 20px;
  transform: rotate(180deg);
  filter: hue-rotate(50deg);
  animation: floatPuzzleRight 6s ease-in-out infinite;
}
@keyframes floatPuzzleLeft {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(18px, -8px) rotate(5deg); }
}
@keyframes floatPuzzleRight {
  0%, 100% { transform: translate(0, 0) rotate(180deg); }
  50% { transform: translate(-18px, 8px) rotate(175deg); }
}"""
        },
        
        # 15. 自我決定論卡片選單 (卡片互動，已在 HTML 中覆蓋，只需定義 CSS)
        15: {
            'type': 'text', # 自帶 HTML 結構，因此標記為 text 避免被 overwrite html
            'css': "" # 已經在 html 修改時定義好 css 了
        },
        
        # 16. 自主感 (大圖 + 返回按鈕)
        16: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/autonomy.png" class="scene-img autonomy-img" alt="自主感">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 20px; right: 20px; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.autonomy-img { animation: autonomyFloat 6s ease-in-out infinite !important; }
@keyframes autonomyFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); filter: drop-shadow(0 15px 30px rgba(82, 133, 140, 0.08)); }
  50% { transform: translateY(-7px) rotate(1.5deg); filter: drop-shadow(0 20px 40px rgba(82, 133, 140, 0.22)); }
}
.back-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  padding: 10px 22px;
  border-radius: 25px;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(82, 133, 140, 0.25);
  transition: all 0.2s ease;
}
.back-btn:hover {
  background: var(--color-secondary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(82, 133, 140, 0.35);
}"""
        },
        
        # 17. 勝任感 (大圖 + 返回按鈕)
        17: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/competence.png" class="scene-img competence-img" alt="勝任感">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 20px; right: 20px; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.competence-img { animation: competenceFloat 6s ease-in-out infinite !important; }
@keyframes competenceFloat {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 15px 30px rgba(82, 133, 140, 0.08)); }
  50% { transform: translateY(-8px) scale(1.02); filter: drop-shadow(0 22px 40px rgba(82, 133, 140, 0.22)); }
}
.back-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  padding: 10px 22px;
  border-radius: 25px;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(82, 133, 140, 0.25);
  transition: all 0.2s ease;
}
.back-btn:hover {
  background: var(--color-secondary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(82, 133, 140, 0.35);
}"""
        },
        
        # 18. 歸屬感 (大圖 + 返回按鈕)
        18: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="溫暖呵護手捧樹苗">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 20px; right: 20px; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.guide-img { animation: seedlingGrow 6s ease-in-out infinite !important; }
@keyframes seedlingGrow {
  0%, 100% { transform: translateY(0) scale(1); filter: brightness(1) drop-shadow(0 15px 25px rgba(192, 169, 145, 0.15)); }
  50% { transform: translateY(-5px) scale(1.01); filter: brightness(1.06) drop-shadow(0 22px 35px rgba(192, 169, 145, 0.25)); }
}
.back-btn {
  background: var(--color-primary);
  color: #FFFFFF;
  border: none;
  padding: 10px 22px;
  border-radius: 25px;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(82, 133, 140, 0.25);
  transition: all 0.2s ease;
}
.back-btn:hover {
  background: var(--color-secondary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(82, 133, 140, 0.35);
}"""
        },
        
        # 19. AI 貼合節奏 (機器人大圖)
        19: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/ai_mentor.png" class="scene-img ai-img" alt="AI陪伴學習">
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.ai-img { animation: aiFloat 5.5s ease-in-out infinite !important; }
@keyframes aiFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); filter: drop-shadow(0 15px 30px rgba(82, 133, 140, 0.06)); }
  50% { transform: translateY(-8px) rotate(0.8deg); filter: drop-shadow(0 22px 40px rgba(82, 133, 140, 0.18)); }
}"""
        },
        
        # 20. 多元選擇 (點擊卡片彈出說明互動 - 增加互動)
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
  gap: 16px;
  width: 320px;
  height: 250px;
}
.media-card {
  position: relative;
  flex: 1;
  min-width: 80px;
  height: 120px;
  background: rgba(255, 255, 255, 0.6);
  border: 1.5px solid rgba(82, 133, 140, 0.15);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px 6px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0,0,0,0.03);
  transition: all 0.22s ease;
  user-select: none;
}
.media-card:hover {
  transform: translateY(-8px) scale(1.08);
  border-color: var(--color-primary);
  background: #FFFFFF;
  box-shadow: 0 10px 20px rgba(82, 133, 140, 0.15);
}
.media-icon { font-size: 2.2rem; margin-bottom: 6px; }
.media-card span { font-size: 0.85rem; font-weight: 700; color: var(--color-text-main); }

.click-badge {
  position: absolute;
  bottom: -8px;
  background: var(--color-highlight-accent);
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(220, 168, 66, 0.3);
}

.media-tip-popup {
  width: 100%;
  background: var(--color-secondary);
  color: #FFFFFF;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.8rem;
  line-height: 1.4;
  padding: 10px 14px;
  border-radius: 8px;
  box-shadow: 0 6px 15px rgba(44, 61, 77, 0.15);
  margin-top: 12px;
  text-align: left;
}"""
        },
        
        # 21. 選擇權與建立自主感 (模擬小手點選按鈕 CSS 動態)
        21: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="click-demo-container">
          <div class="click-btn btn-a">語法探索</div>
          <div class="click-btn btn-b">實作模擬</div>
          <div class="click-hand">👆</div>
        </div>
      </div>""",
            'css': """
.click-demo-container {
  position: relative;
  width: 250px;
  height: 220px;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(82, 133, 140, 0.1);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}
.click-btn {
  padding: 8px 24px;
  background: #FFFFFF;
  border: 2px solid rgba(82, 133, 140, 0.15);
  border-radius: 20px;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-main);
  box-shadow: 0 3px 6px rgba(0,0,0,0.02);
  transition: all 0.2s ease;
}
.click-hand {
  position: absolute;
  font-size: 2.8rem;
  bottom: 10px;
  right: 40px;
  user-select: none;
  animation: simulateClick 4s ease-in-out infinite;
}
@keyframes simulateClick {
  0%, 100% { transform: translate(0, 0) scale(1); }
  40% { transform: translate(-30px, -70px) scale(1); }
  50% { transform: translate(-30px, -70px) scale(0.85); } /* 點按下去的縮放 */
  60% { transform: translate(-30px, -70px) scale(1); }
}
/* 配合手勢，在第50%秒高亮按鈕B */
.btn-b {
  animation: btnHighlight 4s linear infinite;
}
@keyframes btnHighlight {
  0%, 45%, 70%, 100% { border-color: rgba(82, 133, 140, 0.15); background: #FFFFFF; }
  50%, 65% { border-color: var(--color-primary); background: rgba(82, 133, 140, 0.08); box-shadow: 0 0 10px rgba(82, 133, 140, 0.2); }
}"""
        },
        
        # 22. AI Patience 講100遍 (已經在 HTML 中覆蓋互動邏輯，只需定義 CSS)
        22: {
            'type': 'text',
            'css': ""
        },
        
        # 23. 跟不上別人 (跑道上一球落後)
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
  width: 280px;
  height: 200px;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(82, 133, 140, 0.1);
  border-radius: 12px;
}
.runner {
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 50%;
}
.runner-fast-1 { top: 40px; background: var(--color-secondary); animation: runFast1 5s linear infinite; }
.runner-fast-2 { top: 90px; background: var(--color-accent); filter: brightness(0.9); animation: runFast2 5s linear infinite; }
.runner-slow { top: 140px; background: var(--color-primary); animation: runSlow 5s linear infinite; }
@keyframes runFast1 { 0% { left: 10%; } 100% { left: 85%; } }
@keyframes runFast2 { 0% { left: 10%; } 100% { left: 78%; } }
@keyframes runSlow { 0% { left: 10%; } 100% { left: 45%; } }"""
        },
        
        # 24. 隨時想問就問 (閃爍的對話氣泡)
        24: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="chat-box-wrapper">
          <div class="chat-bubble bubble-left">？</div>
          <div class="chat-bubble bubble-right">沒問題，我們再說一遍！💡</div>
        </div>
      </div>""",
            'css': """
.chat-box-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 300px;
  height: 220px;
  justify-content: center;
}
.chat-bubble {
  padding: 12px 18px;
  border-radius: 18px;
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(0,0,0,0.03);
}
.bubble-left {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.7);
  border: 1.5px solid rgba(82, 133, 140, 0.15);
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
        
        # 25. 給予充足時間學得會 (慢慢流逝轉動指針的時鐘)
        25: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="clock-wrapper">
          <div class="clock-face">
            <div class="clock-hand-hour"></div>
            <div class="clock-hand-minute"></div>
          </div>
        </div>
      </div>""",
            'css': """
.clock-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 250px;
  height: 220px;
}
.clock-face {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  border: 4px solid var(--color-primary);
}
.clock-hand-hour, .clock-hand-minute {
  position: absolute;
  background: var(--color-text-main);
  border-radius: 2px;
  transform-origin: bottom center;
  bottom: 50%;
  left: calc(50% - 2px);
}
.clock-hand-hour {
  width: 4px;
  height: 35px;
  animation: spinHand 20s linear infinite;
}
.clock-hand-minute {
  width: 3px;
  height: 55px;
  background: var(--color-secondary);
  animation: spinHand 4s linear infinite;
}
@keyframes spinHand { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }"""
        },
        
        # 26. 建立勝任感 (能量條充能動態)
        26: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="progress-box">
          <span class="progress-title">勝任感充能</span>
          <div class="progress-bg">
            <div class="progress-fill"></div>
          </div>
          <span class="percent-label">99%</span>
        </div>
      </div>""",
            'css': """
.progress-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  width: 280px;
  height: 200px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  border: 1px solid rgba(82, 133, 140, 0.15);
  padding: 24px;
}
.progress-title {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-main);
}
.progress-bg {
  width: 100%;
  height: 16px;
  background: rgba(46, 46, 46, 0.08);
  border-radius: 8px;
  overflow: hidden;
}
.progress-fill {
  width: 0%;
  height: 100%;
  background: var(--color-primary);
  border-radius: 8px;
  animation: fillProgress 4s ease-in-out infinite;
}
.percent-label {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.1rem;
  font-weight: 900;
  color: var(--color-primary);
  animation: countUp 4s linear infinite;
}
@keyframes fillProgress { 0% { width: 0%; } 80%, 100% { width: 99%; } }
@keyframes countUp {
  0% { content: '0%'; opacity: 0.8; }
  80%, 100% { content: '99%'; opacity: 1; }
}"""
        },
        
        # 27. 家長老師有餘裕 (放鬆浮空的熱氣球)
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
  width: 250px;
  height: 250px;
}
.hot-balloon {
  position: absolute;
  font-size: 5.5rem;
  top: 30%;
  left: 35%;
  user-select: none;
  animation: balloonFloat 6s ease-in-out infinite;
}
.cloud-dec {
  position: absolute;
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.85);
  opacity: 0.7;
}
.cloud-1 { top: 15%; left: 10%; animation: cloudMove1 12s linear infinite; }
.cloud-2 { top: 55%; right: 10%; animation: cloudMove2 9s linear infinite; }
@keyframes balloonFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-16px) rotate(3deg); }
}
@keyframes cloudMove1 {
  0% { transform: translateX(0); }
  50% { transform: translateX(15px); }
  100% { transform: translateX(0); }
}
@keyframes cloudMove2 {
  0% { transform: translateX(0); }
  50% { transform: translateX(-12px); }
  100% { transform: translateX(0); }
}"""
        },
        
        # 28. 走進內心 (心形呼吸放大)
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
  width: 250px;
  height: 250px;
}
.heart-shape {
  font-size: 6.5rem;
  animation: heartBeat 4s ease-in-out infinite;
}
@keyframes heartBeat {
  0%, 100% { transform: scale(1); opacity: 0.85; filter: drop-shadow(0 10px 20px rgba(139, 122, 107, 0.1)); }
  50% { transform: scale(1.18); opacity: 1; filter: drop-shadow(0 15px 35px rgba(139, 122, 107, 0.25)); }
}"""
        },
        
        # 29. 歸屬感建立 (純 CSS 溫馨避風港動畫 - 去重)
        29: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-1s">
        <div class="haven-container">
          <div class="haven-house">🏡</div>
          <div class="haven-heart haven-heart-1">🧡</div>
          <div class="haven-heart haven-heart-2">✨</div>
          <div class="haven-heart haven-heart-3">💖</div>
        </div>
      </div>""",
            'css': """
.haven-container {
  position: relative;
  width: 250px;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.haven-house {
  font-size: 6.5rem;
  animation: housePulse 4s ease-in-out infinite;
  filter: drop-shadow(0 10px 25px rgba(82, 133, 140, 0.15));
}
@keyframes housePulse {
  0%, 100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.06); filter: brightness(1.08) drop-shadow(0 15px 35px rgba(82, 133, 140, 0.25)); }
}
.haven-heart {
  position: absolute;
  font-size: 1.8rem;
  opacity: 0;
  user-select: none;
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
  0% { transform: translateY(20px) scale(0.6); opacity: 0; }
  30% { opacity: 0.8; }
  90% { opacity: 0.8; }
  100% { transform: translateY(-50px) scale(1.1) rotate(-15deg); opacity: 0; }
}
@keyframes floatUpHeart2 {
  0% { transform: translateY(30px) scale(0.5); opacity: 0; }
  40% { opacity: 0.9; }
  90% { opacity: 0.9; }
  100% { transform: translateY(-60px) scale(1) rotate(15deg); opacity: 0; }
}
@keyframes floatUpHeart3 {
  0% { transform: translateY(15px) scale(0.7); opacity: 0; }
  30% { opacity: 0.95; }
  90% { opacity: 0.95; }
  100% { transform: translateY(-45px) scale(1.2) rotate(10deg); opacity: 0; }
}"""
        },
        
        # 30. 缺了動力電池充電 (點擊電池充電切換 - 增加互動)
        30: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s" onclick="toggleBatteryCharge()">
        <div class="battery-wrapper" style="cursor: pointer;">
          <div class="battery-body">
            <div class="battery-fill" id="bat-fill"></div>
          </div>
          <div class="battery-tip"></div>
          <span class="charge-label" id="bat-label">動力不足</span>
          <div class="click-badge" style="bottom: 0px;">點擊充電 ⚡</div>
        </div>
        <script>
          let isCharged = false;
          function toggleBatteryCharge() {
            const fill = document.getElementById('bat-fill');
            const label = document.getElementById('bat-label');
            
            fill.style.animation = 'none';
            label.style.animation = 'none';
            void fill.offsetWidth;
            
            isCharged = !isCharged;
            if (isCharged) {
              fill.style.width = '100%';
              fill.style.background = 'var(--color-primary)';
              fill.style.boxShadow = '0 0 12px var(--color-primary)';
              label.textContent = '動力充滿！';
              label.style.color = 'var(--color-primary)';
            } else {
              fill.style.width = '0%';
              fill.style.background = '#E26D5C';
              fill.style.boxShadow = 'none';
              label.textContent = '動力不足';
              label.style.color = '#E26D5C';
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
  width: 250px;
  height: 220px;
  gap: 20px;
}
.battery-body {
  position: relative;
  width: 140px;
  height: 70px;
  border: 4px solid var(--color-secondary);
  border-radius: 8px;
  padding: 4px;
}
.battery-tip {
  position: absolute;
  top: calc(50% - 18px);
  right: 43px;
  width: 8px;
  height: 20px;
  background: var(--color-secondary);
  border-radius: 0 4px 4px 0;
}
.battery-fill {
  width: 0%;
  height: 100%;
  background: var(--color-secondary);
  border-radius: 4px;
  animation: chargeBattery 4s cubic-bezier(0.12, 0, 0.39, 0) infinite;
  transition: all 0.3s ease;
}
.charge-label {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-main);
  animation: changeLabel 4s step-end infinite;
  transition: all 0.3s ease;
}
.click-badge {
  position: absolute;
  bottom: 0px;
  background: var(--color-highlight-accent);
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 900;
  padding: 2px 6px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(220, 168, 66, 0.3);
}
@keyframes chargeBattery {
  0% { width: 0%; background: #E26D5C; }
  35% { width: 40%; background: #E26D5C; }
  70%, 100% { width: 100%; background: var(--color-primary); }
}
@keyframes changeLabel {
  0%, 69% { content: '動力不足'; color: #E26D5C; }
  70%, 100% { content: '動力充滿！'; color: var(--color-primary); }
}"""
        },
        
        # 31. 願意學 (大圖)
        31: {
            'type': 'split',
            'visual': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/willing_to_learn.png" class="scene-img willing-img" alt="願意學">
        </div>
      </div>""",
            'css': """
.image-wrapper { position: relative; display: inline-block; }
.willing-img { animation: sunRise 7s ease-in-out infinite !important; }
@keyframes sunRise {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 15px 30px rgba(192, 169, 145, 0.1)); }
  50% { transform: translateY(-8px) scale(1.015); filter: drop-shadow(0 25px 45px rgba(192, 169, 145, 0.22)); }
}"""
        }
    }

    # 執行批次更新
    for scene_num in range(1, 32):
        if scene_num not in scene_rules:
            # 剩餘的純文字場景（但我們已經不需要了，因為我們重新分配使得每一幕都有插畫/CSS圖形了！）
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
            # 我們保留它們的 HTML 結構，不對 HTML 進行重寫，只更新 CSS 樣式
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
  font-size: 2.3rem;
  font-weight: 700;
  color: var(--color-text-main);
  margin: 16px 0;
  letter-spacing: 0.05em;
  line-height: 1.5;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}}
{rule['css']}"""
            
            # 特別處理最後一幕
            if scene_num == 31:
                css_template += """
.text-side .animate-line:nth-child(2) {
  font-family: "Noto Serif TC", serif;
  font-size: 2.8rem;
  color: var(--color-primary) !important;
  font-weight: 900;
  margin-top: 24px;
}
.text-side .animate-line:nth-child(3) {
  font-size: 1.5rem;
  color: var(--color-secondary) !important;
  font-weight: 700;
}
"""
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_template)
            print(f"CSS Scene {scene_num} styles updated.")
            
    print("\n恭喜！31 幕畫面與 CSS 圖文相符全域重組完畢！")

if __name__ == '__main__':
    rebuild()

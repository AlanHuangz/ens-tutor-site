# edit_super_rebuild.py
import os

target_path = r"C:\Users\wkoyo\Documents\家教網站\animation-dev\scratch\super_rebuild.py"

with open(target_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替換舊的綠色色碼
# 77, 114, 80 -> 82, 133, 140
# 99, 134, 102 -> 82, 133, 140
# #3B5A3E -> #3C6267
# #507053 -> #3C6267
content = content.replace("77, 114, 80", "82, 133, 140")
content = content.replace("99, 134, 102", "82, 133, 140")
content = content.replace("#3B5A3E", "#3C6267")
content = content.replace("#507053", "#3C6267")

# 2. 替換第 5 幕 (去重：輸送帶規格化包裝盒滑動動畫)
old_scene5 = """        # 5. 穩定標準效率同步 (工廠齒輪大圖)
        5: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/industrial_education.png" class="scene-img industrial-img" alt="工業時期教育">
          <div class="gear gear-large">⚙️</div>
          <div class="gear gear-small">⚙️</div>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
@keyframes spinCounterClockwise { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }\"\"\"
        },"""

new_scene5 = """        # 5. 穩定標準效率同步 (純 CSS 規格化輸送帶動畫 - 去重)
        5: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-1s">
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
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene5, new_scene5)

# 3. 替換第 16 幕 (添加返回按鈕)
old_scene16 = """        # 16. 自主感 (大圖 + 返回按鈕)
        16: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/autonomy.png" class="scene-img autonomy-img" alt="自主感">
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
  background: #3C6267;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(82, 133, 140, 0.35);
}\"\"\"
        },"""

new_scene16 = """        # 16. 自主感 (大圖 + 返回按鈕)
        16: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/autonomy.png" class="scene-img autonomy-img" alt="自主感">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 20px; right: 20px; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene16, new_scene16)

# 4. 替換第 17 幕 (添加返回按鈕)
old_scene17 = """        # 17. 勝任感 (大圖 + 返回按鈕)
        17: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/competence.png" class="scene-img competence-img" alt="勝任感">
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
  background: #3C6267;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(82, 133, 140, 0.35);
}\"\"\"
        },"""

new_scene17 = """        # 17. 勝任感 (大圖 + 返回按鈕)
        17: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/competence.png" class="scene-img competence-img" alt="勝任感">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 20px; right: 20px; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene17, new_scene17)

# 5. 替換第 18 幕 (添加返回按鈕)
old_scene18 = """        # 18. 歸屬感 (大圖 + 返回按鈕)
        18: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="溫暖呵護手捧樹苗">
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
  background: #3C6267;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(82, 133, 140, 0.35);
}\"\"\"
        },"""

new_scene18 = """        # 18. 歸屬感 (大圖 + 返回按鈕)
        18: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="溫暖呵護手捧樹苗">
        </div>
        <div id="back-to-menu-container" style="display: none; position: absolute; bottom: 20px; right: 20px; z-index: 100;">
          <button class="back-btn" onclick="backToMenu()">返回選單 ↩</button>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene18, new_scene18)

# 6. 替換第 20 幕 (增加卡片點擊切換與彈出小視窗展示優勢)
old_scene20 = """        # 20. 多元選擇 (滑鼠懸停縮放的圖示 🎨 🎬 🎵)
        20: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="media-choices-wrapper">
          <div class="media-card card-visual">
            <div class="media-icon">🎨</div>
            <span>圖像</span>
          </div>
          <div class="media-card card-video">
            <div class="media-icon">🎬</div>
            <span>影像</span>
          </div>
          <div class="media-card card-audio">
            <div class="media-icon">🎵</div>
            <span>聽覺</span>
          </div>
        </div>
      </div>\"\"\",
            'css': \"\"\"
.media-choices-wrapper {
  display: flex;
  justify-content: center;
  gap: 16px;
  width: 320px;
  height: 220px;
}
.media-card {
  flex: 1;
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
.media-card span { font-size: 0.85rem; font-weight: 700; color: var(--color-text-main); }\"\"\"
        },"""

new_scene20 = """        # 20. 多元選擇 (點擊卡片彈出說明互動 - 增加互動)
        20: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
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
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene20, new_scene20)

# 7. 替換第 26 幕 (能量條增加手動充能微互動)
old_scene26 = """        # 26. 建立勝任感 (能量條充能動態)
        26: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-1s">
        <div class="progress-box">
          <span class="progress-title">勝任感充能</span>
          <div class="progress-bg">
            <div class="progress-fill"></div>
          </div>
          <span class="percent-label">99%</span>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
  background: rgba(44, 61, 77, 0.08);
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
}\"\"\"
        },"""

new_scene26 = """        # 26. 建立勝任感 (能量條手動充能 - 增加互動)
        26: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-1s">
        <div class="progress-box">
          <span class="progress-title" id="charge-title">勝任感充能</span>
          <div class="progress-bg">
            <div class="progress-fill" id="bar-fill"></div>
          </div>
          <div style="display: flex; align-items: center; gap: 10px; width: 100%; justify-content: space-between;">
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
            bar.style.boxShadow = '0 0 15px var(--color-highlight-accent)';
            
            percent.textContent = '100%';
            percent.style.color = 'var(--color-highlight-accent)';
            title.innerHTML = '勝任感滿足！🎉';
            title.style.color = 'var(--color-highlight-accent)';
          }
        </script>
      </div>\"\"\",
            'css': \"\"\"
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
  transition: all 0.3s ease;
}
.progress-bg {
  width: 100%;
  height: 16px;
  background: rgba(44, 61, 77, 0.08);
  border-radius: 8px;
  overflow: hidden;
}
.progress-fill {
  width: 0%;
  height: 100%;
  background: var(--color-primary);
  border-radius: 8px;
  animation: fillProgress 4s ease-in-out infinite;
  transition: all 0.3s ease;
}
.percent-label {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 1.1rem;
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
  font-size: 0.8rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(82, 133, 140, 0.2);
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
}\"\"\"
        },"""

content = content.replace(old_scene26, new_scene26)

# 8. 替換第 29 幕 (去重：純 CSS 避風港與呼吸愛心星空動畫)
old_scene29 = """        # 29. 歸屬感建立 (避風港小房子呼吸)
        29: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="歸屬感的建立">
        </div>
      </div>\"\"\",
            'css': \"\"\"
.image-wrapper { position: relative; display: inline-block; }
.guide-img { animation: seedlingGrow 6s ease-in-out infinite !important; }
@keyframes seedlingGrow {
  0%, 100% { transform: translateY(0) scale(1); filter: brightness(1) drop-shadow(0 15px 25px rgba(192, 169, 145, 0.15)); }
  50% { transform: translateY(-5px) scale(1.01); filter: brightness(1.06) drop-shadow(0 22px 35px rgba(192, 169, 145, 0.25)); }
}\"\"\"
        },"""

new_scene29 = """        # 29. 歸屬感建立 (純 CSS 溫馨避風港動畫 - 去重)
        29: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-1s">
        <div class="haven-container">
          <div class="haven-house">🏡</div>
          <div class="haven-heart haven-heart-1">🧡</div>
          <div class="haven-heart haven-heart-2">✨</div>
          <div class="haven-heart haven-heart-3">💖</div>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene29, new_scene29)

# 9. 替換第 30 幕 (增加電池充電切換互動)
old_scene30 = """        # 30. 缺了動力電池充電 (空電池 ➔ 充滿發光綠色電池)
        30: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s">
        <div class="battery-wrapper">
          <div class="battery-body">
            <div class="battery-fill"></div>
          </div>
          <div class="battery-tip"></div>
          <span class="charge-label">動力不足</span>
        </div>
      </div>\"\"\",
            'css': \"\"\"
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
}
.charge-label {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--color-text-main);
  animation: changeLabel 4s step-end infinite;
}
@keyframes chargeBattery {
  0% { width: 0%; background: #E26D5C; }
  35% { width: 40%; background: #E26D5C; }
  70%, 100% { width: 100%; background: var(--color-primary); }
}
@keyframes changeLabel {
  0%, 69% { content: '動力不足'; color: var(--color-secondary); }
  70%, 100% { content: '動力充滿！'; color: var(--color-primary); }
}\"\"\"
        },"""

new_scene30 = """        # 30. 缺了動力電池充電 (點擊電池充電切換 - 增加互動)
        30: {
            'type': 'split',
            'visual': \"\"\"      <div class="visual-side fade-in delay-2s" onclick="toggleBatteryCharge()">
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
      </div>\"\"\",
            'css': \"\"\"
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
}\"\"\"
        },"""

content = content.replace(old_scene30, new_scene30)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("super_rebuild.py successfully updated with deduplication, return buttons, and micro-interactions!")

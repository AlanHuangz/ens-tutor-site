# align_images_and_text.py
import os
import re

def main():
    scenes_dir = r"C:\Users\wkoyo\Documents\家教網站\animation-dev\scenes"
    
    # 精確圖文相符對照表
    # 僅在主題強烈符合的幕才顯示圖片，其餘幕回歸純文字，使節奏有張有弛，避免硬湊圖文不符的畫面。
    split_scenes = {
        # 焦慮與一代不如一代痛點
        1: {
            'img': '../assets/parent_anxiety.png',
            'alt': '家長懊惱與焦慮',
            'theme': 'A',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/parent_anxiety.png" class="scene-img anxiety-img" alt="家長懊惱與焦慮">
          <div class="bubble bubble-1">？</div>
          <div class="bubble bubble-2">？</div>
          <div class="bubble bubble-3">…</div>
        </div>
      </div>"""
        },
        # 工業化教育
        4: {
            'img': '../assets/industrial_education.png',
            'alt': '工業時期教育',
            'theme': 'B',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/industrial_education.png" class="scene-img industrial-img" alt="工業時期教育">
          <div class="gear gear-large">⚙️</div>
          <div class="gear gear-small">⚙️</div>
        </div>
      </div>"""
        },
        5: {
            'img': '../assets/industrial_education.png',
            'alt': '工業教育特徵',
            'theme': 'B',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/industrial_education.png" class="scene-img industrial-img" alt="工業時期教育">
          <div class="gear gear-large">⚙️</div>
          <div class="gear gear-small">⚙️</div>
        </div>
      </div>"""
        },
        # 腦科學與神經多樣性
        9: {
            'img': '../assets/neurodiversity.png',
            'alt': '神經多樣性大腦',
            'theme': 'C',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/neurodiversity.png" class="scene-img neuro-img" alt="神經多樣性大腦">
        </div>
      </div>"""
        },
        10: {
            'img': '../assets/neurodiversity.png',
            'alt': '多樣的學習方式',
            'theme': 'C',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/neurodiversity.png" class="scene-img neuro-img" alt="神經多樣性大腦">
        </div>
      </div>"""
        },
        # 歸屬感、溫暖接住不安
        18: {
            'img': '../assets/supportive_guide.png',
            'alt': '溫暖呵護手捧樹苗',
            'theme': 'D',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="溫暖呵護手捧樹苗">
        </div>
      </div>"""
        },
        # AI 貼合節奏、多元選擇
        19: {
            'img': '../assets/ai_mentor.png',
            'alt': 'AI陪伴學習',
            'theme': 'E',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/ai_mentor.png" class="scene-img ai-img" alt="AI陪伴學習">
        </div>
      </div>"""
        },
        20: {
            'img': '../assets/ai_mentor.png',
            'alt': '多元圖像影像輸入',
            'theme': 'E',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/ai_mentor.png" class="scene-img ai-img" alt="AI陪伴學習">
        </div>
      </div>"""
        },
        22: {
            'img': '../assets/ai_mentor.png',
            'alt': 'AI耐心拆解100遍',
            'theme': 'E',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/ai_mentor.png" class="scene-img ai-img" alt="AI陪伴學習">
        </div>
      </div>"""
        },
        # 孩子最需要的歸屬感建立
        29: {
            'img': '../assets/supportive_guide.png',
            'alt': '歸屬感的建立',
            'theme': 'D',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="溫暖呵護手捧樹苗">
        </div>
      </div>"""
        },
        # 重新找回願意學
        31: {
            'img': '../assets/willing_to_learn.png',
            'alt': '孩子自信奔向未來',
            'theme': 'F',
            'html': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/willing_to_learn.png" class="scene-img willing-img" alt="孩子自信奔向未來">
        </div>
      </div>"""
        }
    }

    # CSS 特效定義
    css_effects = {
        'A': """
/* 焦慮懊惱情境動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}
.anxiety-img {
  animation: swayAnxiety 6s ease-in-out infinite !important;
}
@keyframes swayAnxiety {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); }
  50% { transform: translateY(-8px) rotate(-1.5deg) scale(1.015); }
}
.bubble {
  position: absolute;
  background: rgba(99, 134, 102, 0.08);
  color: var(--color-primary);
  border: 1.5px solid rgba(99, 134, 102, 0.25);
  font-family: "Noto Sans TC", sans-serif;
  font-weight: 900;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(99, 134, 102, 0.05);
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
}""",
        'B': """
/* 工業時代情境動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}
.industrial-img {
  animation: machineVibrate 4s ease-in-out infinite !important;
}
@keyframes machineVibrate {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-4px) scale(0.995); }
}
.gear {
  position: absolute;
  font-size: 4.5rem;
  color: rgba(99, 134, 102, 0.2);
  line-height: 1;
  user-select: none;
}
.gear-large { top: 18%; left: 14%; font-size: 5.5rem; animation: spinClockwise 12s linear infinite; }
.gear-small { top: 36%; left: 24%; font-size: 3.8rem; animation: spinCounterClockwise 8s linear infinite; }
@keyframes spinClockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
@keyframes spinCounterClockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(-360deg); }
}""",
        'C': """
/* 大腦神經多樣性動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}
.neuro-img {
  animation: brainPulse 5s ease-in-out infinite !important;
}
@keyframes brainPulse {
  0%, 100% { transform: scale(1) translateY(0); filter: drop-shadow(0 15px 30px rgba(99, 134, 102, 0.08)); }
  50% { transform: scale(1.02) translateY(-4px); filter: drop-shadow(0 20px 40px rgba(99, 134, 102, 0.2)); }
}""",
        'D': """
/* 守護陪伴發光小樹苗動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}
.guide-img {
  animation: seedlingGrow 6s ease-in-out infinite !important;
}
@keyframes seedlingGrow {
  0%, 100% { transform: translateY(0) scale(1); filter: brightness(1) drop-shadow(0 15px 25px rgba(192, 169, 145, 0.15)); }
  50% { transform: translateY(-5px) scale(1.01); filter: brightness(1.06) drop-shadow(0 22px 35px rgba(192, 169, 145, 0.25)); }
}""",
        'E': """
/* AI 機器人互動指導動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}
.ai-img {
  animation: aiFloat 5.5s ease-in-out infinite !important;
}
@keyframes aiFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); filter: drop-shadow(0 15px 30px rgba(99, 134, 102, 0.06)); }
  50% { transform: translateY(-7px) rotate(0.6deg); filter: drop-shadow(0 22px 40px rgba(99, 134, 102, 0.18)); }
}""",
        'F': """
/* 願意學自信孩童朝向陽光動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}
.willing-img {
  animation: sunRise 7s ease-in-out infinite !important;
}
@keyframes sunRise {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 15px 30px rgba(192, 169, 145, 0.1)); }
  50% { transform: translateY(-8px) scale(1.015); filter: drop-shadow(0 25px 45px rgba(192, 169, 145, 0.22)); }
}"""
    }

    # 處理 1 到 31 幕
    for scene_num in range(1, 32):
        html_file = os.path.join(scenes_dir, f"scene{scene_num}.html")
        css_file = os.path.join(scenes_dir, f"scene{scene_num}.css")
        
        if not os.path.exists(html_file) or not os.path.exists(css_file):
            print(f"Skipping Scene {scene_num}: Files not found.")
            continue

        # 讀取 HTML 內容
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 提取 p 標籤
        p_matches = re.findall(r'(<p[^>]*class="animate-line[^>]*">[\s\S]*?</p>)', html_content)
        p_tags_cleaned = "\n        ".join([p.strip() for p in p_matches])
        
        # 決定是左右分割還是純文字排版
        is_split = scene_num in split_scenes

        # 1. 重構 HTML 內容
        if is_split:
            visual_html = split_scenes[scene_num]['html']
            inner_container = f"""  <div class="scene-container">
    <div class="scene-split-container">
      <div class="text-side">
        {p_tags_cleaned}
      </div>
{visual_html}
    </div>
  </div>"""
        else:
            # 純文字排版
            inner_container = f"""  <div class="scene-container">
    <div class="text-wrapper">
      {p_tags_cleaned}
    </div>
  </div>"""

        # 替換 HTML 容器
        container_pattern = r'  <div class="scene-container">[\s\S]*?  </div>\n\n  <script>'
        new_html_content = re.sub(container_pattern, inner_container + "\n\n  <script>", html_content)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_html_content)

        # 2. 重構 CSS 內容
        if is_split:
            theme = split_scenes[scene_num]['theme']
            theme_css = css_effects[theme]
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
{theme_css}"""
            
            # 特別微調最後一幕的 Logo 樣式
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
        else:
            # 純文字樣式：文字置中，字級稍微加大以填滿版面
            css_template = f"""/* scene{scene_num}.css - 第 {scene_num} 幕專屬樣式 */

body {{
  background: linear-gradient(135deg, var(--color-bg-light) 0%, var(--color-accent) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}}

.text-wrapper {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 900px;
  text-align: center;
}}

.text-wrapper .animate-line {{
  font-family: "Noto Sans TC", sans-serif;
  font-size: 2.7rem; /* 純文字幕字級稍微放大，聚焦核心文案 */
  font-weight: 700;
  color: var(--color-text-main);
  margin: 18px 0;
  letter-spacing: 0.06em;
  line-height: 1.5;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.01);
}}"""

        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_template)
            
        print(f"Scene {scene_num}: {'[SPLIT ILLUSTRATION]' if is_split else '[PURE CENTERED TEXT]'} processed successfully.")

if __name__ == '__main__':
    main()

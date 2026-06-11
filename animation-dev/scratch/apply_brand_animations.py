# apply_brand_animations.py
import os
import re

def update_scenes():
    scenes_dir = r"C:\Users\wkoyo\Documents\家教網站\animation-dev\scenes"
    
    # 6 大主題分類
    # 主題 A: 1-3 (parent_anxiety.png)
    # 主題 B: 4-8 (industrial_education.png)
    # 主題 C: 9-14 (neurodiversity.png)
    # 主題 D: 15-18 (supportive_guide.png)
    # 主題 E: 19-26 (ai_mentor.png)
    # 主題 F: 27-31 (willing_to_learn.png)
    
    # HTML 的右半邊視覺容器模組
    visual_templates = {
        'A': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/parent_anxiety.png" class="scene-img anxiety-img" alt="家長懊惱與焦慮">
          <div class="bubble bubble-1">？</div>
          <div class="bubble bubble-2">？</div>
          <div class="bubble bubble-3">…</div>
        </div>
      </div>""",
      
        'B': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/industrial_education.png" class="scene-img industrial-img" alt="工業時期教育">
          <div class="gear gear-large">⚙️</div>
          <div class="gear gear-small">⚙️</div>
        </div>
      </div>""",
      
        'C': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/neurodiversity.png" class="scene-img neuro-img" alt="神經多樣性">
        </div>
      </div>""",
      
        'D': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/supportive_guide.png" class="scene-img guide-img" alt="陪伴守護小樹苗">
        </div>
      </div>""",
      
        'E': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/ai_mentor.png" class="scene-img ai-img" alt="AI耐心的陪伴指導">
        </div>
      </div>""",
      
        'F': """      <div class="visual-side fade-in delay-2s">
        <div class="image-wrapper">
          <img src="../assets/willing_to_learn.png" class="scene-img willing-img" alt="孩子找回願意學的心">
        </div>
      </div>"""
    }

    # CSS 動態特效模組
    css_templates = {
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
  background: rgba(220, 168, 66, 0.12);
  color: #DCA842;
  border: 2px solid rgba(220, 168, 66, 0.35);
  font-family: "Noto Sans TC", sans-serif;
  font-weight: 900;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(220, 168, 66, 0.1);
  user-select: none;
}

.bubble-1 {
  width: 52px;
  height: 52px;
  font-size: 1.6rem;
  top: 15%;
  left: -5%;
  animation: bubbleFloat1 8s ease-in-out infinite;
}

.bubble-2 {
  width: 42px;
  height: 42px;
  font-size: 1.3rem;
  top: 30%;
  right: -2%;
  animation: bubbleFloat2 10s ease-in-out infinite;
}

.bubble-3 {
  width: 48px;
  height: 48px;
  font-size: 1.4rem;
  bottom: 20%;
  left: 5%;
  animation: bubbleFloat3 9s ease-in-out infinite;
}

@keyframes bubbleFloat1 {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.7; }
  50% { transform: translateY(-16px) rotate(15deg) scale(1.08); opacity: 1; }
}

@keyframes bubbleFloat2 {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.6; }
  50% { transform: translateY(-12px) rotate(-15deg) scale(0.92); opacity: 0.9; }
}

@keyframes bubbleFloat3 {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.75; }
  50% { transform: translateY(-20px) rotate(10deg) scale(1.1); opacity: 1; }
}
""",
        
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
  color: rgba(42, 68, 73, 0.25);
  line-height: 1;
  user-select: none;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.05));
}

.gear-large {
  top: 18%;
  left: 14%;
  font-size: 5.5rem;
  animation: spinClockwise 12s linear infinite;
}

.gear-small {
  top: 36%;
  left: 24%;
  font-size: 3.8rem;
  animation: spinCounterClockwise 8s linear infinite;
}

@keyframes spinClockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spinCounterClockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(-360deg); }
}
""",
        
        'C': """
/* 大腦神經多樣性動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}

.neuro-img {
  /* 大腦微幅呼吸感與發光投影起伏 */
  animation: brainPulse 5s ease-in-out infinite !important;
}

@keyframes brainPulse {
  0%, 100% { 
    transform: scale(1) translateY(0); 
    filter: drop-shadow(0 15px 30px rgba(99, 134, 102, 0.1)); 
  }
  50% { 
    transform: scale(1.025) translateY(-5px); 
    filter: drop-shadow(0 20px 45px rgba(99, 134, 102, 0.25)); 
  }
}
""",
        
        'D': """
/* 守護陪伴發光小樹苗動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}

.guide-img {
  /* 溫暖呵護的微微起伏與光暈亮度呼吸 */
  animation: seedlingGrow 6s ease-in-out infinite !important;
}

@keyframes seedlingGrow {
  0%, 100% { 
    transform: translateY(0) scale(1); 
    filter: brightness(1) drop-shadow(0 15px 25px rgba(192, 169, 145, 0.15)); 
  }
  50% { 
    transform: translateY(-6px) scale(1.015); 
    filter: brightness(1.08) drop-shadow(0 22px 35px rgba(192, 169, 145, 0.3)); 
  }
}
""",
        
        'E': """
/* AI 機器人互動指導動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}

.ai-img {
  /* 機器人與孩子的微幅漂浮 */
  animation: aiFloat 5.5s ease-in-out infinite !important;
}

@keyframes aiFloat {
  0%, 100% { 
    transform: translateY(0) rotate(0deg); 
    filter: drop-shadow(0 15px 30px rgba(99, 134, 102, 0.08));
  }
  50% { 
    transform: translateY(-8px) rotate(0.8deg); 
    filter: drop-shadow(0 22px 40px rgba(99, 134, 102, 0.22));
  }
}
""",
        
        'F': """
/* 願意學自信孩童朝向陽光動態 */
.image-wrapper {
  position: relative;
  display: inline-block;
}

.willing-img {
  /* 向著陽光與未來前進的昂揚動態 */
  animation: sunRise 7s ease-in-out infinite !important;
}

@keyframes sunRise {
  0%, 100% { 
    transform: translateY(0) scale(1); 
    filter: drop-shadow(0 15px 30px rgba(192, 169, 145, 0.12));
  }
  50% { 
    transform: translateY(-10px) scale(1.02); 
    filter: drop-shadow(0 25px 45px rgba(192, 169, 145, 0.28));
  }
}
"""
    }

    def get_theme(scene_num):
        if 1 <= scene_num <= 3:
            return 'A'
        elif 4 <= scene_num <= 8:
            return 'B'
        elif 9 <= scene_num <= 14:
            return 'C'
        elif 15 <= scene_num <= 18:
            return 'D'
        elif 19 <= scene_num <= 26:
            return 'E'
        elif 27 <= scene_num <= 31:
            return 'F'
        return 'A'

    # 開始處理這 31 幕
    for scene_num in range(1, 32):
        theme = get_theme(scene_num)
        
        # 1. 處理 HTML 檔案
        html_file = os.path.join(scenes_dir, f"scene{scene_num}.html")
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 如果還沒有被轉換為 scene-split-container
            if "scene-split-container" not in html_content:
                # 尋找內部的段落內容，將其提取出來
                p_matches = re.findall(r'<p[^>]*class="animate-line[^>]*">[\s\S]*?</p>', html_content)
                p_tags_content = "\n        ".join([p.strip() for p in p_matches])
                
                # 新的 HTML 結構
                new_container = f"""  <div class="scene-container">
    <div class="scene-split-container">
      <div class="text-side">
        {p_tags_content}
      </div>
{visual_templates[theme]}
    </div>
  </div>"""
                
                # 用正則替換掉舊的 scene-container 區塊
                container_pattern = r'  <div class="scene-container">[\s\S]*?  </div>\n\n  <script>'
                updated_html = re.sub(container_pattern, new_container + "\n\n  <script>", html_content)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(updated_html)
                print(f"HTML Scene {scene_num} (Theme {theme}) -> Converted to split screen.")
            else:
                # 如果已經是分割版面，但我們還是需要確保它有對應主題的正確圖片和結構（特別是 Scene 2, 3，或者是剛剛沒覆蓋的）
                # 這裡就跳過，保護已手動微調的 Scene 1, 4, 5。
                # 為了確保 Scene 2 和 3 也被上圖，因為它們之前是 split-container 嗎？
                # Scene 2 和 3 原本在 excel 生產時是 text-wrapper，所以會被正確轉化。
                print(f"HTML Scene {scene_num} -> Already split layout, skipping HTML rewrite.")

        # 2. 處理 CSS 檔案
        css_file = os.path.join(scenes_dir, f"scene{scene_num}.css")
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # 我們要將 CSS 重塑，使用統一的 text-side 排版，並追加對應主題的 CSS 動畫
            # 保留 body 背景（即使 global.css 覆蓋了 body 背景，這無傷大雅）
            
            # 新的 CSS 模板
            new_css = f"""/* scene{scene_num}.css - 第 {scene_num} 幕專屬樣式 */

body {{
  background: linear-gradient(135deg, #FCFAF5 0%, #F5F1E6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}}

.text-side .animate-line {{
  font-family: "Noto Sans TC", sans-serif;
  font-size: 2.3rem;
  font-weight: 700;
  color: #2C3D4D;
  margin: 16px 0;
  letter-spacing: 0.05em;
  line-height: 1.5;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}}
{css_templates[theme]}"""

            # 針對最後一幕（Scene 31）微調 CTA 樣式
            if scene_num == 31:
                new_css += """
.text-side .animate-line:nth-child(2) {
  font-family: "Noto Serif TC", serif;
  font-size: 2.8rem;
  color: var(--color-primary);
  font-weight: 900;
  margin-top: 24px;
}
.text-side .animate-line:nth-child(3) {
  font-size: 1.5rem;
  color: var(--color-secondary);
  font-weight: 700;
}
"""

            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(new_css)
            print(f"CSS Scene {scene_num} (Theme {theme}) -> Updated styles and theme animations.")

if __name__ == "__main__":
    update_scenes()

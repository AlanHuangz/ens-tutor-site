# bootstrap_scenes.py - 從 Excel 自動生成所有動畫場景與播放器配置

import os
import re
import pandas as pd

def bootstrap():
    excel_path = '影片字卡.xlsx'
    if not os.path.exists(excel_path):
        print(f"錯誤：找不到 {excel_path} 檔案！請確保它位於 animation-dev 目錄下。")
        return

    # 讀取 Excel 檔案
    df = pd.read_excel(excel_path)
    if '文字' not in df.columns:
        print("錯誤：Excel 檔案中找不到名為「文字」的欄位！")
        return

    # 建立 scenes 目錄
    os.makedirs('scenes', exist_ok=True)
    
    scene_configs = []

    for idx, row in df.iterrows():
        scene_num = idx + 1
        raw_text = str(row['文字']).strip()
        
        # 濾掉空的行
        if not raw_text or raw_text.lower() == 'nan':
            continue
            
        # 分割文字（以 / 為斷行）
        lines = [line.strip() for line in raw_text.split('/')]
        
        # 決定這一幕的顯示秒數：每行給予 1.5 秒閱讀時間 + 基礎 2.5 秒
        duration_ms = int(2500 + len(lines) * 1500)
        
        # 用前幾個字當作場景的縮寫名稱
        clean_preview = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', raw_text)
        preview_name = clean_preview[:8] + '...' if len(clean_preview) > 8 else clean_preview
        scene_name = f"第 {scene_num} 幕：{preview_name}"
        
        scene_configs.append({
            'url': f'scenes/scene{scene_num}.html',
            'name': scene_name,
            'duration': duration_ms
        })

        # 1. 建立 HTML 檔案 (若不存在才建立，保護您的手動修改)
        html_file = f'scenes/scene{scene_num}.html'
        if not os.path.exists(html_file):
            # 建立段落 HTML
            p_tags = []
            for line_idx, line_text in enumerate(lines):
                delay_class = f" delay-{line_idx}s" if line_idx > 0 else ""
                p_tags.append(f'      <p class="animate-line fade-in-up{delay_class}">{line_text}</p>')
            
            p_content = "\n".join(p_tags)
            
            html_template = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <title>{scene_name}</title>
  <link rel="stylesheet" href="../shared/reset.css">
  <link rel="stylesheet" href="../shared/global.css">
  <link rel="stylesheet" href="scene{scene_num}.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&family=Noto+Serif+TC:wght@900&display=swap">
</head>
<body>
  <div class="scene-container">
    <div class="text-wrapper">
{p_content}
    </div>
  </div>

  <script>
    // 動畫播放完畢後主動通知播放器切換
    setTimeout(() => {
      window.parent.postMessage({ type: 'SCENE_COMPLETE' }, '*');
    }, {duration_ms});
  </script>
</body>
</html>
"""
            html_template = html_template.replace('{scene_name}', scene_name)\
                                         .replace('{scene_num}', str(scene_num))\
                                         .replace('{p_content}', p_content)\
                                         .replace('{duration_ms}', str(duration_ms))

            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_template)
            print(f"已生成：{html_file}")
        else:
            print(f"已存在，跳過生成：{html_file}")

    # 2. 建立 CSS 檔案 (若不存在才建立，保護您的手動修改)
        css_file = f'scenes/scene{scene_num}.css'
        if not os.path.exists(css_file):
            # 預設場景樣式 (偶數場景用稍微不同的背景色增加變化)
            bg_gradient = "linear-gradient(135deg, #FCFAF5 0%, #F5F1E6 100%)" if scene_num % 2 != 0 else "linear-gradient(135deg, #F9FAFB 0%, #EEF2F6 100%)"
            
            css_template = """/* scene{scene_num}.css - 第 {scene_num} 幕專屬樣式 */

body {
  background: {bg_gradient};
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 800px;
}

.animate-line {
  font-family: "Noto Sans TC", sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: #2C3D4D;
  margin: 12px 0;
  letter-spacing: 0.05em;
  line-height: 1.4;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}
"""
            css_template = css_template.replace('{scene_num}', str(scene_num))\
                                       .replace('{bg_gradient}', bg_gradient)

            # 針對最後一幕做特別樣式（LOGO 與呼籲）
            if idx == len(df) - 1:
                css_template += """
/* 為最後一幕微調文字尺寸與顏色 */
.animate-line:nth-child(2) {
  font-family: "Noto Serif TC", serif;
  font-size: 3rem;
  color: #2A4449;
  font-weight: 900;
  margin-top: 24px;
}
.animate-line:nth-child(3) {
  font-size: 1.4rem;
  color: #DCA842;
  font-weight: 700;
}
"""

            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_template)
            print(f"已生成：{css_file}")
        else:
            print(f"已存在，跳過生成：{css_file}")

    # 3. 重新生成 js/player.js 中的 sceneConfig
    js_file = 'js/player.js'
    if os.path.exists(js_file):
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content = f.read()
            
        # 以正則表達式取代 sceneConfig 陣列
        config_str = "const sceneConfig = [\n"
        for i, cfg in enumerate(scene_configs):
            comma = "," if i < len(scene_configs) - 1 else ""
            config_str += f"  {{ url: '{cfg['url']}', name: '{cfg['name']}', duration: {cfg['duration']} }}{comma}\n"
        config_str += "];"
        
        # 尋找舊的 sceneConfig 定義並替換
        pattern = r'const sceneConfig = \[\s*[\s\S]*?\];'
        new_js_content = re.sub(pattern, config_str, js_content)
        
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(new_js_content)
        print("已更新播放器配置：js/player.js")
        
    print("\n恭喜！文字動畫場景全部引導生成完畢！")

if __name__ == '__main__':
    bootstrap()

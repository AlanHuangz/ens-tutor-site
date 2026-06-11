# highlight_texts.py
import os
import re

def run_highlights():
    scenes_dir = r"C:\Users\wkoyo\Documents\家教網站\animation-dev\scenes"
    
    # 每一幕需要強調的關鍵字對照表
    highlights_map = {
        1: ["一代不如一代"],
        3: ["閃光點", "學習方式"],
        4: ["工業時期"],
        5: ["穩定、標準、效率與同步"],
        6: ["工業時代"],
        7: ["停留在原地"],
        8: ["肯努力，就一定能成功"],
        9: ["神經多樣性"],
        10: ["都不一樣"],
        11: ["三十個孩子"],
        12: ["學習軌道"],
        13: ["顧進度、顧班級、顧考試"],
        14: ["量身規劃", "太難了"],
        15: ["三種核心心理需求"],
        16: ["「自主感」"],
        17: ["「勝任感」"],
        18: ["「歸屬感」"],
        19: ["AI", "學習節奏"],
        20: ["多元的選擇"],
        21: ["選擇權", "「自主感」"],
        22: ["AI", "耐心拆解", "100 遍"],
        23: ["跟不上別人"],
        24: ["隨時想問就問", "沒有心理負擔"],
        25: ["一定都學得會"],
        26: ["「勝任感」"],
        27: ["「自主」", "「勝任」", "餘裕"],
        28: ["走進孩子的內心"],
        29: ["「歸屬感」"],
        30: ["「動力」"],
        31: ["「願意學」", "AI時代"]
    }
    
    for scene_num, keywords in highlights_map.items():
        html_file = os.path.join(scenes_dir, f"scene{scene_num}.html")
        if not os.path.exists(html_file):
            print(f"Warning: {html_file} not found.")
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        updated = False
        new_content = content
        
        # 尋找 <p class="animate-line ...">...</p> 中的文字，僅在這些段落中進行替換，避免破壞外部標籤
        p_pattern = r'(<p[^>]*class="animate-line[^>]*">)([\s\S]*?)(</p>)'
        
        def replace_in_p(match):
            nonlocal updated
            prefix = match.group(1)
            p_text = match.group(2)
            suffix = match.group(3)
            
            # 對於每個要強調的關鍵字進行替換
            for kw in keywords:
                # 為了防止重複包含（例如先替換了「自主」，又替換了「自主感」中的「自主」），需要小心
                # 這裡可以用正則，確保 kw 沒被 span 包裹。
                # 簡單的方法是，如果 kw 已經被 span 包裹，就跳過。
                if f'class="highlight"' in p_text and kw in p_text:
                    # 如果已經有 highlight 標籤了，可能已經處理過
                    continue
                
                # 進行安全替換
                if kw in p_text:
                    p_text = p_text.replace(kw, f'<span class="highlight">{kw}</span>')
                    updated = True
            return prefix + p_text + suffix

        new_content = re.sub(p_pattern, replace_in_p, content)
        
        if updated:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Scene {scene_num}: Applied highlights for {keywords}")
        else:
            print(f"Scene {scene_num}: No change needed or already highlighted.")

if __name__ == "__main__":
    run_highlights()

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const scenesDir = path.join(root, 'scenes');

const sceneDataPath = path.join(root, 'scenes-data.json');
const sceneData = JSON.parse(fs.readFileSync(sceneDataPath, 'utf8'));

function delay(i) {
  const delays = ['', ' delay-500ms', ' delay-1s', ' delay-1500ms', ' delay-2s'];
  return i < delays.length ? delays[i] : ' delay-2s';
}

function visual(scene) {
  const img = path.join(root, 'assets', scene.img);
  const src = fs.existsSync(img) ? scene.img : scene.fallback;
  if (scene.n === 31) {
    return `<div class="final-logo-wrap scale-in">
        <img src="../assets/${src}?v=6.0" class="scene-img final-logo-img" alt="${scene.alt}">
      </div>`;
  }
  return `<div class="photo-stage photo-scene-${String(scene.n).padStart(2, '0')}">
          <span class="photo-light l1"></span>
          <span class="photo-light l2"></span>
          <img src="../assets/${src}" class="scene-img photo-img" alt="${scene.alt}">
          <span class="photo-thread"></span>
        </div>`;
}

function html(scene) {
  const lines = scene.lines.map((line, i) => {
    const strong = i === scene.lines.length - 1 && scene.n !== 31 ? ' emph-line' : '';
    return `        <p class="animate-line fade-in-up${delay(i)}${strong}">${line}</p>`;
  }).join('\n');
  const completion = Math.max(3600, 2600 + scene.lines.length * 640);
  const finalClass = scene.n === 31 ? ' final-scene' : '';
  return `<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>第 ${scene.n} 幕：${scene.title}</title>
  <link rel="stylesheet" href="../shared/reset.css">
  <link rel="stylesheet" href="../shared/global.css?v=1.7">
  <link rel="stylesheet" href="scene${scene.n}.css">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&family=Noto+Serif+TC:wght@900&display=swap">
</head>
<body>
  <div class="scene-container${finalClass}">
    <div class="story-layout">
      <div class="story-copy">
${lines}
      </div>
      <div class="story-visual fade-in delay-500ms" aria-hidden="true">
        ${visual(scene)}
      </div>
    </div>
    <div class="brand-signature"><span>先懂孩子，再懂數學</span><span>AI時代的自學教練</span></div>
  </div>

  <script>
    setTimeout(() => {
      window.parent.postMessage({ type: 'SCENE_COMPLETE' }, '*');
    }, ${completion});
    if (new URLSearchParams(window.location.search).get('qa') === 'still') {
      document.body.classList.add('qa-still');
    }
  </script>
</body>
</html>
`;
}

for (const scene of sceneData) {
  fs.writeFileSync(path.join(scenesDir, `scene${scene.n}.html`), html(scene), 'utf8');
}

const playerPath = path.join(root, 'js', 'player.js');
let player = fs.readFileSync(playerPath, 'utf8');
const config = `const sceneConfig = [\n${sceneData.map((scene) => {
  const duration = Math.max(3900, 2850 + scene.lines.length * 700);
  return `  { url: 'scenes/scene${scene.n}.html', name: '第 ${scene.n} 幕：${scene.title}', duration: ${duration} }`;
}).join(',\n')}\n];`;
player = player.replace(/const sceneConfig = \[[\s\S]*?\];/, config);
fs.writeFileSync(playerPath, player, 'utf8');

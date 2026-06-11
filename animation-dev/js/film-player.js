const beats = [
  ['你是否也常聽人說', '孩子真的變差了嗎？', '有人說「一代不如一代」，但我並不這麼認為', ['孩子', '變差'], ['焦慮', '責怪', '比較'], 'dim-eyes', 7600],
  ['我相信，每個時代的孩子', '都有正確的開啟方式', '只是鑰匙，已經不再是上一個時代那一把', ['開啟', '鑰匙'], ['入口', '理解', '方式'], 'door', 7900],
  ['我們熟悉的教育樣貌', '工業時代的答案', '穩定、標準、效率、同步，是那個時代的答案', ['工業', '答案'], ['穩定', '標準', '效率'], 'factory', 8500],
  ['但我們距離工業時期', '時代已經變了', '科技往前衝，教室裡的方式卻常常停在原地', ['時代', '變了'], ['科技', '教室', '落差'], 'track', 8300],
  ['以前我們常說', '每個大腦都不同', '「別人做得到，你也做得到」忽略了速度、順序與吸收方式', ['大腦', '不同'], ['速度', '順序', '感官'], 'neuro', 9000],
  ['一位老師面對二、三十個孩子', '不是老師不努力', '是要同時顧進度、考試、秩序、情緒，真的太難', ['不是', '太難'], ['進度', '考試', '情緒'], 'crowd', 8800],
  ['教育現場最讓人心疼的', '是兩眼無光的少年', '不是沒有能力，而是一次次挫折後，慢慢不願意了', ['兩眼無光', '不願意'], ['挫折', '沉默', '退縮'], 'dim-eyes', 9400],
  ['所以我們在乎的，不只是分數', '自主 勝任 歸屬', '自主感、勝任感、歸屬感，是願意學的底層燃料', ['自主', '勝任', '歸屬'], ['自主', '勝任', '歸屬'], 'three-senses', 8500],
  ['第一，自主感', '我可以選擇怎麼學', '圖像、影像、聽覺、步調，孩子終於有自己的入口', ['選擇', '入口'], ['選擇權', '入口', '節奏'], 'door', 7600],
  ['第二，勝任感', '我不是不行', '只是需要能拆小步、能反覆問、能慢慢成功的路', ['不是不行', '成功'], ['拆解', '反覆', '成功'], 'steps', 7900],
  ['第三，歸屬感', '挫折時有人接住我', '當不安被溫柔接住，孩子才敢再次提問', ['接住', '提問'], ['安心', '陪伴', '提問'], 'orbit', 7900],
  ['AI 的價值，不是取代老師', '卡住時 立刻被接住', '讓卡住的那一刻，馬上有新的解法可以試', ['卡住', '接住'], ['AI', '即時', '回饋'], 'signal', 8000],
  ['願意學的優勢', '先懂孩子 再懂數學', '我們用 AI 的彈性，加上人的理解，陪孩子找回光', ['懂孩子', '數學', '光'], ['理解', '方法', '陪跑'], 'light-eyes', 9000],
  ['很多時候', '孩子不是學不會', '而是還沒有重新願意學', ['不是學不會', '願意學'], ['重啟', '願意', '改變'], 'door', 8000],
  ['', '', '', [], [], 'logo', 7000]
].map(([kicker, headline, support, hot, cloud, metaphor, duration]) => ({ kicker, headline, support, hot, cloud, metaphor, duration }));

const metaphorTemplates = {
  factory: '<span class="conveyor"></span><span class="factory-box a"></span><span class="factory-box b"></span><span class="gear g1"></span><span class="gear g2"></span>',
  track: '<span class="track fast"><i></i></span><span class="track slow"><i></i></span>',
  neuro: '<span class="node n1"></span><span class="node n2"></span><span class="node n3"></span><span class="path p1"></span><span class="path p2"></span>',
  crowd: '<span class="student s1"></span><span class="student s2"></span><span class="student s3"></span><span class="student s4"></span><span class="student s5"></span>',
  'dim-eyes': '<span class="eye left"></span><span class="eye right"></span>',
  'light-eyes': '<span class="eye left bright"></span><span class="eye right bright"></span><span class="ray"></span>',
  'three-senses': '<span class="sense-ring"></span><span class="sense a"></span><span class="sense b"></span><span class="sense c"></span>',
  steps: '<span class="step a"></span><span class="step b"></span><span class="step c"></span><span class="step d"></span>',
  orbit: '<span class="orbit a"></span><span class="orbit b"></span><span class="core"></span>',
  signal: '<span class="bar a"></span><span class="bar b"></span><span class="bar c"></span>',
  door: '<span class="open-door"></span><span class="door-light"></span>',
  logo: ''
};

const film = document.querySelector('.film');
const scene = document.getElementById('scene');
const kicker = document.getElementById('kicker');
const headline = document.getElementById('headline');
const support = document.getElementById('support');
const cloud = document.getElementById('wordCloud');
const metaphor = document.getElementById('metaphor');
const progress = document.getElementById('progress');
const playBtn = document.getElementById('playBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const params = new URLSearchParams(window.location.search);

let index = 0;
let playing = !(params.get('paused') === '1' || params.get('paused') === 'true');
let beatStart = performance.now();
let pausedAt = 0;
let raf = null;
let transitioning = false;
let transitionTimer = null;
const keepControls = params.get('controls') === '1' || params.get('controls') === 'true';
const freeze = params.get('freeze') === '1' || params.get('freeze') === 'true';

function renderBeat(nextIndex) {
  if (transitionTimer) clearTimeout(transitionTimer);
  transitioning = false;
  index = (nextIndex + beats.length) % beats.length;
  const beat = beats[index];
  film.className = `film ${beat.metaphor}`;
  film.classList.toggle('show-controls', keepControls);
  film.classList.toggle('qa-freeze', freeze);
  film.classList.toggle('show-logo', beat.metaphor === 'logo');
  scene.className = `scene ${beat.metaphor}`;
  kicker.innerHTML = renderDialogue(beat.kicker);
  headline.innerHTML = renderHeadline(beat.headline, beat.hot);
  support.innerHTML = renderDialogue(beat.support);
  cloud.innerHTML = renderCloud(beat.cloud);
  metaphor.className = `metaphor ${beat.metaphor}`;
  metaphor.innerHTML = metaphorTemplates[beat.metaphor] || '';
  beatStart = performance.now();
  pausedAt = 0;
}

function renderHeadline(text, hotWords) {
  if (!text) return '';
  return text.split(/(\s+|，|。|、)/).filter(Boolean).map((part, i) => {
    const clean = part.replace(/[，。、\s？]/g, '');
    const hot = hotWords.some((word) => clean && (clean.includes(word) || word.includes(clean)));
    return `<span class="word${hot ? ' hot' : ''}" style="--i:${i}">${part}</span>`;
  }).join('');
}

function renderDialogue(text) {
  if (!text) return '';
  const chunks = text.match(/[^，。；：、]+[，。；：、]?/g) || [text];
  return chunks.map((chunk, i) => `<span class="cue" style="--j:${i}">${chunk}</span>`).join('');
}

function renderCloud(words) {
  const pos = [['17%', '23%', '-8deg', '0s'], ['80%', '22%', '7deg', '-1.2s'], ['20%', '76%', '5deg', '-2s'], ['79%', '72%', '-6deg', '-0.6s']];
  return words.map((word, i) => {
    const [left, top, rotate, delay] = pos[i % pos.length];
    return `<span class="cloud-word" style="left:${left};top:${top};--r:${rotate};--d:${delay}">${word}</span>`;
  }).join('');
}

function tick(now) {
  if (!playing) return;
  const beat = beats[index];
  const elapsed = now - beatStart;
  const totalBefore = beats.slice(0, index).reduce((sum, item) => sum + item.duration, 0);
  const total = beats.reduce((sum, item) => sum + item.duration, 0);
  progress.style.width = `${Math.min(((totalBefore + elapsed) / total) * 100, 100)}%`;
  if (elapsed >= beat.duration && !transitioning) {
    transitioning = true;
    scene.classList.add('scene-out');
    transitionTimer = setTimeout(() => renderBeat(index + 1), 360);
  }
  raf = requestAnimationFrame(tick);
}

function play() {
  if (playing) return;
  playing = true;
  film.classList.remove('paused');
  beatStart = performance.now() - pausedAt;
  setAnimationState('running');
  raf = requestAnimationFrame(tick);
}

function pause() {
  if (!playing) return;
  playing = false;
  film.classList.add('paused');
  pausedAt = performance.now() - beatStart;
  if (raf) cancelAnimationFrame(raf);
  setAnimationState('paused');
}

function setAnimationState(state) {
  document.querySelectorAll('*').forEach((el) => {
    el.style.animationPlayState = state;
  });
}

function go(delta) {
  if (raf) cancelAnimationFrame(raf);
  renderBeat(index + delta);
  if (playing) raf = requestAnimationFrame(tick);
}

playBtn.addEventListener('click', () => playing ? pause() : play());
prevBtn.addEventListener('click', () => go(-1));
nextBtn.addEventListener('click', () => go(1));

const startBeat = Number.parseInt(params.get('beat') || '0', 10);
renderBeat(Number.isFinite(startBeat) ? startBeat : 0);
if (playing) {
  raf = requestAnimationFrame(tick);
} else {
  film.classList.add('paused');
  setAnimationState('paused');
}

const beats = [
  ['你是否也常聽人說', '孩子真的變差了嗎？', '有人說「一代不如一代」。可是我想先問：真的是孩子變差了嗎？', ['孩子', '變差'], ['焦慮', '責怪', '比較'], 'dim-eyes', 8500],
  ['如果不是呢？', '也許是方法舊了', '孩子沒有少了能力。只是我們還常用上一個時代的方法，要求他們面對現在的世界。', ['方法', '舊了'], ['方法', '時代', '落差'], 'door', 8800],
  ['我們今天熟悉的教育', '來自工業時代', '那套系統擅長穩定、標準、效率與同步。它曾經很有用，因為那是當時的答案。', ['工業', '時代'], ['穩定', '標準', '效率'], 'factory', 9000],
  ['可是現在的孩子', '活在完全不同的世界', '科技往前衝，資訊爆炸，選擇變多；但很多學習方式，卻還停在同一條跑道上。', ['不同', '世界'], ['科技', '資訊', '選擇'], 'track', 9200],
  ['更重要的是', '每個大腦都不一樣', '有人靠圖像理解，有人需要聲音，有人要慢慢拆步驟。速度、順序、入口，本來就不相同。', ['大腦', '不一樣'], ['圖像', '聲音', '步驟'], 'neuro', 9600],
  ['所以問題不只是孩子', '老師也被困住了', '一位老師要同時顧進度、考試、秩序與情緒，還要照顧二、三十種不同的學習節奏。', ['老師', '困住'], ['進度', '考試', '情緒'], 'crowd', 9600],
  ['於是我們在教室裡看見', '兩眼無光的學生', '他們不一定是不會。很多時候，是一次次跟不上、問不出口，最後慢慢不願意了。', ['兩眼無光', '不願意'], ['跟不上', '沉默', '退縮'], 'dim-eyes', 9800],
  ['所以真正要重建的', '不是只有成績', '我們要先把孩子重新帶回三種感受：自主感、勝任感、歸屬感。', ['不是', '成績'], ['自主', '勝任', '歸屬'], 'three-senses', 8500],
  ['先有自主感', '我可以選擇怎麼學', '用圖像、用影片、用聲音，或照自己的步調來。當孩子有入口，學習才會開始。', ['選擇', '入口'], ['圖像', '影片', '步調'], 'door', 8800],
  ['再有勝任感', '我相信自己做得到', '不是把答案塞給他，而是把卡住的地方拆小，讓他一步一步真的成功。', ['做得到', '成功'], ['拆小', '練習', '成功'], 'steps', 8800],
  ['最後是歸屬感', '挫折時有人接住我', '孩子敢問，不是因為他不怕錯；而是因為他知道，錯了也不會被丟下。', ['接住', '不會被丟下'], ['安心', '陪伴', '提問'], 'orbit', 9000],
  ['這時 AI 的價值出現了', '卡住的當下就能回應', '它可以換一種說法、拆一個步驟，甚至耐心解釋一百遍，先把心理負擔放下。', ['AI', '回應'], ['即時', '拆解', '耐心'], 'signal', 9200],
  ['而人的角色更重要', '把光帶回孩子眼裡', 'AI 負責彈性與即時，老師和家長就有更多餘裕，看見孩子真正需要的是什麼。', ['人', '光'], ['理解', '餘裕', '陪伴'], 'light-eyes', 9400],
  ['所以我們相信', '先懂孩子，再懂數學', '很多孩子不是學不會，而是還沒有被帶回「願意」。願意了，學習才真的開始。', ['懂孩子', '懂數學'], ['願意', '開始', '改變'], 'door', 9400],
  ['', '', '', [], [], 'logo', 7600]
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

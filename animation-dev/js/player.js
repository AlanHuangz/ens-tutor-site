const sceneConfig = [
  { url: 'scenes/scene1.html', name: '第 1 幕：你是否也常聽人說', duration: 4250 },
  { url: 'scenes/scene2.html', name: '第 2 幕：我並不這麼認為', duration: 4250 },
  { url: 'scenes/scene3.html', name: '第 3 幕：正確的開啟方式', duration: 5650 },
  { url: 'scenes/scene4.html', name: '第 4 幕：教育來自工業時期', duration: 4950 },
  { url: 'scenes/scene5.html', name: '第 5 幕：標準效率同步', duration: 5650 },
  { url: 'scenes/scene6.html', name: '第 6 幕：距離工業時期很遠', duration: 4950 },
  { url: 'scenes/scene7.html', name: '第 7 幕：科技快速前進', duration: 4950 },
  { url: 'scenes/scene8.html', name: '第 8 幕：不是孩子變差', duration: 5650 },
  { url: 'scenes/scene9.html', name: '第 9 幕：每個孩子不同', duration: 4950 },
  { url: 'scenes/scene10.html', name: '第 10 幕：學習方式不同', duration: 4250 },
  { url: 'scenes/scene11.html', name: '第 11 幕：一位老師三十個孩子', duration: 4950 },
  { url: 'scenes/scene12.html', name: '第 12 幕：老師已經很努力', duration: 4950 },
  { url: 'scenes/scene13.html', name: '第 13 幕：老師同時顧很多事', duration: 4250 },
  { url: 'scenes/scene14.html', name: '第 14 幕：量身打造太難', duration: 4950 },
  { url: 'scenes/scene15.html', name: '第 15 幕：三種感受', duration: 4950 },
  { url: 'scenes/scene16.html', name: '第 16 幕：自主感', duration: 4950 },
  { url: 'scenes/scene17.html', name: '第 17 幕：勝任感', duration: 4950 },
  { url: 'scenes/scene18.html', name: '第 18 幕：歸屬感', duration: 4950 },
  { url: 'scenes/scene19.html', name: '第 19 幕：AI貼近節奏', duration: 4950 },
  { url: 'scenes/scene20.html', name: '第 20 幕：更多選擇', duration: 4950 },
  { url: 'scenes/scene21.html', name: '第 21 幕：自主感建立', duration: 4950 },
  { url: 'scenes/scene22.html', name: '第 22 幕：AI耐心拆解', duration: 4950 },
  { url: 'scenes/scene23.html', name: '第 23 幕：不用面對不耐煩', duration: 4250 },
  { url: 'scenes/scene24.html', name: '第 24 幕：小成功累積', duration: 4950 },
  { url: 'scenes/scene25.html', name: '第 25 幕：老師家長有餘裕', duration: 4950 },
  { url: 'scenes/scene26.html', name: '第 26 幕：真正接住孩子', duration: 4950 },
  { url: 'scenes/scene27.html', name: '第 27 幕：歸屬感建立', duration: 4950 },
  { url: 'scenes/scene28.html', name: '第 28 幕：不是學不會', duration: 4950 },
  { url: 'scenes/scene29.html', name: '第 29 幕：重新願意學', duration: 4950 }
];

let currentIndex = 0;
let isPlaying = true;
let isMuted = true;
let timer = null;
let startTime = 0;
let elapsed = 0;
let duration = sceneConfig[0].duration;
let isTransitioning = false;

const urlParams = new URLSearchParams(window.location.search);
const showControls = urlParams.get('controls') === '1' || urlParams.get('controls') === 'true';
document.body.classList.toggle('show-controls', showControls);

const iframe1 = document.getElementById('scene-frame-1');
const iframe2 = document.getElementById('scene-frame-2');
let activeIframe = iframe1;
let inactiveIframe = iframe2;

const indicator = document.querySelector('.scene-indicator');
const progress = document.getElementById('timeline-progress');
const playBtn = document.getElementById('play-btn');
const playIcon = document.getElementById('play-icon');
const pauseIcon = document.getElementById('pause-icon');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const musicBtn = document.getElementById('music-btn');
const muteIcon = document.getElementById('mute-icon');
const soundIcon = document.getElementById('sound-icon');
const bgMusic = document.getElementById('bg-music');

function init() {
  sessionStorage.setItem('is_interactive_mode', 'false');
  activeIframe = iframe1;
  inactiveIframe = iframe2;
  indicator.textContent = `${sceneConfig[0].name} (1/${sceneConfig.length})`;

  activeIframe.onload = () => {
    setIframePlayState(activeIframe, isPlaying ? 'running' : 'paused');
    if (isPlaying) startTimer();
    activeIframe.onload = null;
  };

  playBtn.addEventListener('click', togglePlay);
  prevBtn.addEventListener('click', prevScene);
  nextBtn.addEventListener('click', nextScene);
  musicBtn.addEventListener('click', toggleMusic);

  // 首次點擊或觸摸網頁時，自動解鎖音訊並開始播放背景音樂 (繞過瀏覽器限制)
  function unlockAudio() {
    isMuted = false;
    muteIcon.style.display = 'none';
    soundIcon.style.display = 'block';
    musicBtn.classList.remove('muted');
    bgMusic.muted = false;
    bgMusic.play().then(() => {
      console.log("音訊解鎖成功，開始播放背景音樂");
    }).catch(e => {
      console.log("首點音訊播放失敗：", e);
    });
    // 移除事件，只需解鎖一次
    document.removeEventListener('click', unlockAudio);
    document.removeEventListener('touchstart', unlockAudio);
  }
  document.addEventListener('click', unlockAudio);
  document.addEventListener('touchstart', unlockAudio);

  bgMusic.addEventListener('error', () => {
    console.log("本地背景音樂載入失敗，切換至備用音訊...");
    const fallbackUrl = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3';
    if (bgMusic.src !== fallbackUrl) {
      bgMusic.src = fallbackUrl;
      bgMusic.load();
      if (!isMuted && isPlaying) {
        bgMusic.play().catch(e => console.log("備用音樂播放失敗：", e));
      }
    } else {
      console.log("備用音樂也載入失敗，隱藏音樂按鈕");
      bgMusic.pause();
      musicBtn.style.display = 'none';
    }
  });

  window.addEventListener('message', (event) => {
    if (!event.data || event.source !== activeIframe.contentWindow) return;
    if (event.data.type === 'SCENE_COMPLETE') {
      if (elapsed >= duration - 700) nextScene();
    }
    if (event.data.type === 'GO_TO_SCENE') loadScene(event.data.index);
  });
}

function loadScene(index) {
  if (index < 0 || index >= sceneConfig.length || isTransitioning) return;

  isTransitioning = true;
  resetTimer();
  currentIndex = index;
  duration = sceneConfig[currentIndex].duration;
  elapsed = 0;
  progress.style.width = '0%';
  indicator.textContent = `${sceneConfig[currentIndex].name} (${currentIndex + 1}/${sceneConfig.length})`;

  const nextUrl = sceneConfig[currentIndex].url;
  let loaded = false;
  const previousIframe = activeIframe;

  inactiveIframe.className = 'scene-frame incoming';
  inactiveIframe.onload = () => {
    if (loaded) return;
    loaded = true;
    setIframePlayState(inactiveIframe, isPlaying ? 'running' : 'paused');

    previousIframe.className = 'scene-frame outgoing';
    inactiveIframe.className = 'scene-frame active';

    const temp = activeIframe;
    activeIframe = inactiveIframe;
    inactiveIframe = temp;

    window.setTimeout(() => {
      previousIframe.onload = null;
      if (previousIframe === inactiveIframe) previousIframe.src = 'about:blank';
      isTransitioning = false;
      if (isPlaying) startTimer();
    }, 780);
  };

  window.setTimeout(() => {
    if (!loaded && inactiveIframe.onload) inactiveIframe.onload();
  }, 2500);

  inactiveIframe.src = nextUrl;
}

function startTimer() {
  resetTimer();
  startTime = Date.now() - elapsed;

  function updateProgress() {
    if (!isPlaying) return;

    elapsed = Date.now() - startTime;
    const percent = Math.min((elapsed / duration) * 100, 100);
    progress.style.width = `${percent}%`;

    if (elapsed >= duration) nextScene();
    else timer = requestAnimationFrame(updateProgress);
  }

  timer = requestAnimationFrame(updateProgress);
}

function resetTimer() {
  if (timer) {
    cancelAnimationFrame(timer);
    timer = null;
  }
}

function togglePlay() {
  isPlaying = !isPlaying;
  playIcon.style.display = isPlaying ? 'none' : 'block';
  pauseIcon.style.display = isPlaying ? 'block' : 'none';
  setIframePlayState(activeIframe, isPlaying ? 'running' : 'paused');

  if (isPlaying) {
    startTimer();
    if (!isMuted) bgMusic.play().catch(() => {});
  } else {
    resetTimer();
    bgMusic.pause();
  }
}

function setIframePlayState(targetIframe, state) {
  try {
    const doc = targetIframe.contentDocument || targetIframe.contentWindow.document;
    if (!doc || !doc.body) return;
    doc.body.style.setProperty('--play-state', state);
    doc.body.querySelectorAll('*').forEach((el) => {
      el.style.animationPlayState = state;
    });
  } catch (_) {}
}

function prevScene() {
  loadScene(currentIndex > 0 ? currentIndex - 1 : 0);
}

function nextScene() {
  const nextIndex = currentIndex < sceneConfig.length - 1 ? currentIndex + 1 : 0;
  loadScene(nextIndex);
}

function toggleMusic() {
  isMuted = !isMuted;
  muteIcon.style.display = isMuted ? 'block' : 'none';
  soundIcon.style.display = isMuted ? 'none' : 'block';
  musicBtn.classList.toggle('muted', isMuted);

  if (isMuted) {
    bgMusic.pause();
  } else if (isPlaying) {
    bgMusic.play().catch(() => {});
  }
}

document.addEventListener('DOMContentLoaded', init);

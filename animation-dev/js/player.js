// player.js - 播放器協調控制邏輯

// 場景清單設定 (路徑、名稱、與備用預期播放毫秒數)
const sceneConfig = [
  { url: 'scenes/scene1.html', name: '第 1 幕：你是否也聽過  ...', duration: 5500 },
  { url: 'scenes/scene2.html', name: '第 2 幕：但我不這麼認為', duration: 4000 },
  { url: 'scenes/scene3.html', name: '第 3 幕：我相信每個時代的...', duration: 7000 },
  { url: 'scenes/scene4.html', name: '第 4 幕：我們熟悉的教育樣...', duration: 5500 },
  { url: 'scenes/scene5.html', name: '第 5 幕：它曾經回應那個時...', duration: 5500 },
  { url: 'scenes/scene6.html', name: '第 6 幕：但我們距離工業時...', duration: 5500 },
  { url: 'scenes/scene7.html', name: '第 7 幕：以前的成功學常說...', duration: 5500 },
  { url: 'scenes/scene8.html', name: '第 8 幕：但現代腦科學提醒...', duration: 5500 },
  { url: 'scenes/scene9.html', name: '第 9 幕：每個人吸收知識的...', duration: 5500 },
  { url: 'scenes/scene10.html', name: '第 10 幕：可是在教育現場 ...', duration: 5500 },
  { url: 'scenes/scene11.html', name: '第 11 幕：老師們已經很努力...', duration: 5500 },
  { url: 'scenes/scene12.html', name: '第 12 幕：只是要同時顧進度...', duration: 5500 },
  { url: 'scenes/scene13.html', name: '第 13 幕：自我決定論提到 ...', duration: 5500 },
  { url: 'scenes/scene14.html', name: '第 14 幕：自主感  我想怎...', duration: 5500 },
  { url: 'scenes/scene15.html', name: '第 15 幕：勝任感  在還沒...', duration: 5500 },
  { url: 'scenes/scene16.html', name: '第 16 幕：歸屬感  我挫折...', duration: 5500 },
  { url: 'scenes/scene17.html', name: '第 17 幕：AI 能夠配合孩...', duration: 5500 },
  { url: 'scenes/scene18.html', name: '第 18 幕：有了更多選擇  ...', duration: 5500 },
  { url: 'scenes/scene19.html', name: '第 19 幕：AI 能夠拆解步...', duration: 5500 },
  { url: 'scenes/scene20.html', name: '第 20 幕：隨時想問就問沒有...', duration: 5500 },
  { url: 'scenes/scene21.html', name: '第 21 幕：孩子漸漸得到勝任...', duration: 4000 },
  { url: 'scenes/scene22.html', name: '第 22 幕：而前面兩項都被滿...', duration: 5500 },
  { url: 'scenes/scene23.html', name: '第 23 幕：也有餘裕照顧孩子...', duration: 4000 },
  { url: 'scenes/scene24.html', name: '第 24 幕：因此孩子有了最重...', duration: 4000 },
  { url: 'scenes/scene25.html', name: '第 25 幕：所以孩子不是學不...', duration: 5500 },
  { url: 'scenes/scene26.html', name: '第 26 幕：讓我們一起陪孩子...', duration: 7000 }
];

let currentIndex = 0;
let isPlaying = true;
let isMuted = true;
let timer = null;
let startTime = 0;
let elapsed = 0; // 當前場景已播放時間
let duration = sceneConfig[0].duration;

const iframe = document.getElementById('scene-frame');
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

// 初始化
function init() {
  loadScene(0);

  // 監聽按鈕事件
  playBtn.addEventListener('click', togglePlay);
  prevBtn.addEventListener('click', prevScene);
  nextBtn.addEventListener('click', nextScene);
  musicBtn.addEventListener('click', toggleMusic);

  // 監聽來自 Iframe 分幕的動畫播畢事件
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SCENE_COMPLETE') {
      console.log(`收到 Iframe 通知：第 ${currentIndex + 1} 幕播放完畢`);
      // 切換下一幕
      nextScene();
    }
  });
}

// 載入指定場景
function loadScene(index) {
  if (index < 0 || index >= sceneConfig.length) return;
  
  currentIndex = index;
  duration = sceneConfig[currentIndex].duration;
  elapsed = 0;
  
  // 更新狀態文字
  indicator.textContent = `${sceneConfig[currentIndex].name} (${currentIndex + 1}/${sceneConfig.length})`;
  
  // 更新 iframe 網址
  iframe.src = sceneConfig[currentIndex].url;
  
  // 重設進度條與定時器
  progress.style.width = '0%';
  resetTimer();
  
  if (isPlaying) {
    startTimer();
  }
}

// 計時器邏輯：驅動進度條與備用切換
function startTimer() {
  startTime = Date.now() - elapsed;
  
  function updateProgress() {
    if (!isPlaying) return;
    
    elapsed = Date.now() - startTime;
    const percent = Math.min((elapsed / duration) * 100, 100);
    progress.style.width = `${percent}%`;
    
    if (elapsed >= duration) {
      nextScene(); // 時間到，切換至下一幕
    } else {
      timer = requestAnimationFrame(updateProgress);
    }
  }
  
  timer = requestAnimationFrame(updateProgress);
}

function resetTimer() {
  if (timer) {
    cancelAnimationFrame(timer);
    timer = null;
  }
}

// 播放 / 暫停 切換
function togglePlay() {
  if (isPlaying) {
    isPlaying = false;
    resetTimer();
    playIcon.style.display = 'block';
    pauseIcon.style.display = 'none';
    setIframePlayState('paused');
    if (!isMuted) bgMusic.pause();
  } else {
    isPlaying = true;
    playIcon.style.display = 'none';
    pauseIcon.style.display = 'block';
    setIframePlayState('running');
    startTimer();
    if (!isMuted && bgMusic.paused) {
      bgMusic.play().catch(e => console.log('音樂自動播放失敗：', e));
    }
  }
}

// 控制 Iframe 內部 CSS 動畫播放狀態
function setIframePlayState(state) {
  try {
    const iframeBody = iframe.contentDocument || iframe.contentWindow.document;
    if (iframeBody && iframeBody.body) {
      iframeBody.body.style.setProperty('--play-state', state);
      // 對所有元素套用 play state
      const elements = iframeBody.body.querySelectorAll('*');
      elements.forEach(el => {
        el.style.animationPlayState = state;
      });
    }
  } catch (err) {
    console.log('無法控制 Iframe 內動畫狀態 (跨域或尚未加載)：', err);
  }
}

// 當 Iframe 加載完成，確保其動畫狀態與主播放器一致
iframe.addEventListener('load', () => {
  setIframePlayState(isPlaying ? 'running' : 'paused');
});

// 切換至上一幕
function prevScene() {
  if (currentIndex > 0) {
    loadScene(currentIndex - 1);
  } else {
    // 若在第一幕，重頭播放
    loadScene(0);
  }
}

// 切換至下一幕 (若為最後一幕則循環播放)
function nextScene() {
  resetTimer();
  if (currentIndex < sceneConfig.length - 1) {
    loadScene(currentIndex + 1);
  } else {
    // 循環回第一幕
    loadScene(0);
  }
}

// 音樂開關
function toggleMusic() {
  if (isMuted) {
    isMuted = false;
    muteIcon.style.display = 'none';
    soundIcon.style.display = 'block';
    musicBtn.classList.remove('muted');
    if (isPlaying) {
      bgMusic.play().catch(e => {
        console.log('瀏覽器阻擋自動播放音樂：', e);
        // 使用者互動後才可播放，在此提醒
      });
    }
  } else {
    isMuted = true;
    muteIcon.style.display = 'block';
    soundIcon.style.display = 'none';
    musicBtn.classList.add('muted');
    bgMusic.pause();
  }
}

// 初始化啟動
document.addEventListener('DOMContentLoaded', init);

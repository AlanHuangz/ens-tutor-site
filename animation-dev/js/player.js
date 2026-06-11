// player.js - 播放器協調控制邏輯

// 場景清單設定 (路徑、名稱、與備用預期播放毫秒數)
const sceneConfig = [
  { url: 'scenes/scene1.html', name: '第 1 幕：你是否也常聽人說...', duration: 5500 },
  { url: 'scenes/scene2.html', name: '第 2 幕：但我並不這麼認為', duration: 4000 },
  { url: 'scenes/scene3.html', name: '第 3 幕：我相信每個時代的...', duration: 7000 },
  { url: 'scenes/scene4.html', name: '第 4 幕：我們現在熟悉的教...', duration: 5500 },
  { url: 'scenes/scene5.html', name: '第 5 幕：那時候的教育  ...', duration: 5500 },
  { url: 'scenes/scene6.html', name: '第 6 幕：但我們距離工業時...', duration: 4000 },
  { url: 'scenes/scene7.html', name: '第 7 幕：當科技快速前進 ...', duration: 5500 },
  { url: 'scenes/scene8.html', name: '第 8 幕：以前的成功學常說...', duration: 5500 },
  { url: 'scenes/scene9.html', name: '第 9 幕：但現代腦科學提醒...', duration: 5500 },
  { url: 'scenes/scene10.html', name: '第 10 幕：每個人吸收知識的...', duration: 5500 },
  { url: 'scenes/scene11.html', name: '第 11 幕：但在體制內的教育...', duration: 5500 },
  { url: 'scenes/scene12.html', name: '第 12 幕：老師們已經非常努...', duration: 5500 },
  { url: 'scenes/scene13.html', name: '第 13 幕：只是要同時顧進度...', duration: 4000 },
  { url: 'scenes/scene14.html', name: '第 14 幕：還要為每個孩子量...', duration: 5500 },
  { url: 'scenes/scene15.html', name: '第 15 幕：心理學的自我決定...', duration: 5500 },
  { url: 'scenes/scene16.html', name: '第 16 幕：第一是自主感  ...', duration: 5500 },
  { url: 'scenes/scene17.html', name: '第 17 幕：第二是勝任感  ...', duration: 5500 },
  { url: 'scenes/scene18.html', name: '第 18 幕：第三是歸屬感  ...', duration: 7000 },
  { url: 'scenes/scene19.html', name: '第 19 幕：現在AI 能夠完...', duration: 4000 },
  { url: 'scenes/scene20.html', name: '第 20 幕：不管是圖像影像還...', duration: 5500 },
  { url: 'scenes/scene21.html', name: '第 21 幕：有了選擇權  孩...', duration: 5500 },
  { url: 'scenes/scene22.html', name: '第 22 幕：AI 可以耐心拆...', duration: 5500 },
  { url: 'scenes/scene23.html', name: '第 23 幕：孩子再也不用擔心...', duration: 5500 },
  { url: 'scenes/scene24.html', name: '第 24 幕：隨時想問就問沒有...', duration: 4000 },
  { url: 'scenes/scene25.html', name: '第 25 幕：只要給予足夠的時...', duration: 5500 },
  { url: 'scenes/scene26.html', name: '第 26 幕：這樣孩子的勝任感...', duration: 4000 },
  { url: 'scenes/scene27.html', name: '第 27 幕：當孩子的自主與勝...', duration: 5500 },
  { url: 'scenes/scene28.html', name: '第 28 幕：有了餘裕  才能...', duration: 5500 },
  { url: 'scenes/scene29.html', name: '第 29 幕：這時孩子最需要的...', duration: 5500 },
  { url: 'scenes/scene30.html', name: '第 30 幕：所以很多時候孩子...', duration: 5500 },
  { url: 'scenes/scene31.html', name: '第 31 幕：讓我們一起陪孩子...', duration: 7000 }
];

let currentIndex = 0;
let isPlaying = true;
let isMuted = true;
let timer = null;
let startTime = 0;
let elapsed = 0; // 當前場景已播放時間
let duration = sceneConfig[0].duration;

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

// 初始化
function init() {
  activeIframe = iframe1;
  inactiveIframe = iframe2;

  // 監聽第一幕 (預設載入) 的完成
  activeIframe.onload = function() {
    setIframePlayState(activeIframe, isPlaying ? 'running' : 'paused');
    activeIframe.onload = null;
    if (isPlaying) {
      startTimer();
    }
  };

  // 更新狀態文字
  indicator.textContent = `${sceneConfig[0].name} (1/${sceneConfig.length})`;

  // 監聽按鈕事件
  playBtn.addEventListener('click', togglePlay);
  prevBtn.addEventListener('click', prevScene);
  nextBtn.addEventListener('click', nextScene);
  musicBtn.addEventListener('click', toggleMusic);

  // 監聽背景音樂加載失敗 (若本地下載未就緒，切換至備用雲端 URL)
  bgMusic.addEventListener('error', () => {
    console.log("本地背景音樂加載失敗或尚未下載完成，切換至雲端備用音訊源...");
    const fallbackUrl = 'https://assets.mixkit.co/music/preview/mixkit-warm-lights-347.mp3';
    if (bgMusic.src !== fallbackUrl) {
      bgMusic.src = fallbackUrl;
      bgMusic.load();
    }
  });

  // 監聽來自 Iframe 分幕的動畫播畢與互動跳轉事件
  window.addEventListener('message', (event) => {
    if (event.data) {
      if (event.data.type === 'SCENE_COMPLETE') {
        // 關鍵安全檢查：只有當前作用中的 iframe 發出的完成訊號才受理，防止舊頁面延遲訊號干擾
        if (event.source === activeIframe.contentWindow) {
          console.log(`收到 Iframe 通知：第 ${currentIndex + 1} 幕播放完畢`);
          nextScene();
        } else {
          console.log(`忽略非作用中 Iframe 的完成訊號`);
        }
      } else if (event.data.type === 'GO_TO_SCENE') {
        if (event.source === activeIframe.contentWindow) {
          console.log(`收到 Iframe 互動跳轉要求，目標索引：${event.data.index}`);
          loadScene(event.data.index);
        }
      }
    }
  });
}

// 載入指定場景 (雙緩衝無縫切換，徹底消除加載時的白閃與停頓)
function loadScene(index) {
  if (index < 0 || index >= sceneConfig.length) return;
  
  const targetUrl = sceneConfig[index].url;
  currentIndex = index;
  duration = sceneConfig[currentIndex].duration;
  elapsed = 0;
  
  // 更新狀態文字
  indicator.textContent = `${sceneConfig[currentIndex].name} (${currentIndex + 1}/${sceneConfig.length})`;
  
  // 重設進度條與定時器
  progress.style.width = '0%';
  resetTimer();
  
  let hasLoaded = false;
  
  // 1. 在背景 iframe 載入目標頁面
  inactiveIframe.onload = function() {
    if (hasLoaded) return;
    hasLoaded = true;
    
    // 確保新 iframe 內部播放狀態與主播放器同步
    setIframePlayState(inactiveIframe, isPlaying ? 'running' : 'paused');
    
    // 2. 進行淡入淡出樣式切換
    activeIframe.className = 'scene-frame incoming';
    inactiveIframe.className = 'scene-frame active';
    
    // 3. 交換雙緩衝指標
    const temp = activeIframe;
    activeIframe = inactiveIframe;
    inactiveIframe = temp;
    
    // 4. 清除舊 onload，並延遲清空 src 避免淡出動畫期間變白
    inactiveIframe.onload = null;
    const oldIframe = inactiveIframe;
    setTimeout(() => {
      if (oldIframe === inactiveIframe) {
        oldIframe.src = 'about:blank';
      }
    }, 500);
    
    // 5. 啟動計時器
    if (isPlaying) {
      startTimer();
    }
  };
  
  // 設置 3 秒超時保護，防範加載異常導致卡屏
  const timeoutId = setTimeout(() => {
    if (!hasLoaded) {
      console.warn("Iframe 加載超合，強制切換幕");
      inactiveIframe.onload();
    }
  }, 3000);
  
  // 觸發載入
  inactiveIframe.src = targetUrl;
}

// 計時器邏輯：驅動進度條與備用切換
function startTimer() {
  startTime = Date.now() - elapsed;
  
  function updateProgress() {
    if (!isPlaying) return;
    
    // 如果處於互動模式（如卡片展開或充電中），凍結進度條並不進行自動換幕
    const isInteractiveMode = sessionStorage.getItem('is_interactive_mode') === 'true';
    if (isInteractiveMode) {
      startTime = Date.now() - elapsed; // 不斷更新起始點，避免時間累積
      timer = requestAnimationFrame(updateProgress);
      return;
    }
    
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
    setIframePlayState(activeIframe, 'paused');
    if (!isMuted) bgMusic.pause();
  } else {
    isPlaying = true;
    playIcon.style.display = 'none';
    pauseIcon.style.display = 'block';
    setIframePlayState(activeIframe, 'running');
    startTimer();
    if (!isMuted && bgMusic.paused) {
      bgMusic.play().catch(e => console.log('音樂自動播放失敗：', e));
    }
  }
}

// 控制 Iframe 內部 CSS 動畫播放狀態
function setIframePlayState(targetIframe, state) {
  try {
    const iframeBody = targetIframe.contentDocument || targetIframe.contentWindow.document;
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

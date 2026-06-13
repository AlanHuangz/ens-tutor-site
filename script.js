// 願意學 — 網站互動與報名邏輯 (v4.0)

// Helper function
function query(selector) {
  return document.querySelector(selector);
}

// 1. Header 手機版選單切換與頁尾年份
function initCommonLayout() {
  const header = query(".site-header");
  const toggle = query(".nav-toggle");
  const year = query("#year");

  if (year) {
    year.textContent = new Date().getFullYear();
  }

  if (toggle && header) {
    toggle.addEventListener("click", () => {
      const isOpen = header.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
    });
  }

  // 點擊選單外部時收合選單
  document.addEventListener("click", (event) => {
    if (!header || !header.classList.contains("nav-open")) return;
    if (!event.target.closest(".site-header")) {
      header.classList.remove("nav-open");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
    }
  });

  // 滾動時增加 Header 陰影
  window.addEventListener("scroll", () => {
    if (header) {
      header.classList.toggle("is-scrolled", window.scrollY > 24);
    }
  }, { passive: true });
}

// 2. 報名表單提交處理 (booking.html)
function initBookingForm() {
  const signupForm = query("#signupForm");
  const formPanel = query("#formPanel");
  const successPanel = query("#successPanel");
  const successSummaryContent = query("#successSummaryContent");

  if (!signupForm || !formPanel || !successPanel) return;

  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    // 取得所有勾選的時段
    const checkedSlots = Array.from(document.querySelectorAll('input[name="slots"]:checked'))
      .map(cb => cb.value);

    if (checkedSlots.length === 0) {
      alert("請至少選擇一個您可以配合的候選時段喔！");
      return;
    }

    const parentName = query("#parentName").value.trim();
    const contactInfo = query("#contactInfo").value.trim();
    const studentName = query("#studentName").value.trim();
    const studentLevel = query("#studentLevel").value;
    const lessonLocationType = query("#lessonLocationType").value;
    const lessonType = query("#lessonType").value;
    const lessonAddress = query("#lessonAddress").value.trim();
    const timeNote = query("#timeNote").value.trim();
    const learningNeed = query("#learningNeed").value.trim();
    const parentExpectation = query("#parentExpectation").value.trim();

    // 組裝 Inquiry API 所需的 payload
    const payload = {
      studentName: studentName,
      studentLevel: studentLevel,
      lessonType: lessonType,
      contactInfo: `家長稱呼: ${parentName} / 聯絡方式: ${contactInfo}`,
      learningNeed: learningNeed || "無特別補充",
      parentExpectation: parentExpectation || "無特別補充",
      lessonLocationType: lessonLocationType,
      lessonAddress: lessonAddress || "線上 (免填)",
      slots: checkedSlots,
      note: timeNote || ""
    };

    // 顯示載入中狀態
    const submitBtn = signupForm.querySelector(".submit-btn");
    const originalBtnText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = "正在送出報名資料...";

    try {
      const response = await fetch("/api/inquiries", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("伺服器回應錯誤，請稍後再試。");
      }

      const result = await response.json();

      // 隱藏表單面板，顯示成功面板
      formPanel.style.display = "none";
      successPanel.style.display = "block";

      // 渲染摘要內容
      const slotsText = checkedSlots.join("、");
      successSummaryContent.innerHTML = `
        <p><strong>家長稱呼：</strong> ${parentName}</p>
        <p><strong>聯絡方式：</strong> ${contactInfo}</p>
        <p><strong>孩子姓名/年級：</strong> ${studentName} (${studentLevel})</p>
        <p><strong>上課方式/安排：</strong> ${lessonLocationType} / ${lessonType}</p>
        <p><strong>上課地點：</strong> ${lessonAddress || "線上"}</p>
        <p><strong>候選時段：</strong> ${slotsText}</p>
        ${timeNote ? `<p><strong>時段備註：</strong> ${timeNote}</p>` : ""}
      `;

      // 滾動到成功面板頂部
      successPanel.scrollIntoView({ behavior: "smooth", block: "center" });

    } catch (error) {
      alert(`暫時無法送出報名資料，請透過官方 LINE 直接與我聯繫：${error.message}`);
      submitBtn.disabled = false;
      submitBtn.textContent = originalBtnText;
    }
  });
}

// ==========================================
// 願意學前哨影片網頁播放器邏輯 (Ken Burns & HTML 字幕)
// ==========================================

const introScenes = [
  {
    id: 1,
    start: 0.0,
    end: 5.0,
    image: "assets/images/scene01.png",
    motion: "slow-zoom-in",
    captionPosition: "left-center"
  },
  {
    id: 2,
    start: 5.0,
    end: 10.5,
    image: "assets/images/scene02.png",
    motion: "slow-zoom-in",
    captionPosition: "left-bottom"
  },
  {
    id: 3,
    start: 10.5,
    end: 16.0,
    image: "assets/images/scene03.png",
    motion: "slow-pan-right",
    captionPosition: "right-center"
  },
  {
    id: 4,
    start: 16.0,
    end: 21.5,
    image: "assets/images/scene04.png",
    motion: "slow-zoom-out",
    captionPosition: "left-center"
  },
  {
    id: 5,
    start: 21.5,
    end: 27.5,
    image: "assets/images/scene05.png",
    motion: "still-breathe",
    captionPosition: "left-center"
  },
  {
    id: 6,
    start: 27.5,
    end: 32.0,
    image: "assets/images/scene06.png",
    motion: "slow-zoom-in",
    captionPosition: "left-center"
  },
  {
    id: 7,
    start: 32.0,
    end: 36.5,
    image: "assets/images/scene07.png",
    motion: "slow-zoom-in",
    captionPosition: "right-center"
  },
  {
    id: 8,
    start: 36.5,
    end: 41.5,
    image: "assets/images/scene08.png",
    motion: "slow-pan-left",
    captionPosition: "left-center"
  },
  {
    id: 9,
    start: 41.5,
    end: 47.0,
    image: "assets/images/scene09.png",
    motion: "slow-zoom-in",
    captionPosition: "left-bottom"
  },
  {
    id: 10,
    start: 47.0,
    end: 52.0,
    image: "assets/images/scene10.png",
    motion: "still-breathe",
    captionPosition: "left-center"
  }
];

const introCaptions = [
  {
    scene: 1,
    lines: [
      { text: "大人常說", at: 0.8 },
      { text: "都是手機害的", at: 2.0 }
    ]
  },
  {
    scene: 2,
    lines: [
      { text: "可那裡，", at: 5.8 },
      { text: "有時只是他的避難所", at: 7.2 }
    ]
  },
  {
    scene: 3,
    lines: [
      { text: "一回到題目，", at: 11.4 },
      { text: "他又想起自己不會", at: 12.8 }
    ]
  },
  {
    scene: 4,
    lines: [
      { text: "不是他不想學，", at: 16.9 },
      { text: "是他跟不上了", at: 18.2 }
    ]
  },
  {
    scene: 5,
    lines: [
      { text: "我們很少問，", at: 22.5 },
      { text: "他是怎麼放棄的", at: 24.0 }
    ]
  },
  {
    scene: 6,
    lines: [
      { text: "聽不懂的時候，", at: 28.2 },
      { text: "他只能撐著", at: 29.4 }
    ]
  },
  {
    scene: 7,
    lines: [
      { text: "錯太多次，", at: 32.7 },
      { text: "連開始都會怕", at: 33.9 }
    ]
  },
  {
    scene: 8,
    lines: [
      { text: "大人越急，", at: 37.3 },
      { text: "他越不敢說不會", at: 38.6 }
    ]
  },
  {
    scene: 9,
    lines: [
      { text: "先陪他看懂一小步", at: 42.3 }
    ]
  },
  {
    scene: 10,
    lines: [
      { text: "願意學", at: 47.8 },
      { text: "先懂孩子，再懂數學", at: 49.2 }
    ]
  }
];

function initIntroVideoPlayer() {
  const TOTAL_DURATION = 52.0;
  
  // Elements
  const scenesContainer = query('#scenesContainer');
  const captionContainer = query('#captionContainer');
  const playBtn = query('#playBtn');
  const iconPlay = query('#iconPlay');
  const iconPause = query('#iconPause');
  const iconReplay = query('#iconReplay');
  const timeDisplay = query('#timeDisplay');
  const progressBar = query('#progressBar');
  const progressContainer = query('#progressContainer');
  const bigPlayOverlay = query('#bigPlayOverlay');
  const bgm = query('#bgm');
  
  if (!scenesContainer || !captionContainer) return;

  // State
  let isPlaying = false;
  let currentTime = 0;
  let lastTimestamp = 0;
  let animationFrameId = null;
  let currentSceneId = null;

  // Initialize Scenes
  function initScenes() {
    scenesContainer.innerHTML = '';
    introScenes.forEach(scene => {
      const sceneEl = document.createElement('div');
      sceneEl.className = `scene motion-${scene.motion}`;
      sceneEl.id = `scene-${scene.id}`;
      
      const img = document.createElement('img');
      img.src = scene.image;
      img.alt = `Scene ${scene.id}`;
      
      sceneEl.appendChild(img);
      scenesContainer.appendChild(sceneEl);
    });
  }

  // Format time (s -> m:ss)
  function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  }

  function updateUI() {
    // Update progress bar & time
    const progressPercent = Math.min((currentTime / TOTAL_DURATION) * 100, 100);
    if (progressBar) progressBar.style.width = `${progressPercent}%`;
    if (timeDisplay) timeDisplay.textContent = formatTime(currentTime);

    // Determine current scene
    const activeScene = introScenes.find(s => currentTime >= s.start && currentTime < s.end);
    
    if (activeScene) {
      if (currentSceneId !== activeScene.id) {
        // Scene changed
        // 1. Hide all scenes
        scenesContainer.querySelectorAll('.scene').forEach(el => el.classList.remove('active'));
        // 2. Show new scene
        const newSceneEl = document.getElementById(`scene-${activeScene.id}`);
        if (newSceneEl) newSceneEl.classList.add('active');
        
        // 3. Setup captions for the new scene
        currentSceneId = activeScene.id;
        captionContainer.className = `caption ${activeScene.captionPosition}`;
        
        const sceneCaption = introCaptions.find(c => c.scene === activeScene.id);
        captionContainer.innerHTML = ''; // Clear previous
        
        if (sceneCaption) {
          sceneCaption.lines.forEach((line, index) => {
            const lineEl = document.createElement('div');
            lineEl.className = 'caption-line';
            lineEl.id = `caption-${activeScene.id}-line-${index}`;
            lineEl.textContent = line.text;
            lineEl.dataset.at = line.at;
            captionContainer.appendChild(lineEl);
          });
        }
      }

      // Update captions visibility
      const lineEls = captionContainer.querySelectorAll('.caption-line');
      lineEls.forEach(el => {
        const atTime = parseFloat(el.dataset.at);
        if (currentTime >= atTime) {
          el.classList.add('show');
        } else {
          el.classList.remove('show');
        }
      });
    } else if (currentTime >= TOTAL_DURATION) {
      // End of video
      pause();
      currentTime = TOTAL_DURATION;
      if (progressBar) progressBar.style.width = '100%';
      if (timeDisplay) timeDisplay.textContent = formatTime(currentTime);
      if (iconPause) iconPause.style.display = 'none';
      if (iconPlay) iconPlay.style.display = 'none';
      if (iconReplay) iconReplay.style.display = 'block';
    }
  }

  // Loop
  function loop(timestamp) {
    if (!lastTimestamp) lastTimestamp = timestamp;
    const deltaTime = (timestamp - lastTimestamp) / 1000;
    lastTimestamp = timestamp;

    if (isPlaying) {
      currentTime += deltaTime;
      if (currentTime > TOTAL_DURATION) {
        currentTime = TOTAL_DURATION;
      }
      updateUI();
    }

    if (isPlaying) {
      animationFrameId = requestAnimationFrame(loop);
    }
  }

  function play() {
    if (currentTime >= TOTAL_DURATION) {
      currentTime = 0;
      currentSceneId = null;
    }
    isPlaying = true;
    lastTimestamp = 0;
    
    if (iconPlay) iconPlay.style.display = 'none';
    if (iconReplay) iconReplay.style.display = 'none';
    if (iconPause) iconPause.style.display = 'block';
    if (bigPlayOverlay) bigPlayOverlay.classList.add('hidden');
    
    if (bgm) {
      bgm.play().catch(err => {
        console.log("Audio play blocked by browser policy: ", err);
      });
    }

    animationFrameId = requestAnimationFrame(loop);
  }

  function pause() {
    isPlaying = false;
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
    }
    if (iconPause) iconPause.style.display = 'none';
    if (iconReplay) iconReplay.style.display = 'none';
    if (iconPlay) iconPlay.style.display = 'block';
    if (bigPlayOverlay) bigPlayOverlay.classList.remove('hidden');
    
    if (bgm) {
      bgm.pause();
    }
  }

  function togglePlay() {
    if (isPlaying) {
      pause();
    } else {
      play();
    }
  }

  // Seek functionality
  if (progressContainer) {
    progressContainer.addEventListener('click', (e) => {
      const rect = progressContainer.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const newPercent = clickX / rect.width;
      currentTime = newPercent * TOTAL_DURATION;
      
      if (currentTime >= TOTAL_DURATION) currentTime = TOTAL_DURATION - 0.1;
      if (currentTime < 0) currentTime = 0;
      
      currentSceneId = null; 
      updateUI();
      
      if (bgm && !isNaN(bgm.duration)) {
        bgm.currentTime = currentTime;
      }
      
      if (currentTime < TOTAL_DURATION && !isPlaying) {
        if (iconPlay) iconPlay.style.display = 'block';
        if (iconReplay) iconReplay.style.display = 'none';
        if (iconPause) iconPause.style.display = 'none';
      }
    });
  }

  if (playBtn) playBtn.addEventListener('click', togglePlay);
  if (bigPlayOverlay) bigPlayOverlay.addEventListener('click', play);

  // Init
  initScenes();
  updateUI();
}

// 初始化
document.addEventListener("DOMContentLoaded", () => {
  initCommonLayout();
  initBookingForm();
  initIntroVideoPlayer();
});

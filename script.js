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

// 初始化
document.addEventListener("DOMContentLoaded", () => {
  initCommonLayout();
  initBookingForm();
});

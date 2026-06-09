const settingsOutput = document.querySelector("#settingsOutput");
const unavailableList = document.querySelector("#unavailableList");
const inquiryList = document.querySelector("#inquiryList");
const blockForm = document.querySelector("#blockForm");
const replyDraft = document.querySelector("#replyDraft");

let appState = {
  settings: {},
  unavailable: [],
  inquiries: [],
};

function formatDateTime(value) {
  if (!value) return "未記錄";
  return new Intl.DateTimeFormat("zh-TW", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function statusLabel(status) {
  const labels = {
    new: "新諮詢",
    contacted: "已回覆",
    confirmed: "已確認",
    waitlist: "候補",
    declined: "無法安排",
  };
  return labels[status] || status || "新諮詢";
}

function mapSearchUrl(address) {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`;
}

function renderSettings() {
  const settings = appState.settings || {};
  const items = [
    ["開始授課", settings.availableFrom || "2026-07-01"],
    ["授課對象", settings.audience || "國小、國中"],
    ["正式課", `${settings.lessonMinutes || 90} 分鐘 / ${settings.regularPrice || 1200} 元`],
    ["初次體驗", `${settings.trialPrice || 800} 元，${settings.trialLimit || "限一次"}`],
  ];

  settingsOutput.innerHTML = items
    .map(
      ([label, value]) => `
        <div class="status-item">
          <span>${label}</span>
          <strong>${value}</strong>
        </div>
      `
    )
    .join("");
}

function renderUnavailable() {
  if (!appState.unavailable.length) {
    unavailableList.innerHTML = '<div class="list-item"><p>目前沒有標記不可預約時段。</p></div>';
    return;
  }

  unavailableList.innerHTML = appState.unavailable
    .map(
      (item) => `
        <div class="list-item">
          <div>
            <strong>${item.date} ${item.time}</strong>
            <p>${item.reason}</p>
          </div>
          <button class="button ghost" type="button" data-delete-block="${item.id}">移除</button>
        </div>
      `
    )
    .join("");
}

function renderInquiries() {
  if (!appState.inquiries.length) {
    inquiryList.innerHTML = '<div class="inquiry-card"><p>目前還沒有家長送出預約。</p></div>';
    return;
  }

  inquiryList.innerHTML = appState.inquiries
    .map((item) => {
      const slots = item.slots && item.slots.length ? item.slots : ["尚未選擇"];
      return `
        <article class="inquiry-card">
          <div>
            <h3>${item.studentName || "未填姓名"}</h3>
            <p>${formatDateTime(item.createdAt)}</p>
          </div>
          <div class="inquiry-meta">
            <span class="pill">${item.studentLevel || "未填年級"}</span>
            <span class="pill">${statusLabel(item.status)}</span>
          </div>
          <p><strong>需求：</strong>${item.lessonType || "未填寫"}</p>
          <p><strong>聯絡：</strong>${item.contactInfo || "未填寫"}</p>
          <p><strong>上課方式：</strong>${item.lessonLocationType || "未填寫"}</p>
          <p><strong>約略地點：</strong>${item.lessonAddress || "未提供"}</p>
          <p><strong>孩子狀況：</strong>${item.learningNeed || "未補充"}</p>
          <p><strong>家長補充：</strong>${item.parentExpectation || "未補充"}</p>
          <div>
            <strong>候選時段</strong>
            <ul class="slot-list">
              ${slots.map((slot) => `<li>${slot}</li>`).join("")}
            </ul>
          </div>
          <div class="card-actions">
            <button class="button primary" type="button" data-reply="${item.id}" data-reply-status="available">一般回覆</button>
            <button class="button ghost" type="button" data-reply="${item.id}" data-reply-status="conflict">撞期回覆</button>
            <button class="button ghost" type="button" data-status="${item.id}" data-next-status="contacted">標記已回覆</button>
            <button class="button ghost" type="button" data-status="${item.id}" data-next-status="confirmed">標記已確認</button>
            ${
              item.lessonAddress
                ? `<a class="button ghost" href="${mapSearchUrl(item.lessonAddress)}" target="_blank" rel="noreferrer">開 Google Maps</a>`
                : ""
            }
            <button class="button ghost" type="button" data-delete-inquiry="${item.id}">刪除</button>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderArticles() {
  const articleList = document.querySelector("#articleList");
  if (!articleList) return;
  if (!appState.articles || !appState.articles.length) {
    articleList.innerHTML = '<div class="list-item"><p>目前沒有已發佈的文章。</p></div>';
    return;
  }

  articleList.innerHTML = appState.articles
    .map(
      (art) => `
        <div class="list-item" style="border-left: 4px solid var(--teal, #0d7c75); padding-left: 12px; margin-bottom: 12px;">
          <div style="flex: 1;">
            <strong style="font-size: 1.15rem; display: block; color: var(--ink);">${art.title}</strong>
            <span style="font-size: 0.8rem; color: var(--muted);">${formatDateTime(art.createdAt)}</span>
            <p style="margin: 6px 0; font-size: 0.95rem; color: var(--muted);">${art.summary}</p>
            <div style="margin-top: 4px;">
              ${(art.tags || []).map(t => `<span class="pill" style="font-size: 0.75rem; margin-right: 4px; background: rgba(45, 90, 86, 0.1); color: var(--teal, #2d5a56); padding: 2px 8px; border-radius: 4px;">${t}</span>`).join("")}
            </div>
          </div>
          <button class="button ghost" type="button" data-delete-article="${art.id}" style="color: #c62828; border-color: rgba(198, 40, 40, 0.2); margin-left: 16px;">刪除</button>
        </div>
      `
    )
    .join("");
}

function render() {
  renderSettings();
  renderUnavailable();
  renderInquiries();
  renderArticles();
}

async function loadState() {
  const response = await fetch("/api/state");
  appState = await response.json();
  render();
}

async function addUnavailable(event) {
  event.preventDefault();
  const payload = {
    date: document.querySelector("#blockDate").value,
    time: document.querySelector("#blockTime").value,
    reason: document.querySelector("#blockReason").value.trim(),
  };

  const response = await fetch("/api/unavailable", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (response.ok) {
    blockForm.reset();
    await loadState();
  }
}

async function deleteUnavailable(id) {
  await fetch(`/api/unavailable/${encodeURIComponent(id)}`, { method: "DELETE" });
  await loadState();
}

async function updateInquiryStatus(id, status) {
  await fetch(`/api/inquiries/${encodeURIComponent(id)}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  await loadState();
}

async function deleteInquiry(id) {
  await fetch(`/api/inquiries/${encodeURIComponent(id)}`, { method: "DELETE" });
  await loadState();
}

async function deleteArticle(id) {
  await fetch(`/api/articles/${encodeURIComponent(id)}`, { method: "DELETE" });
  await loadState();
}

async function createReply(id, status) {
  const response = await fetch("/api/assistant/reply", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ inquiryId: id, status }),
  });
  const result = await response.json();
  replyDraft.value = result.reply || "";
  replyDraft.focus();
}

blockForm.addEventListener("submit", addUnavailable);

const articleForm = document.querySelector("#articleForm");
if (articleForm) {
  articleForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = document.querySelector("#articleTitle").value.trim();
    const tagsInput = document.querySelector("#articleTags").value.trim();
    const summary = document.querySelector("#articleSummary").value.trim();
    const content = document.querySelector("#articleContent").value.trim();
    const tags = tagsInput ? tagsInput.split(",").map(t => t.trim()).filter(Boolean) : [];

    const response = await fetch("/api/articles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, tags, summary, content }),
    });

    if (response.ok) {
      articleForm.reset();
      await loadState();
    }
  });
}

document.querySelector("#refreshData").addEventListener("click", loadState);

document.addEventListener("click", async (event) => {
  const deleteId = event.target.dataset.deleteBlock;
  const deleteInquiryId = event.target.dataset.deleteInquiry;
  const deleteArticleId = event.target.dataset.deleteArticle;
  const statusId = event.target.dataset.status;
  const replyId = event.target.dataset.reply;

  if (deleteId) {
    await deleteUnavailable(deleteId);
  }

  if (deleteInquiryId) {
    await deleteInquiry(deleteInquiryId);
  }

  if (deleteArticleId) {
    if (confirm("確定要刪除這篇文章嗎？")) {
      await deleteArticle(deleteArticleId);
    }
  }

  if (statusId) {
    await updateInquiryStatus(statusId, event.target.dataset.nextStatus);
  }

  if (replyId) {
    await createReply(replyId, event.target.dataset.replyStatus);
  }
});

document.querySelector("#copyReply").addEventListener("click", async () => {
  if (!replyDraft.value.trim()) return;
  await navigator.clipboard.writeText(replyDraft.value);
});

loadState();

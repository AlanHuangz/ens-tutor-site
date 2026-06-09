const http = require("http");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const dataDir = process.env.DATA_DIR || root;
const dataFile = path.join(dataDir, "data.json");
const port = Number(process.env.PORT || 5173);
const host = process.env.HOST || "0.0.0.0";
const adminUser = process.env.ADMIN_USER || "admin";
const adminPassword = process.env.ADMIN_PASSWORD || "change-this-password";
const displayHost = host === "0.0.0.0" ? "your-computer-ip" : host;
const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".mp4": "video/mp4",
};

const defaultData = {
  settings: {
    availableFrom: "2026-07-01",
    lessonMinutes: 90,
    regularPrice: 1200,
    trialPrice: 800,
    trialLimit: "限一次",
    audience: "國小、國中",
    note: "七月起開放少量家庭陪伴名額，目前可先提出候選時段與孩子狀態；家長聯繫以官方 LINE 為主，實際安排需二次確認。",
  },
  unavailable: [],
  inquiries: [],
};

function ensureDataFile() {
  fs.mkdirSync(dataDir, { recursive: true });
  if (!fs.existsSync(dataFile)) {
    fs.writeFileSync(dataFile, JSON.stringify(defaultData, null, 2), "utf8");
  }
}

function readData() {
  ensureDataFile();
  return JSON.parse(fs.readFileSync(dataFile, "utf8"));
}

function writeData(data) {
  fs.writeFileSync(dataFile, JSON.stringify(data, null, 2), "utf8");
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload));
}

function isAdminRequest(request) {
  const header = request.headers.authorization || "";
  if (!header.startsWith("Basic ")) return false;
  const credentials = Buffer.from(header.slice(6), "base64").toString("utf8");
  return credentials === `${adminUser}:${adminPassword}`;
}

function requireAdmin(request, response) {
  if (isAdminRequest(request)) return true;
  response.writeHead(401, {
    "WWW-Authenticate": 'Basic realm="Tutor Admin"',
    "Content-Type": "text/plain; charset=utf-8",
  });
  response.end("Admin login required");
  return false;
}

function readBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.on("data", (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) {
        reject(new Error("Request body too large"));
        request.destroy();
      }
    });
    request.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(error);
      }
    });
    request.on("error", reject);
  });
}

function createId(prefix) {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

function generateReply(inquiry, status = "available") {
  const name = inquiry.studentName || "孩子";
  const slots = (inquiry.slots || []).length ? inquiry.slots.join("、") : "您方便的時段";
  const grade = inquiry.studentLevel || "目前年級";
  const location = inquiry.lessonAddress ? `，上課地點為「${inquiry.lessonAddress}」` : "";
  const expectation = inquiry.parentExpectation ? `\n\n您補充的孩子狀態：「${inquiry.parentExpectation}」，我會一併評估考量。` : "";

  return `您好，已收到您對 ${name}（${grade}）的「願意學」自學陪伴申請！\n\n您選擇的時段為「${slots}」${location}。我會儘快評估交通與行程安排，並透過您留下的聯絡資訊與您聯繫確認。${expectation}`;
}

async function handleApi(request, response, requestUrl) {
  const data = readData();



  if (request.method === "GET" && requestUrl.pathname === "/api/public-state") {
    sendJson(response, 200, {
      settings: data.settings,
      unavailable: data.unavailable,
    });
    return true;
  }

  if (request.method === "GET" && requestUrl.pathname === "/api/state") {
    if (!requireAdmin(request, response)) return true;
    sendJson(response, 200, data);
    return true;
  }

  if (request.method === "POST" && requestUrl.pathname === "/api/inquiries") {
    const payload = await readBody(request);
    const inquiry = {
      id: createId("inq"),
      createdAt: new Date().toISOString(),
      status: "new",
      studentName: payload.studentName || "",
      studentLevel: payload.studentLevel || "",
      learningNeed: payload.learningNeed || "",
      parentExpectation: payload.parentExpectation || "",
      contactInfo: payload.contactInfo || "",
      lessonType: payload.lessonType || "",
      lessonLocationType: payload.lessonLocationType || "",
      lessonAddress: payload.lessonAddress || "",
      slots: Array.isArray(payload.slots) ? payload.slots : [],
      note: payload.note || "",
    };
    data.inquiries.unshift(inquiry);
    writeData(data);
    sendJson(response, 201, { inquiry, reply: generateReply(inquiry, "before-july") });
    return true;
  }

  if (request.method === "PATCH" && requestUrl.pathname.startsWith("/api/inquiries/")) {
    if (!requireAdmin(request, response)) return true;
    const id = decodeURIComponent(requestUrl.pathname.replace("/api/inquiries/", ""));
    const payload = await readBody(request);
    const inquiry = data.inquiries.find((item) => item.id === id);
    if (!inquiry) {
      sendJson(response, 404, { error: "Inquiry not found" });
      return true;
    }
    inquiry.status = payload.status || inquiry.status;
    inquiry.updatedAt = new Date().toISOString();
    writeData(data);
    sendJson(response, 200, { inquiry });
    return true;
  }

  if (request.method === "DELETE" && requestUrl.pathname.startsWith("/api/inquiries/")) {
    if (!requireAdmin(request, response)) return true;
    const id = decodeURIComponent(requestUrl.pathname.replace("/api/inquiries/", ""));
    data.inquiries = data.inquiries.filter((item) => item.id !== id);
    writeData(data);
    sendJson(response, 200, { ok: true });
    return true;
  }

  if (request.method === "POST" && requestUrl.pathname === "/api/unavailable") {
    if (!requireAdmin(request, response)) return true;
    const payload = await readBody(request);
    const block = {
      id: createId("off"),
      date: payload.date || "",
      time: payload.time || "",
      reason: payload.reason || "暫不開放",
      createdAt: new Date().toISOString(),
    };
    data.unavailable.unshift(block);
    writeData(data);
    sendJson(response, 201, { block });
    return true;
  }

  if (request.method === "DELETE" && requestUrl.pathname.startsWith("/api/unavailable/")) {
    if (!requireAdmin(request, response)) return true;
    const id = decodeURIComponent(requestUrl.pathname.replace("/api/unavailable/", ""));
    data.unavailable = data.unavailable.filter((item) => item.id !== id);
    writeData(data);
    sendJson(response, 200, { ok: true });
    return true;
  }

  if (request.method === "POST" && requestUrl.pathname === "/api/assistant/reply") {
    if (!requireAdmin(request, response)) return true;
    const payload = await readBody(request);
    const inquiry = data.inquiries.find((item) => item.id === payload.inquiryId) || payload.inquiry || {};
    sendJson(response, 200, { reply: generateReply(inquiry, payload.status || "available") });
    return true;
  }

  if (request.method === "GET" && requestUrl.pathname === "/api/articles") {
    sendJson(response, 200, data.articles || []);
    return true;
  }

  if (request.method === "POST" && requestUrl.pathname === "/api/articles") {
    if (!requireAdmin(request, response)) return true;
    const payload = await readBody(request);
    const article = {
      id: createId("art"),
      createdAt: new Date().toISOString(),
      title: payload.title || "未命名文章",
      content: payload.content || "",
      summary: payload.summary || "",
      tags: Array.isArray(payload.tags) ? payload.tags : [],
    };
    if (!data.articles) data.articles = [];
    data.articles.unshift(article);
    writeData(data);
    sendJson(response, 201, { article });
    return true;
  }

  if (request.method === "DELETE" && requestUrl.pathname.startsWith("/api/articles/")) {
    if (!requireAdmin(request, response)) return true;
    const id = decodeURIComponent(requestUrl.pathname.replace("/api/articles/", ""));
    if (!data.articles) data.articles = [];
    data.articles = data.articles.filter((item) => item.id !== id);
    writeData(data);
    sendJson(response, 200, { ok: true });
    return true;
  }

  return false;
}

function serveStatic(response, requestUrl) {
  const redirects = {
    "/belief": "/",
    "/belief.html": "/",
    "/method": "/",
    "/method.html": "/",
    "/system": "/",
    "/system.html": "/",
    "/offer": "/",
    "/offer.html": "/",
    "/contact": "/booking.html",
    "/contact.html": "/booking.html",
  };

  const redirectTarget = redirects[requestUrl.pathname];
  if (redirectTarget) {
    response.writeHead(301, { "Location": redirectTarget });
    response.end();
    return;
  }

  let pathname = decodeURIComponent(requestUrl.pathname === "/" ? "/index.html" : requestUrl.pathname);
  if (!path.extname(pathname)) {
    pathname = `${pathname}.html`;
  }
  const filePath = path.normalize(path.join(root, pathname));

  if (!filePath.startsWith(root)) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }

  const ext = path.extname(filePath);
  const contentType = contentTypes[ext] || "application/octet-stream";

  if (ext === ".mp4") {
    fs.stat(filePath, (err, stats) => {
      if (err) {
        response.writeHead(404);
        response.end("Not found");
        return;
      }
      const range = request.headers.range;
      if (!range) {
        response.writeHead(200, {
          "Content-Type": contentType,
          "Content-Length": stats.size,
        });
        fs.createReadStream(filePath).pipe(response);
        return;
      }
      const parts = range.replace(/bytes=/, "").split("-");
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stats.size - 1;
      const chunksize = (end - start) + 1;
      const fileStream = fs.createReadStream(filePath, { start, end });
      response.writeHead(206, {
        "Content-Range": `bytes ${start}-${end}/${stats.size}`,
        "Accept-Ranges": "bytes",
        "Content-Length": chunksize,
        "Content-Type": contentType,
      });
      fileStream.pipe(response);
    });
    return;
  }

  fs.readFile(filePath, (error, data) => {
    if (error) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }

    response.writeHead(200, {
      "Content-Type": contentType,
    });
    response.end(data);
  });
}

const server = http.createServer(async (request, response) => {
  try {
    const requestUrl = new URL(request.url, `http://${host}:${port}`);
    const protectedFiles = ["/admin.html", "/admin.css", "/admin.js"];
    if (protectedFiles.includes(requestUrl.pathname) && !requireAdmin(request, response)) {
      return;
    }
    if (requestUrl.pathname.startsWith("/api/")) {
      const handled = await handleApi(request, response, requestUrl);
      if (!handled) {
        sendJson(response, 404, { error: "API route not found" });
      }
      return;
    }
    serveStatic(response, requestUrl);
  } catch (error) {
    sendJson(response, 500, { error: error.message });
  }
});

ensureDataFile();
server.listen(port, host, () => {
  console.log(`Tutor site running at http://${displayHost}:${port}/`);
  console.log(`Admin panel: http://${displayHost}:${port}/admin.html`);
});

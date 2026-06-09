# 上線說明

## 正式上線前必填

部署 Node 服務時，請設定環境變數：

```text
ADMIN_USER=你的後台帳號
ADMIN_PASSWORD=你的後台密碼
PORT=5173
DATA_DIR=資料持久化資料夾路徑
```

若未設定，系統會使用預設值 `admin / change-this-password`，不可用於正式上線。

你提供的正式帳密請填在部署平台的環境變數設定裡，不要寫進程式碼或公開文件。

## 本機預覽啟動

在 PowerShell 進入專案資料夾後執行：

```powershell
$env:ADMIN_USER='你的後台帳號'
$env:ADMIN_PASSWORD='你的後台密碼'
$env:PORT='5173'
node server.js
```

看到 `Tutor site running` 後，保持這個視窗開著，網站就會持續運作。

## 網站入口

- 前台：`/`
- 後台：`/admin.html`
- 官方 LINE：`@197nqpdg`

後台已加上 Basic Auth。前台不會顯示後台入口。

## API 權限

- `/api/public-state`：公開，前台用來讀取不可預約時段。
- `/api/inquiries`：公開，家長送出候選申請。
- `/api/state`：需後台登入。
- `/api/unavailable`：需後台登入。
- `/api/assistant/reply`：需後台登入。

## 目前資料儲存方式

目前使用 `data.json` 儲存諮詢與不可預約時段。這適合 MVP 或小規模測試。

正式長期營運時，建議改接正式資料庫，例如 Supabase、PostgreSQL、Firebase 或平台提供的持久化儲存。

如果部署平台支援 Persistent Volume，請設定 `DATA_DIR` 指到該磁碟掛載資料夾，系統會把 `data.json` 建在那裡。

## Google Maps 車程

目前後台提供「開 Google Maps」快速查地點。若要自動判斷前後堂交通時間，之後可接 Google Maps Platform Routes API。

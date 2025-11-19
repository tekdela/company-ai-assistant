# Trợ lý AI nội bộ hỗ trợ công việc cho công ty

Hệ thống trợ lý AI nội bộ hoàn chỉnh với React frontend và FastAPI backend.

## ✨ Tính năng

- 📋 **Quản lý kiến thức**: Upload CSV/TXT và tìm kiếm thông tin
- ⏰ **Đồng hồ thời gian thực**: Hỗ trợ VN 🇻🇳, Nhật 🇯🇵, Hàn 🇰🇷, Mỹ 🇺🇸
- 🔄 **Dịch Việt-Nhật**: Từ điển thuật ngữ kỹ thuật và kinh doanh
- 💬 **Giao diện chat hiện đại**: Glass morphism với gradient đẹp mắt

## 🚀 Cài đặt và chạy

### Phương pháp 1: Docker (Khuyến nghị)

```bash
# Clone repository
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant

# Chạy với Docker Compose
docker-compose up -d
```

Truy cập: http://localhost:3000

### Phương pháp 2: Chạy thủ công

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 📚 Sử dụng

### Upload tài liệu
1. Kéo thả file CSV/TXT vào khu vực upload
2. Hệ thống sẽ xử lý và lưu vào database
3. Bắt đầu hỏi về thông tin trong file

### Câu hỏi mẫu
- "Bây giờ mấy giờ?"
- "Giờ ở Nhật Bản là mấy giờ?"
- "Dịch sang tiếng Nhật 'cảm ơn'"
- Hỏi về thông tin trong file đã upload

## 🛠 Công nghệ

- **Backend**: FastAPI, Python 3.11, SQLite, Pandas
- **Frontend**: React 18, TypeScript, React Dropzone
- **Deployment**: Docker, Docker Compose

## 📝 API Endpoints

- `POST /api/chat` - Chat với AI assistant
- `POST /api/upload-knowledge` - Upload CSV/TXT files
- `GET /api/time?timezone=xxx` - Lấy thời gian theo timezone
- `GET /` - Trạng thái API

## 🎨 Tính năng UI

- ✅ Glass morphism design
- ✅ Gradient background đẹp mắt
- ✅ Drag & drop file upload
- ✅ Real-time messaging
- ✅ Typing indicators
- ✅ Quick question buttons
- ✅ Mobile responsive

## 📄 License

MIT

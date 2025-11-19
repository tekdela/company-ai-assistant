# Hướng dẫn sử dụng Trợ lý AI

## Khởi động hệ thống

### Phương pháp 1: Docker Compose (Khuyến nghị)
```bash
docker-compose up -d
```
Truy cập: http://localhost:3000

### Phương pháp 2: Chạy riêng lẻ

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```
Truy cập: http://localhost:3000

## Các tính năng

### 1. Tra cứu thời gian
**Ví dụ câu hỏi:**
- "Bây giờ mấy giờ?"
- "Giờ ở Nhật Bản là mấy giờ?"
- "Thời gian ở Hàn Quốc?"
- "Mấy giờ ở Mỹ?"

**Kết quả:** Hiển thị giờ địa phương với emoji cờ quốc gia 🇻🇳 🇯🇵 🇰🇷 🇺🇸

### 2. Dịch Việt - Nhật
**Ví dụ câu hỏi:**
- "Dịch sang tiếng Nhật 'xin chào'"
- "Dịch 'cảm ơn'"
- "Translate 'công ty'"

**Hỗ trợ:** Thuật ngữ kỹ thuật, kinh doanh, từ vựng thông dụng

### 3. Tìm kiếm tài liệu nội bộ

**Bước 1: Upload tài liệu**
- Kéo thả file CSV/TXT vào khu vực upload
- Hệ thống tự động xử lý và lưu vào database

**Bước 2: Đặt câu hỏi**
- Hỏi bất cứ điều gì liên quan đến tài liệu
- Ví dụ: "Quy trình onboarding?" hoặc "Giờ làm việc công ty?"

**Lưu ý:**
- Nếu không có thông tin, bot sẽ trả lời "Không tìm thấy thông tin"
- Bot chỉ trả lời dựa trên dữ liệu đã upload (NO HALLUCINATION)

## Upload file CSV

**Format mẫu:**
```csv
Category,Information
Quy trình,"Mô tả quy trình..."
Chính sách,"Mô tả chính sách..."
```

**Lưu ý:**
- Dùng dấu ngoặc kép "" cho nội dung có dấu phẩy
- Encoding: UTF-8
- Hỗ trợ .csv và .txt

## API Endpoints

Nếu muốn tích hợp với hệ thống khác:

**1. Chat endpoint:**
```bash
POST http://localhost:8000/api/chat
Content-Type: application/json
{
  "message": "Bây giờ mấy giờ?"
}
```

**2. Upload file:**
```bash
POST http://localhost:8000/api/upload-knowledge
Content-Type: multipart/form-data
file: <your-file.csv>
```

**3. Get time:**
```bash
GET http://localhost:8000/api/time?timezone=japan
```

## Xử lý sự cố

**Backend không khởi động:**
```bash
cd backend
pip install --upgrade -r requirements.txt
```

**Frontend lỗi:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Database lỗi:**
```bash
cd backend
rm knowledge.db
# Hệ thống sẽ tự tạo lại database mới
```

## Thông tin kỹ thuật

- Backend: FastAPI (Python 3.11+)
- Frontend: React 18 + TypeScript
- Database: SQLite
- Port: Backend 8000, Frontend 3000

# Affina – Phân tích dữ liệu với Metabase và Streamlit (Docker Compose)

Dự án này dựng nhanh một stack phân tích dữ liệu gồm:
- PostgreSQL (lưu trữ dữ liệu)
- Ingest (ETL: đọc Excel và nạp vào Postgres)
- Metabase (tạo câu hỏi/báo cáo/dashboard)
- Streamlit (dashboard tuỳ biến bằng Python)
---

## Kiến trúc tổng quan

Luồng dữ liệu:
1) ingest/ingest.py đọc file Excel `ingest/data.xlsx`, làm sạch tối thiểu và ghi vào bảng `raw_data` trong Postgres.
2) Metabase kết nối tới Postgres để tạo câu hỏi, biểu đồ và dashboard.
3) Streamlit đọc bảng `raw_data` để hiển thị dữ liệu và vẽ biểu đồ cơ bản.

Services và cổng:
- postgres:5432 (nội bộ Compose, map ra host 5432)
- metabase:3000 (http://localhost:3000)
- streamlit:8501 (http://localhost:8501)
- mcp_placeholder: placeholder để bạn tích hợp MCP/scheduler sau này (không bắt buộc chạy)

Thông số kết nối mặc định (theo docker-compose.yml):
- DB name: `analytics`
- User: `babyfat`
- Password: `admin`
- Host (từ containers khác): `postgres`
- Host (từ máy bạn): `localhost`

---

## Cấu trúc dự án

```
Metabase/
├─ docker-compose.yml           # Định nghĩa các services Docker
├─ README.md                    # Tài liệu hướng dẫn
├─ ingest/
│  ├─ Dockerfile                # Image cho service ingest
│  ├─ requirements.txt          # Thư viện Python cho ingest
│  ├─ ingest.py                 # Script ETL đọc Excel -> Postgres (bảng raw_data)
│  └─ data.xlsx                 # Dữ liệu nguồn (bạn đặt file ở đây)
└─ streamlit/
   ├─ Dockerfile                # Image cho service streamlit
   ├─ requirements.txt          # Thư viện Python cho streamlit
   └─ streamlit_app.py          # Ứng dụng dashboard Streamlit
```

---

## Yêu cầu hệ thống

- Docker Desktop (Windows) đã bật Docker Compose v2
- Cổng trống: 3000 (Metabase), 8501 (Streamlit), 5432 (Postgres)
- File dữ liệu `ingest/data.xlsx`

Lưu ý: Docker mới không cần khoá `version:` trong docker-compose.yml. Bạn có thể thấy cảnh báo “the attribute `version` is obsolete”. Có thể bỏ dòng đó để tránh cảnh báo (không ảnh hưởng chạy).

---

## Cài đặt và chạy (Windows – cmd.exe)

1) Mở Command Prompt và cd vào thư mục dự án:

```
cd C:\Users\admin\Desktop\Affina\Metabase
```

2) Khởi động toàn bộ services (build nếu cần):

```
docker compose up -d --build
```

3) Kiểm tra trạng thái:

```
docker compose ps
```

4) Xem log nhanh theo service:

```
docker compose logs -f postgres
docker compose logs -f ingest
docker compose logs -f streamlit
docker compose logs -f metabase
```

5) Truy cập ứng dụng:
- Metabase: http://localhost:3000
- Streamlit: http://localhost:8501

Thiết lập Metabase lần đầu (Admin Setup) → Add your database:
- Database type: PostgreSQL
- Host: postgres
- Port: 5432
- Database name: analytics
- Username: babyfat
- Password: admin

---

## Cách hoạt động của Ingest (ETL)

- Service `ingest` chạy một lần khi bạn `up` stack, đọc `ingest/data.xlsx` và ghi bảng `raw_data` (replace).
- Biến môi trường DB dùng trong `ingest`:
  - `DATABASE_URL=postgresql://babyfat:admin@postgres:5432/analytics`

---

## Ghi chú về Streamlit

- Streamlit kết nối tới cùng Postgres qua biến môi trường `DATABASE_URL`.
- Ứng dụng mặc định đọc `SELECT * FROM raw_data LIMIT 500` và hiển thị bảng + vẽ biểu đồ cho cột numeric.

Restart nếu bạn sửa code:
```
docker compose restart streamlit
```

---

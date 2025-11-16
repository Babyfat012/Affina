# Affina – Phân tích dữ liệu với Metabase + Streamlit + MCP

Dự án này xây dựng một hệ thống phân tích dữ liệu hoàn chỉnh với kiến trúc hiện đại, bao gồm:
- **MySQL** (Remote database - cơ sở dữ liệu chính)
- **PostgreSQL** (Metadata store cho Metabase)
- **Ingest Service** (ETL: đọc Excel và nạp vào MySQL)
- **Metabase** (Business Intelligence - tạo dashboard và báo cáo)
- **Streamlit** (Custom dashboard với Python)
- **MCP** (Model Context Protocol - placeholder cho tích hợp AI/LLM)

---

## 🏗️ Kiến trúc hệ thống

### Luồng dữ liệu

```
[Excel File] → [Ingest Service] → [MySQL Remote DB]
                                        ↓
                                   [Metabase]
                                        ↓
                                   [Streamlit]
                                        ↓
                              [Dashboard & Analytics]
```

**Chi tiết:**
1. **Ingest Service** đọc file `data.xlsx`, làm sạch dữ liệu và ghi vào bảng `raw_data` trong MySQL
2. **Metabase** kết nối đến MySQL để tạo câu hỏi, biểu đồ và dashboard tương tác
3. **Streamlit** đọc từ MySQL để hiển thị dashboard tuỳ chỉnh với Python
4. **MCP Placeholder** sẵn sàng cho tích hợp AI/LLM trong tương lai

### Services và Ports

| Service | Port | URL | Mô tả |
|---------|------|-----|-------|
| **metabase_db** | 5432 | - | PostgreSQL cho metadata Metabase |
| **metabase** | 3001 | http://localhost:3001 | Giao diện BI của Metabase |
| **streamlit** | 8501 | http://localhost:8501 | Dashboard Python tùy chỉnh |
| **ingest** | - | - | ETL job (chạy 1 lần rồi tắt) |
| **mcp_placeholder** | - | - | Placeholder cho MCP integration |

### Thông tin kết nối

**MySQL Remote Database (Production):**
- Host: `<PORT_MYSQL_HOST>`
- Port: `3306`
- Database: `<YOUR_DB_NAME>`
- Username: `<YOUR_DB_USER_NAME>`
- Password: `<YOUR_DB_PASSWORD_NAME>`
- Connection String: `<YOUR_DB_URL>`

**PostgreSQL (Metabase Metadata):**
- Host: `metabase_db` (internal) / `localhost` (từ máy host)
- Port: `5432`
- Database: `metabase_app`
- Username: `<MB_DB_USER>`
- Password: `<MB_DB_PASS>`

**⚠️ Lưu ý bảo mật:** Thông tin nhạy cảm được quản lý qua file `.env`

---

## 📁 Cấu trúc dự án

```
Metabase/
├─ docker-compose.yml           # Định nghĩa các Docker services
├─ .env                         # Biến môi trường (credentials, config)
├─ README.md                    # Tài liệu hướng dẫn (file này)
├─ metabase_backup.sql          # Backup metadata Metabase
│
├─ ingest/                      # Service ETL
│  ├─ Dockerfile                # Docker image cho ingest
│  ├─ requirements.txt          # Dependencies Python
│  ├─ ingest.py                 # Script ETL: Excel → MySQL
│  ├─ data.xlsx                 # Dữ liệu nguồn chính
│  └─ data - Copy.xlsx          # Backup dữ liệu
│
└─ streamlit/                   # Service Dashboard
   ├─ Dockerfile                # Docker image cho Streamlit
   ├─ requirements.txt          # Dependencies Python
   └─ streamlit_app.py          # Ứng dụng dashboard web
```

---

## 🧩 Mô tả các Components

### 1. **Ingest Service** (ETL Pipeline)
**Chức năng:**
- Đọc dữ liệu từ file Excel (`data.xlsx`)
- Làm sạch dữ liệu (loại bỏ duplicates, xử lý missing values)
- Ghi vào bảng `raw_data` trong MySQL remote database

**Tech stack:** Python 3.11, Pandas, SQLAlchemy, OpenPyXL, PyMySQL

**Cách hoạt động:**
- Service chạy một lần khi `docker compose up`
- Sau khi hoàn thành sẽ tự động dừng
- Có thể chạy lại bằng: `docker compose restart ingest`

**File quan trọng:**
- `ingest/ingest.py`: Logic ETL chính
- `ingest/data.xlsx`: Dữ liệu đầu vào (188 dòng)

**Environment variables:**
- `DATABASE_URL`: Connection string đến MySQL (từ file `.env`)

### 2. **Metabase** (Business Intelligence Tool)
**Chức năng:**
- Kết nối đến MySQL để query và phân tích dữ liệu
- Tạo questions (câu hỏi SQL)
- Xây dựng visualizations (biểu đồ, bảng)
- Tạo dashboards tương tác
- Hỗ trợ plugins và custom visualizations

**Tech stack:** Metabase OSS (Open Source), Java

**Đặc điểm:**
- **Metadata Store:** Sử dụng PostgreSQL riêng (`metabase_db`) để lưu cấu hình
- **Plugins:** Mount folder `./plugins` cho custom drivers
- **Encryption:** Sử dụng secret key để mã hóa sensitive data

**Cấu hình:**
- Port: `3001` (map từ 3000 internal)
- First-time setup: Tạo admin account khi lần đầu truy cập

**Environment variables:**
- `MB_DB_TYPE`: 
- `MB_DB_HOST`: 
- `MB_DB_PORT`: 
- `MB_DB_DBNAME`: 
- `MB_DB_USER`: 
- `MB_DB_PASS`: 
- `MB_ENCRYPTION_SECRET_KEY`: 

### 3. **Streamlit Dashboard**
**Chức năng:**
- Kết nối trực tiếp đến MySQL
- Hiển thị dữ liệu từ bảng `raw_data`
- Tạo biểu đồ tương tác với Python
- UI đơn giản, dễ customize

**Tech stack:** Python 3.11, Streamlit, Pandas, SQLAlchemy

**Đặc điểm:**
- Real-time dashboard
- Caching data với `@st.cache_data`
- Auto-detect numeric columns để vẽ charts
- Có thể mở rộng thêm các visualizations

**File quan trọng:**
- `streamlit/streamlit_app.py`: Code dashboard chính

**Environment variables:**
- `DATABASE_URL`: Connection string đến MySQL (từ file `.env`)

### 4. **MCP Placeholder** (Future Integration)
**Chức năng:**
- Placeholder service cho Model Context Protocol
- Dự kiến tích hợp AI/LLM capabilities
- Có thể thay thế bằng scheduler/orchestrator thực (Airflow, Prefect)

**Hiện tại:**
- Chỉ là Alpine container echo message
- Không ảnh hưởng đến các service khác

**Tương lai:**
- Tích hợp MCP để hỗ trợ natural language queries
- AI-powered data insights
- Automated report generation

### 5. **PostgreSQL (metabase_db)**
**Chức năng:**
- Lưu trữ metadata của Metabase:
  - User accounts và permissions
  - Questions và SQL queries
  - Dashboard configurations
  - Visualization settings
  - Schedule và alerts

**Tech stack:** PostgreSQL 15

**Đặc điểm:**
- Volume persistent: `mb_pgdata`
- Restart policy: `unless-stopped`
- Expose port 5432 để backup/restore

---

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống
- **Docker Desktop** for Windows (bật Docker Compose v2)
- **Ports trống:** 3001, 8501, 5432
- **File dữ liệu:** `ingest/data.xlsx`
- **Network:** Có thể kết nối đến ``

### Bước 1: Chuẩn bị môi trường

```cmd
cd C:\Users\admin\Desktop\Affina\Metabase
```

### Bước 2: Khởi động services

**Build và start tất cả services:**
```cmd
docker compose up -d --build
```

**Chỉ start (không build lại):**
```cmd
docker compose up -d
```

### Bước 3: Kiểm tra trạng thái

```cmd
docker compose ps
```

**Output mong đợi:**
```
NAME                  STATUS    PORTS
metabase_db           Up        0.0.0.0:5432->5432/tcp
metabase              Up        0.0.0.0:3001->3000/tcp
streamlit             Up        0.0.0.0:8501->8501/tcp
ingest                Exited    (code 0)
mcp_placeholder       Exited    (code 0)
```

### Bước 4: Xem logs

**Xem log của service cụ thể:**
```cmd
docker compose logs -f metabase
docker compose logs -f streamlit
docker compose logs ingest
```

**Output mong đợi cho ingest:**
```
ingest-1  | Ingest finished: wrote 188 rows
```

**Xem tất cả logs:**
```cmd
docker compose logs
```

### Bước 5: Truy cập ứng dụng

**Metabase:** http://localhost:3001
- Lần đầu: Setup admin account
- Add database connection:
  - Type: MySQL
  - Host: ``
  - Port: ``
  - Database: ``
  - Username: ``
  - Password: ``

**Streamlit:** http://localhost:8501
- Tự động load dữ liệu từ bảng `raw_data`
- Hiển thị charts nếu có numeric columns

---

## 🔧 Quản lý và vận hành

### Chạy lại Ingest job
```cmd
docker compose restart ingest
docker compose logs -f ingest
```

### Stop tất cả services
```cmd
docker compose down
```

### Stop và xóa volumes (⚠️ mất dữ liệu)
```cmd
docker compose down -v
```

### Backup Metabase metadata
```cmd
docker exec -t metabase_db pg_dump -U admin metabase_app > metabase_backup.sql
```

### Restore Metabase metadata
```cmd
docker exec -i metabase_db psql -U admin metabase_app < metabase_backup.sql
```

### Rebuild một service cụ thể
```cmd
docker compose up -d --build streamlit
```

### Xem resource usage
```cmd
docker stats
```

---

## 🛠️ Troubleshooting

### Lỗi: "relation raw_data does not exist"
**Nguyên nhân:** Ingest service chưa chạy hoặc thất bại

**Giải pháp:**
```cmd
docker compose logs ingest
docker compose restart ingest
```

Xác nhận đã thấy message: `Ingest finished: wrote 188 rows`

### Lỗi: "Can't connect to MySQL server"
**Nguyên nhân:** Network không thể reach `172.16.10.32` hoặc credentials sai

**Giải pháp:**
- Kiểm tra VPN/network
- Verify credentials trong `.env`
- Test connection từ container:
```cmd
docker exec -it streamlit ping 172.16.10.32
```

### Lỗi: "Port already in use"
**Nguyên nhân:** Port 3001, 8501 hoặc 5432 đã được dùng

**Giải pháp:**
- Tìm process đang dùng port: 
```cmd
netstat -ano | findstr :3001
```
- Stop process hoặc đổi port trong `docker-compose.yml`

### Lỗi: "additional properties not allowed"
**Nguyên nhân:** Cảnh báo YAML format (không ảnh hưởng)

**Giải pháp:** Bỏ qua hoặc kiểm tra indent trong `docker-compose.yml`

### Warning: "version is obsolete"
**Nguyên nhân:** Docker Compose v2 không cần key `version:`

**Giải pháp:** Bỏ qua - không ảnh hưởng, hoặc xóa dòng `version:` trong file

---

## 📊 Dữ liệu và Schema

### Bảng: raw_data
**Source:** `ingest/data.xlsx`

**Số dòng:** 188 rows (sau khi làm sạch)

**Columns:** Tùy thuộc vào file Excel của bạn

**ETL Process:**
1. Load từ Excel (sheet đầu tiên)
2. Drop duplicates
3. Drop rows where all values are NULL
4. Write to MySQL với mode `replace`

**Code tham khảo:**
```python
# ingest/ingest.py
df = pd.read_excel("data.xlsx", sheet_name=0, engine="openpyxl")
df = df.drop_duplicates()
df = df.dropna(how="all")
df.to_sql("raw_data", engine, if_exists="replace", index=False)
```

---

## 🔐 Bảo mật

### File .env
**⚠️ QUAN TRỌNG:** File `.env` chứa credentials nhạy cảm

**Best practices:**
- ✅ Đã add vào `.gitignore` (không push lên Git)
- ✅ Backup riêng ở nơi an toàn
- ✅ Không share qua email/chat
- ✅ Sử dụng secrets manager trong production

### Encryption
- Metabase sử dụng `MB_ENCRYPTION_SECRET_KEY` để mã hóa:
  - Database passwords
  - OAuth tokens
  - Email credentials

**⚠️ Lưu ý:** Không thay đổi key này sau khi đã setup Metabase (sẽ không decrypt được)

### Production checklist
- [ ] Đổi passwords mặc định
- [ ] Sử dụng HTTPS/SSL
- [ ] Giới hạn network access (firewall)
- [ ] Regular backup
- [ ] Monitoring và logging
- [ ] Update Docker images thường xuyên

---

## 🚀 Roadmap

### Phase 1: ✅ Completed
- [x] Docker Compose setup
- [x] MySQL remote connection
- [x] Metabase integration
- [x] Streamlit dashboard
- [x] ETL pipeline (Excel → MySQL)
- [x] Environment variables management

### Phase 2: 🔄 Planned
- [ ] MCP (Model Context Protocol) integration
- [ ] AI/LLM capabilities cho natural language queries
- [ ] Advanced visualizations
- [ ] Real-time data updates
- [ ] Authentication & Authorization

### Phase 3: 📋 Future
- [ ] Scheduled ETL jobs (Airflow/Prefect)
- [ ] Data quality checks
- [ ] Alerting system (Email/Slack)
- [ ] Performance optimization
- [ ] Multi-environment support (Dev/Staging/Prod)

---

## 📚 Tài liệu tham khảo

- [Metabase Documentation](https://www.metabase.com/docs/latest/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 👥 Liên hệ và hỗ trợ

**Project Location:** `C:\Users\admin\Desktop\Affina\Metabase`

**GitHub:** https://github.com/Babyfat012/Affina

**Database Admin:** `aff_admin` (172.16.10.32:3306)

---

## 📝 License

Internal project - Affina

---

**Cập nhật lần cuối:** 16/11/2025


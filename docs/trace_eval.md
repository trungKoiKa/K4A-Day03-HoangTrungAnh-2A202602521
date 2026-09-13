# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Hoàng Trung Anh]  
> **Mã Sinh Viên / Mã Học viên:** [2A202602521]  
> **Chủ đề Lựa chọn:** [ *Trợ lý Học vụ & Tra cứu Lịch thi VinUni:* Tra cứu điểm GPA, lịch thi và đặt lịch tư vấn học vụ với Cố vấn.]

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá           | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm                                                                                                                                                                                                                                                                                                                                               |     |
| --------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| **1. Multi-step Reasoning** | 4/5            | Tra cứu GPA hoặc lịch thi đơn thuần chỉ là truy vấn dữ liệu. Nhưng khi người dùng hỏi kiểu “em có đủ điều kiện đăng ký môn/đủ điều kiện tốt nghiệp không?”, trợ lý phải lấy điểm từng học phần, số tín chỉ, quy chế đào tạo rồi tính và giải thích kết quả. Đặt lịch tư vấn cũng có chuỗi bước: hiểu nhu cầu → kiểm tra lịch trống → đề xuất khung giờ → xác nhận → tạo lịch hẹn. |     |
| **2. Tool Interaction**     | 4/5            | Bắt buộc cần kết nối dữ liệu bên ngoài: hệ thống quản lý học tập/SIS để lấy GPA và điểm; hệ thống lịch thi; lịch làm việc của cố vấn; có thể thêm email hoặc calendar để gửi xác nhận. Đây là điểm mạnh nhất của đề tài                                                                                                                                                           |     |
| **3. Dynamic Decision**     | 3/5            | Hành động tiếp theo phụ thuộc dữ liệu vừa quan sát. Ví dụ: nếu lịch thi bị trùng hoặc quá sát nhau, agent cảnh báo; nếu cố vấn không rảnh, agent tìm khung giờ khác; nếu GPA thấp hơn ngưỡng, agent đề xuất đặt lịch tư vấn học vụ hoặc hiển thị các môn cần cải thiện.                                                                                                           |     |
| **4. Long Horizon Goal**    | 4/5            | Agent có thể giữ mục tiêu qua nhiều lượt: “tìm lịch tư vấn phù hợp trước kỳ thi”, “theo dõi thay đổi lịch thi”, “nhắc sinh viên trước ngày thi”. Tuy nhiên, nếu chỉ làm tra cứu một lần rồi trả kết quả thì tính long-horizon chưa cao. Có thể nâng điểm bằng tính năng theo dõi, nhắc lịch và xử lý đổi lịch tự động.                                                            |     |
| **TỔNG ĐIỂM AGENTIC FIT**   | **15/ 20**     | Tổng điểm của 4 tiêu chí là 15 > 12: Bài toán với chủ đề: Trợ lý học vụ & Tra cứu lịch: Tra cứu điểm GPA, lịch thi và đặt lịch tư vấn học vụ với Cố vấn. thi rất phù hợp để triển khai Agentic System                                                                                                                                                                             |     |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu GPA và tên cố vấn học tập của sinh viên SV2026002, sau đó đặt lịch tư vấn cho sinh viên này với đúng cố vấn vào lúc 09:30 ngày 18/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026002"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026002",
      "data": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.6,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
      }
    },
    "latency_ms": 627.41
  },
  {
    "step": 2,
    "query": "Hãy tra cứu GPA và tên cố vấn học tập của sinh viên SV2026002, sau đó đặt lịch tư vấn cho sinh viên này với đúng cố vấn vào lúc 09:30 ngày 18/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_appointment",
    "arguments": {
      "advisor_name": "TS. Lê Thị B",
      "datetime_str": "09:30 18/09/2026",
      "student_id": "SV2026002"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-SV2026002-99",
      "student_id": "SV2026002",
      "datetime": "09:30 18/09/2026",
      "advisor": "TS. Lê Thị B",
      "message": "Đặt lịch thành công cho sinh viên SV2026002 với TS. Lê Thị B vào lúc 09:30 18/09/2026."
    },
    "latency_ms": 1289.65
  },
  {
    "step": 3,
    "query": "Hãy tra cứu GPA và tên cố vấn học tập của sinh viên SV2026002, sau đó đặt lịch tư vấn cho sinh viên này với đúng cố vấn vào lúc 09:30 ngày 18/09/2026.",
    "action_type": "FINAL_ANSWER",
    "thought": "Groq phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "GPA của sinh viên **SV2026002** là **3.6** và cố vấn học tập của anh/Chị là **TS. Lê Thị B**.\n\nLịch hẹn tư vấn đã được đặt thành công:\n\n- **Ngày / Giờ:** 18/09/2026 09:30  \n- **Cố vấn:** TS. Lê Thị B  \n- **Mã đặt lịch:** BK‑SV2026002‑99\n\nNếu cần thay đổi hoặc hủy lịch, xin liên hệ phòng học vụ. Chúc thành công!",
    "latency_ms": 455.86
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã cấu hình API Key trong `.env` và xác nhận Agent chạy trên Groq API (`openai/gpt-oss-safeguard-20b`).

- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!

"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ. Có thể bỏ student_id để tra cứu sinh viên đang đăng nhập (CURRENT_STUDENT_ID).",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên; bỏ qua nếu tra cứu hồ sơ sinh viên đang đăng nhập."
                }
            },
            "required": []
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string, optional): Mặc định lấy hồ sơ sinh viên đang đăng nhập
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string, optional): Mặc định lấy cố vấn trong hồ sơ sinh viên
    # 3. Chỉ datetime_str là bắt buộc; danh tính lấy từ ngữ cảnh người dùng.
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch với cố vấn học tập. Bỏ student_id và advisor_name để dùng hồ sơ sinh viên đang đăng nhập và cố vấn đã gán.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên; bỏ qua để dùng hồ sơ sinh viên đang đăng nhập."
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn; bỏ qua để dùng cố vấn được gán trong hồ sơ sinh viên."
                }
            },
            "required": ["datetime_str"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}


def _resolve_student_id(student_id: str = None) -> str:
    """Dùng mã được truyền vào hoặc hồ sơ người dùng hiện tại trong phiên."""
    return (student_id or os.getenv("CURRENT_STUDENT_ID", "")).strip().upper()


def _missing_student_context() -> str:
    return json.dumps({
        "status": "CONTEXT_REQUIRED",
        "message": "Chưa có hồ sơ sinh viên hiện tại. Đăng nhập và truyền student_id từ session; trong demo, cấu hình CURRENT_STUDENT_ID trong .env."
    }, ensure_ascii=False)


def execute_academic_query(student_id: str = None) -> str:
    """Tra cứu hồ sơ theo mã chỉ định hoặc hồ sơ người dùng hiện tại."""
    student_id = _resolve_student_id(student_id)
    if not student_id:
        return _missing_student_context()

    student = MOCK_DATABASE.get(student_id)
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(
    student_id: str = None,
    datetime_str: str = None,
    advisor_name: str = None,
) -> str:
    """Đặt lịch; tự lấy sinh viên và cố vấn từ hồ sơ hiện tại nếu không truyền."""
    student_id = _resolve_student_id(student_id)
    if not student_id:
        return _missing_student_context()

    student = MOCK_DATABASE.get(student_id)
    if not student:
        return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"}, ensure_ascii=False)
    if not datetime_str:
        return json.dumps({"status": "NEEDS_INPUT", "field": "datetime_str", "message": "Cần ngày và giờ muốn đặt lịch."}, ensure_ascii=False)

    advisor_name = advisor_name or student.get("advisor")
    if not advisor_name:
        return json.dumps({"status": "ADVISOR_NOT_FOUND", "message": "Hồ sơ hiện tại chưa có cố vấn được gán."}, ensure_ascii=False)

    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)

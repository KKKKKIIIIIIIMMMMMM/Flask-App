# 🖼️ KIM Gallery

คุณสมบัติหลัก

ไว้สำหรับแสดงผลรูปภาพและวิดีโอที่ผู้ใช้งานอัปโหลดเพื่อไปแชร์กับผู้อื่นได้เเละเก็บเพื่อเป็นความทรงจำของตัวเอง

## Usage
- Python 3.11+
- Flask
- SQLAlchemy
- Flask-Login
- Bootstrap 5
- HTML5/CSS3/JavaScript

## Requirements
- Python 3.11 หรือสูงกว่า
- Poetry (สำหรับจัดการแพ็คเกจ)
- SQLite (ฐานข้อมูล)


## Structure
```
KIM-Gallery/
├── kim_gallery/
│   ├── auth/         # ระบบยืนยันตัวตน
│   ├── gallery/      # จัดการรูปภาพและวิดีโอ
│   ├── main/         # หน้าหลักและฟังก์ชันทั่วไป
│   ├── static/       # ไฟล์ static (CSS, JS, รูปภาพ)
│   └── templates/    # เทมเพลต HTML
├── migrations/       # ไฟล์ migration ฐานข้อมูล
├── pyproject.toml   # การกำหนดค่า Poetry
└── run.py           # จุดเริ่มต้นแอปพลิเคชัน

## วิธีใช้งาน
1. ลงทะเบียนบัญชีผู้ใช้ใหม่
2. เข้าสู่ระบบ
3. อัปโหลดรูปภาพหรือวิดีโอ
4. เพิ่มแท็กและคำอธิบาย
5. แชร์ผลงานกับผู้อื่น

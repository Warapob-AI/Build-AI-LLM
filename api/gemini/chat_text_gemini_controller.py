import requests
# -*- coding: utf-8 -*-

def chat_with_ai(prompt, GEMINI_API_KEY):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    params = {"key": GEMINI_API_KEY}

    response = requests.post(url, headers=headers, params=params, json=data, timeout=60)
    if response.status_code == 200:
        res = response.json()
        try:
            return res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "❌ ไม่สามารถอ่านคำตอบจาก Gemini ได้"
    else:
        return f"❌ เกิดข้อผิดพลาด: {response.text}"

def chat_header_ai_gen(prompt, GEMINI_API_KEY):
    """
    ส่ง prompt ไปยัง Gemini เพื่อให้ AI สรุปหรือสร้าง header (หัวข้อ) ให้
    และ return เฉพาะ header ที่ได้กลับมา (เช่น บรรทัดแรก หรือข้อความสั้น)
    """
    import requests

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    # เพิ่มคำสั่งใน prompt เพื่อให้ Gemini สรุป header สั้น ๆ
    header_prompt = (
        "จากข้อความต่อไปนี้ ให้สรุปหัวข้อสั้น ๆ (header) ที่เหมาะสมที่สุด 1 บรรทัด:\n"
        f"{prompt}\n"
        "ตอบกลับมาเฉพาะหัวข้อเท่านั้น"
    )
    data = {
        "contents": [
            {"parts": [{"text": header_prompt}]}
        ]
    }
    params = {"key": GEMINI_API_KEY}

    response = requests.post(url, headers=headers, params=params, json=data, timeout=60)
    if response.status_code == 200:
        res = response.json()
        try:
            # ดึงข้อความ header ที่ Gemini ตอบกลับมา
            header = res["candidates"][0]["content"]["parts"][0]["text"]
            # คืนค่าเฉพาะบรรทัดแรก (กรณี Gemini ตอบหลายบรรทัด)
            return header.strip().split('\n')[0]
        except Exception:
            return "❌ ไม่สามารถอ่าน header จาก Gemini ได้"
    else:
        return f"❌ เกิดข้อผิดพลาด: {response.text}"


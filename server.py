from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# الاتصال بالداتا بيز
def connect_db():
    return sqlite3.connect("attendance.db")

# إنشاء الجدول + إضافة الأسماء
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            attended INTEGER DEFAULT 0,
            absent INTEGER DEFAULT 0
        )
    """)

    # 👇 حط الأسماء هنا
    names = [
       
    ]

    for name in names:
        cursor.execute("INSERT OR IGNORE INTO people (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()

# الصفحة الرئيسية
@app.route("/")
def home():
    return "Server is running"

# حفظ الحضور
@app.route("/save", methods=["POST"])
def save():
    data = request.json

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM people")
    all_people = [row[0] for row in cursor.fetchall()]

    for person in all_people:
        if person in data:
            cursor.execute(
                "UPDATE people SET attended = attended + 1 WHERE name=?",
                (person,)
            )
        else:
            cursor.execute(
                "UPDATE people SET absent = absent + 1 WHERE name=?",
                (person,)
            )

    conn.commit()
    conn.close()

    return jsonify({"message": "Saved successfully"})

# عرض الإحصائيات
@app.route("/stats")
def stats():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, attended, absent FROM people")
    result = cursor.fetchall()

    data = []
    for name, attended, absent in result:
        total = attended + absent
        percent = (attended / total * 100) if total > 0 else 0

        data.append({
            "name": name,
            "attendance": attended,
            "absence": absent,
            "percentage": round(percent, 2)
        })

    conn.close()
    return jsonify(data)

# 👇 أهم حاجة: دي آخر سطر
if __name__ == "__main__":
    init_db()  # إنشاء الداتا بيز أول مرة
    app.run(host="0.0.0.0", port=10000)
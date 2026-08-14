import sqlite3
from datetime import datetime, date

DB_NAME = "student_os.db"

def get_connection():
    """إنشاء اتصال مع قاعدة البيانات"""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # لإرجاع النتائج على شكل Dictionaries لسهولة التعامل
    return conn

def init_db():
    """إنشاء جميع الجداول المطلوبة عند بداية التشغيل"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. جدول المهام (Tasks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. جدول العادات (Habits)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            streak INTEGER DEFAULT 0,
            last_completed DATE
        )
    ''')
    
    # 3. جدول جلسات التركيز (Focus Sessions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            duration_minutes INTEGER NOT NULL,
            session_type TEXT DEFAULT 'Pomodoro',
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


# ==========================================
# ⚙️ 1. عمليات المهام (TASKS CRUD)
# ==========================================

def add_task(title: str, priority: str = "Medium"):
    """إضافة مهمة جديدة"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, priority) VALUES (?, ?)",
        (title, priority)
    )
    conn.commit()
    conn.close()

def get_tasks():
    """جلب جميع المهام"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id: int, status: str):
    """تحديث حالة المهمة (Done / Pending)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    """حذف مهمة"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# ==========================================
# 🔥 2. عمليات العادات (HABITS & STREAKS)
# ==========================================

def add_habit(name: str):
    """إضافة عادة جديدة"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO habits (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_habits():
    """جلب جميع العادات"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    conn.close()
    return habits

def complete_habit(habit_id: int):
    """
    تسجيل إنجاز العادة وحساب الـ Streak:
    - إذا أنجزت اليوم: لا يتغير شيء.
    - إذا أنجزت البارحة: يزداد الـ streak بـ 1.
    - إذا فات أكثر من يوم: يعاد الـ streak إلى 1.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT streak, last_completed FROM habits WHERE id = ?", (habit_id,))
    habit = cursor.fetchone()
    
    if habit:
        today = date.today()
        current_streak = habit["streak"]
        last_date_str = habit["last_completed"]
        
        if last_date_str:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # تم الإنجاز اليوم من قبل
                conn.close()
                return False 
            elif days_diff == 1:
                # إنجاز متتابع (يوم غد)
                new_streak = current_streak + 1
            else:
                # انقطع السلسلة
                new_streak = 1
        else:
            # أول مرة تتسجل
            new_streak = 1
            
        cursor.execute(
            "UPDATE habits SET streak = ?, last_completed = ? WHERE id = ?",
            (new_streak, today.isoformat(), habit_id)
        )
        conn.commit()
        conn.close()
        return True

def delete_habit(habit_id: int):
    """حذف عادة"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()


# ==========================================
# ⏱️ 3. عمليات جلسات التركيز (FOCUS SESSIONS)
# ==========================================

def log_focus_session(duration_minutes: int, session_type: str = "Pomodoro"):
    """تسجيل جلسة تركيز مكتملة"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO focus_sessions (duration_minutes, session_type) VALUES (?, ?)",
        (duration_minutes, session_type)
    )
    conn.commit()
    conn.close()

def get_total_focus_time():
    """حساب مجموع دقائق التركيز"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(duration_minutes) as total FROM focus_sessions")
    result = cursor.fetchone()
    conn.close()
    return result["total"] if result["total"] else 0
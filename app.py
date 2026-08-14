import streamlit as st
import database as db
import plotly.express as px
import pandas as pd
import time

# 1. إعداد الصفحة
st.set_page_config(
    page_title="Student OS",
    page_icon="🎓",
    layout="wide"
)

# إدخال تنسيق CSS للأزرار الخضراء
st.markdown("""
    <style>
    /* تغيير لون جميع الأزرار للأخضر */
    div.stButton > button {
        background-color: #2ECC71 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    /* تغيير اللون عند تحريك الماوس فوق الزر (Hover) */
    div.stButton > button:hover {
        background-color: #27AE60 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. تهيئة قاعدة البيانات عند التشغيل
db.init_db()

st.title("🎓 Student OS")
st.caption("نظامك الشخصي لإدارة المهام، العادات، ووقت التركيز")

# 3. إنشاء التبويبات (Tabs)
tab_tasks, tab_habits, tab_focus, tab_stats = st.tabs([
    "✅ المهام (Tasks)", 
    "🔥 العادات (Habits)", 
    "⏱️ مؤقت التركيز (Focus)", 
    "📊 الإحصائيات (Stats)"
])

# ==========================================
# 📊 TAB 1: TASKS (إدارة المهام)
# ==========================================
with tab_tasks:
    st.header("📋 إدارة المهام")
    
    # نموذج إضافة مهمة جديدة
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            task_title = st.text_input("عنوان المهمة", placeholder="مثال: مراجعة الرياضيات...")
        with col2:
            priority = st.selectbox("الأولوية", ["Low", "Medium", "High"], index=1)
        
        submit_task = st.form_submit_button("إضافة المهمة ➕")
        if submit_task and task_title.strip():
            db.add_task(task_title.strip(), priority)
            st.success("تمت إضافة المهمة بنجاح!")
            st.rerun()

    st.divider()
    
    # عرض المهام
    tasks = db.get_tasks()
    if not tasks:
        st.info("ما عندك حتى مهمة حالياً. ضيف شي مهمة الفوق! 🎯")
    else:
        for task in tasks:
            col_check, col_title, col_prio, col_del = st.columns([0.5, 3, 1, 0.5])
            
            is_done = task["status"] == "Done"
            
            # زر التغيير بين Done و Pending
            with col_check:
                if st.checkbox("", value=is_done, key=f"task_{task['id']}"):
                    if not is_done:
                        db.update_task_status(task["id"], "Done")
                        st.rerun()
                else:
                    if is_done:
                        db.update_task_status(task["id"], "Pending")
                        st.rerun()
            
            # عنوان المهمة
            with col_title:
                if is_done:
                    st.markdown(f"~~{task['title']}~~")
                else:
                    st.write(task['title'])
            
            # الأولوية
            with col_prio:
                badge_color = "🔴" if task["priority"] == "High" else "🟡" if task["priority"] == "Medium" else "🟢"
                st.caption(f"{badge_color} {task['priority']}")
                
            # حذف
            with col_del:
                if st.button("🗑️", key=f"del_task_{task['id']}"):
                    db.delete_task(task["id"])
                    st.rerun()

# ==========================================
# 🔥 TAB 2: HABITS (تتبع العادات)
# ==========================================
with tab_habits:
    st.header("🔥 تتبع العادات و الـ Streaks")
    
    # إضافة عادة جديدة
    with st.form("add_habit_form", clear_on_submit=True):
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            habit_name = st.text_input("اسم العادة", placeholder="مثال: قراءة 10 صفحات، الرياضة...")
        with col_h2:
            submit_habit = st.form_submit_button("إضافة العادة ➕")
            
        if submit_habit and habit_name.strip():
            db.add_habit(habit_name.strip())
            st.success("تمت إضافة العادة!")
            st.rerun()

    st.divider()
    
    habits = db.get_habits()
    if not habits:
        st.info("باقي ما ضفتي حتى عادة. ابدأ دابا بتبني عادات جديدة! 💪")
    else:
        for habit in habits:
            col_name, col_streak, col_btn, col_del = st.columns([2, 1, 1, 0.5])
            
            with col_name:
                st.subheader(habit["name"])
            
            with col_streak:
                st.metric("الـ Streak الحالي", f"🔥 {habit['streak']} أيام")
                
            with col_btn:
                if st.button("تسجيل إنجاز اليوم ✅", key=f"habit_{habit['id']}"):
                    success = db.complete_habit(habit["id"])
                    if success:
                        st.balloons()
                        st.success("مبروك! كبرتي الـ Streak 🔥")
                    else:
                        st.warning("راه سجلتي هاد العادة اليوم من قبل!")
                    st.rerun()
                    
            with col_del:
                if st.button("🗑️", key=f"del_habit_{habit['id']}"):
                    db.delete_habit(habit["id"])
                    st.rerun()

# ==========================================
# ⏱️ TAB 3: FOCUS TIMER (مؤقت Pomodoro)
# ==========================================
with tab_focus:
    st.header("⏱️ مؤقت التركيز (Pomodoro)")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        minutes_input = st.number_input("مدة الجلسة (بالدقائق):", min_value=1, max_value=120, value=25)
    with col_t2:
        session_type = st.selectbox("نوع الجلسة:", ["Pomodoro 🍅", "Deep Work 🧠", "Quick Review ⚡"])

    if st.button("ابدأ المؤقت 🚀", type="primary"):
        st.write(f"⏱️ بدأت الجلسة: {session_type}")
        
        # حاوية الوقت
        timer_placeholder = st.empty()
        total_seconds = minutes_input * 60
        
        # شريط التقدم
        progress_bar = st.progress(0.0)
        
        for remaining in range(total_seconds, -1, -1):
            mins, secs = divmod(remaining, 60)
            timer_placeholder.header(f"⏳ {mins:02d}:{secs:02d}")
            
            # تحديث شريط التقدم
            progress = (total_seconds - remaining) / total_seconds
            progress_bar.progress(progress)
            
            time.sleep(1)  # تنتظر ثانية واحدة
            
        st.success("🎉 انتهت الجلسة بنجاح! تبارك الله عليك.")
        db.log_focus_session(minutes_input, session_type)
        st.balloons()

# ==========================================
# 📊 TAB 4: STATISTICS (الإحصائيات)
# ==========================================
with tab_stats:
    st.header("📊 إحصائيات الأداء")
    
    tasks = db.get_tasks()
    total_focus = db.get_total_focus_time()
    
    # بطاقات الأرقام الرئيسية (Metrics)
    m1, m2, m3 = st.columns(3)
    
    completed_tasks = len([t for t in tasks if t["status"] == "Done"])
    pending_tasks = len([t for t in tasks if t["status"] == "Pending"])
    
    with m1:
        st.metric("المهام المكتملة", f"{completed_tasks} / {len(tasks)}")
    with m2:
        st.metric("مجموع دقائق التركيز", f"{total_focus} دقيقة ⏱️")
    with m3:
        hours = round(total_focus / 60, 1)
        st.metric("ساعات العمل المركز", f"{hours} ساعة 🧠")
        
    st.divider()
    
    # رسم بياني لحالة المهام باستخدام Plotly
    if tasks:
        st.subheader("توزيع المهام (Done vs Pending)")
        df_tasks = pd.DataFrame([dict(t) for t in tasks])
        status_counts = df_tasks['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig = px.pie(
            status_counts, 
            values='Count', 
            names='Status', 
            color='Status',
            color_discrete_map={'Done': '#2ecc71', 'Pending': '#e74c3c'},
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا توجد بيانات كافية لرسم الإحصائيات بعد.")
import streamlit as st
import database as db
import plotly.express as px
import pandas as pd
import time
import os
import random

# 1. إعداد الصفحة
st.set_page_config(
    page_title="Student OS - Kaoutar Edition", 
    page_icon="👑", 
    layout="wide"
)

# 2. تهيئة قاعدة البيانات
db.init_db()

# 3. قائمة الاقتباسات التحفيزية لكوثر 💡
MOTIVATIONAL_QUOTES = [
    "كوثر، النجاح ماشي حظ، النجاح هو استمرار وتعب يومي! كملي ✨",
    "كوثر، التفوق كينتظرك، كل دقيقة تركيز كتقربك للهدف 🎯",
    "كوثر، انتِ قدها! خلي هدفك دايماً قدام عينيك وقراي بذكاء 🧠🔥",
    "كوثر، العزيمة والحرص هما السر باش تكوني اللولة فـ المدرسة 💪",
    "كوثر، الاستمرارية هي اللي تصنع الفرق، كملي اليوم بطاقة إيجابية 🌟"
]

# اختيار اقتباس عشوائي عند كل تشغيل
daily_quote = random.choice(MOTIVATIONAL_QUOTES)

# 4. تطبيق CSS للتصميم والعبارة التشجيعية
st.markdown("""
    <style>
    /* خلفية القائمة الجانبية Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFC0CB !important;
    }
    
    /* العبارة التحفيزية العلوية */
    .top-goal-banner {
        background-color: #FFE4E1;
        border: 2px dashed #FFB6C1;
        padding: 8px 16px;
        border-radius: 12px;
        font-weight: bold;
        color: #2D3748;
        text-align: center;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* مربع الاقتباس اليومي */
    .quote-box {
        background-color: #FFF0F5;
        border-right: 5px solid #2ECC71;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 500;
        color: #2D3748;
        margin-bottom: 20px;
    }
    
    /* أزرار باللون الأخضر الجميل */
    div.stButton > button {
        background-color: #2ECC71 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 8px 20px !important;
        font-size: 15px !important;
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        background-color: #27AE60 !important;
        transform: scale(1.02);
    }

    /* التبويبات العليا Tabs */
    button[data-baseweb="tab"] {
        background-color: #FFE4E1 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        margin-right: 5px !important;
        color: #2D3748 !important;
        font-weight: bold !important;
    }
    
    button[aria-selected="true"] {
        background-color: #FFB6C1 !important;
        border: 2px solid #2D3748 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 5. العبارة الثابتة فـ الأعلى
st.markdown(
    '<div class="top-goal-banner">👑 لا تنسي هدفنا الأول: الأولى على صعيد المدرسة (19/20) - التلميذة المثالية ✨</div>', 
    unsafe_allow_html=True
)

# 6. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("🎓 Kaoutar OS")
    st.caption("Kuromi Companion Edition 🖤")
    st.write("---")
    st.write("✅ **Tasks:** إدارة المهام")
    st.write("🔥 **Habits:** تتبع العادات")
    st.write("⏱️ **Focus:** مؤقت التركيز")
    st.write("📊 **Stats:** الإحصائيات")
    st.write("---")
    st.write("⚙️ Version v0.5")

# 7. التنسيق الرئيسي (صورة Kuromi + المحتوى)
col_img, col_content = st.columns([1, 2.5])

with col_img:
    if os.path.exists("assets/kuromi.png"):
        st.image("assets/kuromi.png", use_container_width=True)
    else:
        st.info("📌 ضعي صورة Kuromi داخل مجلد assets/kuromi.png لتظهر هنا!")

with col_content:
    st.title("🖤 مرحباً بك كوثر!")
    
    # عرض الاقتباس اليومي
    st.markdown(f'<div class="quote-box">💬 <b>اقتباس اليوم:</b> {daily_quote}</div>', unsafe_allow_html=True)
    
    # إنشاء التبويبات Tabs
    tab_tasks, tab_habits, tab_focus, tab_stats = st.tabs([
        "✅ Tasks", 
        "🔥 Habits", 
        "⏱️ Focus", 
        "📊 Statistics"
    ])

    # ==========================================
    # ✅ TAB 1: TASKS
    # ==========================================
    with tab_tasks:
        st.subheader("📋 إدارة المهام الدراسية")
        
        with st.form("add_task_form", clear_on_submit=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                task_title = st.text_input("عنوان المهمة", placeholder="شنو غادي نراجعوا اليوم يا كوثر؟")
            with c2:
                priority = st.selectbox("الأولوية", ["Low", "Medium", "High"], index=1)
            
            if st.form_submit_button("إضافة مهمة ➕"):
                if task_title.strip():
                    db.add_task(task_title.strip(), priority)
                    st.success("تمت الإضافة بنجاح!")
                    st.rerun()

        st.write("---")
        
        tasks = db.get_tasks()
        if not tasks:
            st.info("لا توجد مهام حالياً! ضيفي مراجعة اليوم ✨")
        else:
            for task in tasks:
                col_check, col_title, col_prio, col_del = st.columns([0.5, 3, 1, 0.5])
                is_done = task["status"] == "Done"
                
                with col_check:
                    if st.checkbox("", value=is_done, key=f"t_{task['id']}"):
                        if not is_done:
                            db.update_task_status(task["id"], "Done")
                            st.rerun()
                    else:
                        if is_done:
                            db.update_task_status(task["id"], "Pending")
                            st.rerun()
                
                with col_title:
                    st.write(f"~~{task['title']}~~" if is_done else task['title'])
                
                with col_prio:
                    badge = "🔴" if task["priority"] == "High" else "🟡" if task["priority"] == "Medium" else "🟢"
                    st.caption(f"{badge} {task['priority']}")
                    
                with col_del:
                    if st.button("🗑️", key=f"del_t_{task['id']}"):
                        db.delete_task(task["id"])
                        st.rerun()

    # ==========================================
    # 🔥 TAB 2: HABITS
    # ==========================================
    with tab_habits:
        st.subheader("🔥 تتبع العادات اليومية")
        
        with st.form("add_habit_form", clear_on_submit=True):
            h_name = st.text_input("اسم العادة الجديدة", placeholder="مثال: حفظ 5 مصطلحات، حل تمارين...")
            if st.form_submit_button("إضافة عادة ➕"):
                if h_name.strip():
                    db.add_habit(h_name.strip())
                    st.success("تمت إضافة العادة!")
                    st.rerun()

        st.write("---")
        
        habits = db.get_habits()
        if not habits:
            st.info("استمري فـ بناء عادات التلميذة المثالية! 💪")
        else:
            for habit in habits:
                col_h_name, col_h_streak, col_h_btn, col_h_del = st.columns([2, 1, 1.5, 0.5])
                
                with col_h_name:
                    st.write(f"**{habit['name']}**")
                
                with col_h_streak:
                    st.caption(f"🔥 {habit['streak']} أيام")
                    
                with col_h_btn:
                    if st.button("تسجيل إنجاز اليوم", key=f"h_{habit['id']}"):
                        success = db.complete_habit(habit["id"])
                        if success:
                            st.balloons()
                            st.success("تبارك الله عليك يا كوثر! 🔥")
                        else:
                            st.warning("تم التسجيل اليوم بالفعل!")
                        st.rerun()
                        
                with col_h_del:
                    if st.button("🗑️", key=f"del_h_{habit['id']}"):
                        db.delete_habit(habit["id"])
                        st.rerun()

    # ==========================================
    # ⏱️ TAB 3: FOCUS TIMER
    # ==========================================
    with tab_focus:
        st.subheader("⏱️ مؤقت التركيز والتفوق")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            mins = st.number_input("مدة الجلسة (دقائق):", min_value=1, max_value=120, value=25)
        with col_f2:
            s_type = st.selectbox("نوع الجلسة:", ["Pomodoro 🍅", "Deep Work 🧠", "Quick Review ⚡"])

        if st.button("ابدأي المؤقت 🚀"):
            st.write(f"بدأت جلسة: {s_type}")
            timer_box = st.empty()
            p_bar = st.progress(0.0)
            
            total_sec = mins * 60
            for r in range(total_sec, -1, -1):
                m, s = divmod(r, 60)
                timer_box.header(f"⏳ {m:02d}:{s:02d}")
                p_bar.progress((total_sec - r) / total_sec)
                time.sleep(1)
                
            st.success("🎉 برافو كوثر! انتهت الجلسة بنجاح.")
            db.log_focus_session(mins, s_type)
            st.balloons()

    # ==========================================
    # 📊 TAB 4: STATISTICS
    # ==========================================
    with tab_stats:
        st.subheader("📊 إحصائيات طريق النجاح")
        
        all_tasks = db.get_tasks()
        total_focus = db.get_total_focus_time()
        
        m1, m2 = st.columns(2)
        done_count = len([t for t in all_tasks if t["status"] == "Done"])
        
        with m1:
            st.metric("المهام المكتملة", f"{done_count} / {len(all_tasks)}")
        with m2:
            st.metric("مجموع ساعات التركيز", f"{round(total_focus / 60, 1)} ساعة 🧠")
            
        st.write("---")
        
        if all_tasks:
            df = pd.DataFrame([dict(t) for t in all_tasks])
            counts = df['status'].value_counts().reset_index()
            counts.columns = ['Status', 'Count']
            
            fig = px.pie(
                counts, 
                values='Count', 
                names='Status', 
                color='Status',
                color_discrete_map={'Done': '#2ECC71', 'Pending': '#E74C3C'},
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية حالياً.")
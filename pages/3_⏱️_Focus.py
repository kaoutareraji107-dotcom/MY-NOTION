import streamlit as st
import database as db
import time
import os

st.set_page_config(page_title="Focus - Kaoutar OS", page_icon="⏱️", layout="wide")

# CSS المخصص + شريط التقدم الوردي
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    
    .top-goal-banner {
        background-color: #FFE4E1; border: 2px dashed #FFB6C1;
        padding: 10px; border-radius: 12px; font-weight: bold;
        color: #2D3748; text-align: center; font-size: 14px; margin-bottom: 20px;
    }
    
    /* تغيير لون شريط التقدم Progress Bar إلى الوردي الاحترافي */
    .stProgress > div > div > div > div {
        background-color: #FFB6C1 !important;
    }
    
    /* تصميم زر البداية الأخضر */
    div.stButton > button {
        background-color: #2ECC71 !important; color: white !important;
        border-radius: 10px !important; border: none !important; 
        font-weight: bold !important; font-size: 16px !important;
        padding: 10px 24px !important;
    }
    div.stButton > button:hover { background-color: #27AE60 !important; }
    </style>
""", unsafe_allow_html=True)

# العبارة الثابتة للهدف الذهبي
st.markdown('<div class="top-goal-banner">👑 لا تنسي هدفنا الأول: الأولى على صعيد المدرسة (19/20) - التلميذة المثالية ✨</div>', unsafe_allow_html=True)

col_img, col_main = st.columns([1, 2.5])

with col_img:
    if os.path.exists("assets/kuromi_focus.png"):
        st.image("assets/kuromi_focus.png", use_container_width=True)
    elif os.path.exists("assets/kuromi.png"):
        st.image("assets/kuromi.png", use_container_width=True)

with col_main:
    st.title("⏱️ مؤقت التركيز والتفوق")
    st.caption("اختاري نوع الجلسة الدراسية وابتعدي عن أي مشتتات يا كوثر! 🧠")

    # تحديد نوع الجلسة
    session_type = st.selectbox(
        "اختر نوع الجلسة الدراسية:",
        ["Pomodoro 🍅", "Deep Work 🧠", "Exam Prep 📚"]
    )

    # تحديد الوقت التلقائي حسب اختيار الجلسة
    if session_type == "Pomodoro 🍅":
        default_mins = 25
    elif session_type == "Deep Work 🧠":
        default_mins = 45
    else:  # Exam Prep
        default_mins = 60

    # إمكانية تعديل الوقت حسب الرغبة
    selected_minutes = st.number_input(
        "مدة الجلسة بالدقائق (يمكنك التعديل):",
        min_value=1,
        max_value=180,
        value=default_mins,
        step=5
    )

    st.write("---")

    if st.button("ابدأي جلسة التركيز الآن 🚀"):
        st.subheader(f"🧠 جلسة جارية: {session_type}")
        
        timer_box = st.empty()
        progress_bar = st.progress(0.0)
        
        total_seconds = selected_minutes * 60
        
        # العد التنازلي مع شريط التقدم الوردي
        for remaining in range(total_seconds, -1, -1):
            mins, secs = divmod(remaining, 60)
            timer_box.markdown(f"# ⏳ `{mins:02d}:{secs:02d}`")
            
            # نسبة التقدم فـ الشريط
            progress = (total_seconds - remaining) / total_seconds
            progress_bar.progress(progress)
            
            time.sleep(1)

        # حفظ الجلسة فـ قاعدة البيانات عند الانتهاء
        db.log_focus_session(selected_minutes, session_type)

        # احتفال كامل بانتهاء الوقت 🎉🎈
        st.balloons()
        st.snow()
        st.success(f"🎉 برافو كوثر! أتممتِ جلسة {session_type} بنجاح ({selected_minutes} دقيقة). خطوة أخرى نحو المرتبة الأولى! 👑")
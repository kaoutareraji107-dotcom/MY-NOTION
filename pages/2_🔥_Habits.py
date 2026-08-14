import streamlit as st
import database as db
import os

st.set_page_config(page_title="Habits - Kaoutar OS", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    .top-goal-banner {
        background-color: #FFE4E1; border: 2px dashed #FFB6C1;
        padding: 10px; border-radius: 12px; font-weight: bold;
        color: #2D3748; text-align: center; font-size: 14px; margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #2ECC71 !important; color: white !important;
        border-radius: 10px !important; border: none !important; font-weight: bold !important;
    }
    div.stButton > button:hover { background-color: #27AE60 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-goal-banner">👑 لا تنسي هدفنا الأول: الأولى على صعيد المدرسة (19/20) - التلميذة المثالية ✨</div>', unsafe_allow_html=True)

col_img, col_main = st.columns([1, 2.5])

with col_img:
    if os.path.exists("assets/kuromi_habits.png"):
        st.image("assets/kuromi_habits.png", use_container_width=True)
    elif os.path.exists("assets/kuromi.png"):
        st.image("assets/kuromi.png", use_container_width=True)

with col_main:
    st.title("🔥 تتبع العادات اليومية")
    st.caption("عادات التلميذة المثالية هي سر الاستمرارية! 💪")

    with st.form("add_habit_form", clear_on_submit=True):
        h_name = st.text_input("اسم العادة الجديدة", placeholder="مثال: حفظ 5 مصطلحات، الرياضة...")
        if st.form_submit_button("إضافة عادة ➕"):
            if h_name.strip():
                db.add_habit(h_name.strip())
                st.success("تمت إضافة العادة!")
                st.rerun()

    st.write("---")

    habits = db.get_habits()
    if not habits:
        st.info("ابدأي بتبني عادات جديدة اليوم! 🌟")
    else:
        for habit in habits:
            col_h_name, col_h_streak, col_h_btn, col_h_del = st.columns([2, 1, 1.5, 0.5])
            
            with col_h_name:
                st.subheader(habit['name'])
            
            with col_h_streak:
                st.caption(f"🔥 {habit['streak']} أيام متتالية")
                
            with col_h_btn:
                if st.button("تسجيل إنجاز اليوم ✅", key=f"h_{habit['id']}"):
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
import streamlit as st
import database as db
import os

st.set_page_config(page_title="Tasks - Kaoutar OS", page_icon="✅", layout="wide")

# CSS المخصص
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
    if os.path.exists("assets/kuromi_tasks.png"):
        st.image("assets/kuromi_tasks.png", use_container_width=True)
    elif os.path.exists("assets/kuromi.png"):
        st.image("assets/kuromi.png", use_container_width=True)

with col_main:
    st.title("✅ إدارة المهام الدراسية")
    st.caption("شنو غادي ننجزو اليوم يا كوثر؟ 📝")

    with st.form("add_task_form", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            task_title = st.text_input("عنوان المهمة", placeholder="مثال: تحضير درس الفلسفة...")
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
import streamlit as st
import database as db
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Stats - Kaoutar OS", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    .top-goal-banner {
        background-color: #FFE4E1; border: 2px dashed #FFB6C1;
        padding: 10px; border-radius: 12px; font-weight: bold;
        color: #2D3748; text-align: center; font-size: 14px; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-goal-banner">👑 لا تنسي هدفنا الأول: الأولى على صعيد المدرسة (19/20) - التلميذة المثالية ✨</div>', unsafe_allow_html=True)

col_img, col_main = st.columns([1, 2.5])

with col_img:
    if os.path.exists("assets/kuromi_stats.png"):
        st.image("assets/kuromi_stats.png", use_container_width=True)
    elif os.path.exists("assets/kuromi.png"):
        st.image("assets/kuromi.png", use_container_width=True)

with col_main:
    st.title("📊 إحصائيات الأداء والتفوق")
    st.caption("الأرقام كتكشف حجم المجهود الجبار لي كتديري! 📈")

    all_tasks = db.get_tasks()
    total_focus = db.get_total_focus_time()

    m1, m2 = st.columns(2)
    done_count = len([t for t in all_tasks if t["status"] == "Done"])

    with m1:
        st.metric("المهام المكتملة", f"{done_count} / {len(all_tasks)}")
    with m2:
        hours = round(total_focus / 60, 1)
        st.metric("مجموع ساعات التركيز", f"{hours} ساعة 🧠")

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
        st.info("لا توجد بيانات كافية حالياً لرسم الإحصائيات.")
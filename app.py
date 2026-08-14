import streamlit as st
import random
import os
import database as db

# 1. إعداد الصفحة
st.set_page_config(
    page_title="Kaoutar OS - Home 👑", 
    page_icon="🖤", 
    layout="wide"
)

# 2. تهيئة قاعدة البيانات
db.init_db()

# 3. قائمة الاقتباسات التحفيزية الخاصة بكوثر 💡
MOTIVATIONAL_QUOTES = [
    "كوثر، النجاح ماشي حظ، النجاح هو استمرار وتعب يومي! كملي ✨",
    "كوثر، التفوق كينتظرك، كل دقيقة تركيز كتقربك للهدف 🎯",
    "كوثر، انتِ قدها! خلي هدفك دايماً قدام عينيك وقراي بذكاء 🧠🔥",
    "كوثر، العزيمة والحرص هما السر باش تكوني اللولة فـ المدرسة 💪",
    "كوثر، الاستمرارية هي اللي تصنع الفرق، كملي اليوم بطاقة إيجابية 🌟"
]

daily_quote = random.choice(MOTIVATIONAL_QUOTES)

# 4. تنسيق CSS مخصص للـ Kuromi Theme
st.markdown("""
    <style>
    /* خلفية القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #FFC0CB !important;
    }
    
    /* العبارة العلوية للهدف الذهبي */
    .top-goal-banner {
        background-color: #FFE4E1;
        border: 2px dashed #FFB6C1;
        padding: 12px 20px;
        border-radius: 15px;
        font-weight: bold;
        color: #2D3748;
        text-align: center;
        font-size: 16px;
        margin-bottom: 25px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }

    /* مربع الاقتباس اليومي لكوثر */
    .quote-box {
        background-color: #FFF0F5;
        border-right: 6px solid #2ECC71;
        padding: 15px 20px;
        border-radius: 12px;
        font-size: 17px;
        font-weight: 600;
        color: #2D3748;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    
    /* بطاقة الترحيب */
    .welcome-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #FFE4E1;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03);
    }
    </style>
""", unsafe_allow_html=True)

# 5. العبارة العلوية الثابتة فـ الأفق
st.markdown(
    '<div class="top-goal-banner">👑 لا تنسي هدفنا الأول: الأولى على صعيد المدرسة (19/20) - التلميذة المثالية ✨</div>', 
    unsafe_allow_html=True
)

# 6. الشريط الجانبي (Sidebar Navigation)
with st.sidebar:
    st.title("🎓 Kaoutar OS")
    st.caption("Kuromi Companion Edition 🖤")
    st.write("---")
    st.info("👈 اختاري المكون لي بغيتي تخدمي عليه من القائمة الفوق.")
    st.write("---")
    st.write("⚙️ Version v1.0")

# 7. محتوى الصفحة الرئيسية (صورة Kuromi + الترحيب والاقتباس)
col_img, col_content = st.columns([1.2, 2])

with col_img:
    if os.path.exists("assets/kuromi_home.png"):
        st.image("assets/kuromi_home.png", use_container_width=True)
    elif os.path.exists("assets/kuromi.png"):
        st.image("assets/kuromi.png", use_container_width=True)
    else:
        st.info("📌 ضعي صورة Kuromi داخل مجلد assets/kuromi_home.png لتظهر هنا!")

with col_content:
    st.title("🖤 مرحباً بك يا كوثر!")
    
    # مربع الاقتباس
    st.markdown(f'<div class="quote-box">💬 <b>رسالة اليوم لكِ:</b><br>{daily_quote}</div>', unsafe_allow_html=True)
    
    # كارت التقديم للوظائف
    st.markdown("""
        <div class="welcome-card">
            <h3>📌 مستعدة لليوم؟</h3>
            <p>انتقلي عبر القائمة الجانبية لتنظيم يومك الدراسية:</p>
            <ul>
                <li><b>✅ Tasks:</b> تفقدي قائمة المهام اليومية وقومي بإنجازها.</li>
                <li><b>🔥 Habits:</b> طوري عادات التلميذة المثالية وحافظي على الـ Streak.</li>
                <li><b>⏱️ Focus:</b> ابدأي جلسة تركيز (Pomodoro / Deep Work / Exam Prep).</li>
                <li><b>📊 Stats:</b> تابعي نسبة إنجازك وتفوقك.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
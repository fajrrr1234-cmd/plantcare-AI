import streamlit as st
import pandas as pd

# ==============================
# إعداد الصفحة
# ==============================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌱",
    layout="wide"
)

# ==============================
# التصميم
# ==============================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f5faf5, #eef7f0);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    text-align: center;
    padding: 20px;
}

.main-title h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 5px;
}

.main-title p {
    color: #64748b;
    font-size: 18px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    border: 1px solid #e5eee7;
    margin-bottom: 20px;
}

.good {
    background: #ecfdf3;
    border: 1px solid #bbf7d0;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
}

.warning {
    background: #fff8e7;
    border: 1px solid #fde68a;
    padding: 25px;
    border-radius: 20px;
}

.result-title {
    font-size: 27px;
    font-weight: 800;
}

.info-box {
    background: #f8fafc;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# بيانات النباتات
# ==============================

plants = {

    "🍅 طماطم": {
        "soil": 40,
        "light": 60,
        "min_temp": 18,
        "max_temp": 30
    },

    "🌿 نعناع": {
        "soil": 45,
        "light": 40,
        "min_temp": 15,
        "max_temp": 28
    },

    "🌹 ورد": {
        "soil": 35,
        "light": 55,
        "min_temp": 16,
        "max_temp": 30
    },

    "🌵 صبار": {
        "soil": 15,
        "light": 50,
        "min_temp": 15,
        "max_temp": 35
    }
}


# ==============================
# العنوان
# ==============================

st.markdown("""
<div class="main-title">

<h1>🌱 PlantCare AI</h1>

<p>
نظام ذكي لمراقبة صحة النباتات وتحليل احتياجاتها
</p>

</div>
""", unsafe_allow_html=True)

st.divider()


# ==============================
# تعريف المشروع
# ==============================

st.markdown("""
<div class="card">

<h3>🌿 مرحبًا بك في PlantCare AI</h3>

<p>
يساعدك النظام على معرفة حالة نباتك من خلال تحليل
رطوبة التربة ودرجة الحرارة وكمية الإضاءة.
بعد إدخال البيانات، يقوم النظام بتحليلها وتقديم
توصية مناسبة للعناية بالنبات.
</p>

</div>
""", unsafe_allow_html=True)


# ==============================
# الأعمدة الرئيسية
# ==============================

input_col, result_col = st.columns([1, 1.4])


# ==============================
# إدخال البيانات
# ==============================

with input_col:

    st.markdown("""
    <div class="card">

    <h3>📋 بيانات النبات</h3>

    </div>
    """, unsafe_allow_html=True)

    plant = st.selectbox(
        "🌿 اختر نوع النبات",
        list(plants.keys())
    )

    soil = st.slider(
        "💧 رطوبة التربة",
        0,
        100,
        50,
        help="نسبة رطوبة التربة الحالية"
    )

    temperature = st.slider(
        "🌡️ درجة الحرارة",
        0,
        50,
        25,
        help="درجة الحرارة المحيطة بالنبات"
    )

    light = st.slider(
        "☀️ مستوى الإضاءة",
        0,
        100,
        70,
        help="نسبة كمية الضوء المتوفرة للنبات"
    )

    analyze = st.button(
        "🔍 تحليل صحة النبات",
        use_container_width=True
    )


# ==============================
# القراءات
# ==============================

with result_col:

    st.markdown("""
    <div class="card">

    <h3>📊 القراءات الحالية</h3>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💧 الرطوبة",
            f"{soil}%"
        )

    with col2:
        st.metric(
            "🌡️ الحرارة",
            f"{temperature}°C"
        )

    with col3:
        st.metric(
            "☀️ الإضاءة",
            f"{light}%"
        )

    chart = pd.DataFrame({
        "المؤشر": [
            "رطوبة التربة",
            "الإضاءة"
        ],
        "النسبة": [
            soil,
            light
        ]
    })

    st.bar_chart(
        chart,
        x="المؤشر",
        y="النسبة"
    )


# ==============================
# التحليل
# ==============================

if analyze:

    plant_data = plants[plant]

    problems = []
    recommendations = []

    # فحص الرطوبة

    if soil < plant_data["soil"]:

        problems.append(
            "💧 رطوبة التربة منخفضة"
        )

        recommendations.append(
            "قم بري النبات وزيادة رطوبة التربة."
        )

    # فحص الإضاءة

    if light < plant_data["light"]:

        problems.append(
            "☀️ مستوى الإضاءة منخفض"
        )

        recommendations.append(
            "ضع النبات في مكان يحصل على إضاءة أكثر."
        )

    # فحص الحرارة

    if temperature < plant_data["min_temp"]:

        problems.append(
            "🥶 درجة الحرارة منخفضة"
        )

        recommendations.append(
            "حاول وضع النبات في مكان أكثر دفئًا."
        )

    elif temperature > plant_data["max_temp"]:

        problems.append(
            "🔥 درجة الحرارة مرتفعة"
        )

        recommendations.append(
            "أبعد النبات عن مصدر الحرارة وحاول تبريد المكان."
        )


    # ==============================
    # عرض النتيجة
    # ==============================

    st.divider()

    st.subheader("🤖 نتيجة التحليل الذكي")


    if len(problems) == 0:

        st.markdown("""
        <div class="good">

        <div class="result-title">
        🌱 النبات بحالة ممتازة
        </div>

        <p>
        جميع المؤشرات الحالية مناسبة للنبات.
        استمر في المحافظة على هذه الظروف.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.success(
            "تم تحليل البيانات بنجاح ✅"
        )


    else:

        st.markdown("""
        <div class="warning">

        <div class="result-title">
        ⚠️ النبات يحتاج إلى عناية
        </div>

        <p>
        تم اكتشاف بعض المؤشرات التي تحتاج إلى تحسين.
        </p>

        </div>
        """, unsafe_allow_html=True)


        st.write("### 🔎 المشكلات المكتشفة")

        for problem in problems:

            st.warning(problem)


        st.write("### 💡 التوصيات")

        for recommendation in recommendations:

            st.info(recommendation)


# ==============================
# معلومات المشروع
# ==============================

st.divider()

st.markdown("""
<div class="card">

<h3>🧠 معلومات المشروع</h3>

<div class="info-box">

<p>
<strong>المشكلة:</strong>
صعوبة معرفة احتياجات النبات بشكل دقيق.
</p>

<p>
<strong>المدخلات:</strong>
نوع النبات، رطوبة التربة، درجة الحرارة، والإضاءة.
</p>

<p>
<strong>التحليل:</strong>
مقارنة البيانات المدخلة بالاحتياجات المناسبة لكل نوع من النباتات.
</p>

<p>
<strong>المخرجات:</strong>
حالة النبات والتوصيات المناسبة للعناية به.
</p>

<p>
<strong>الفئة المستفيدة:</strong>
أصحاب النباتات، المزارعون، والمهتمون بالزراعة.
</p>

</div>

</div>
""", unsafe_allow_html=True)


# ==============================
# التذييل
# ==============================

st.markdown("""
<div style="text-align:center; color:#64748b; padding:20px;">

🌱 PlantCare AI

<br>

نظام ذكي لمراقبة صحة النباتات

</div>
""", unsafe_allow_html=True)
st.markdown("## 📷 صوري نبتتك")

photo = st.camera_input("اضغطي هنا لفتح الكاميرا وتصوير النبتة")

if photo is not None:
    st.image(photo, caption="🌱 صورة النبتة", use_container_width=True)
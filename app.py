import streamlit as st
import pandas as pd

# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌱",
    layout="wide"
)

# =========================
# التصميم
# =========================

st.markdown("""
<style>
.stApp {
    direction: rtl;
    text-align: right;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-bottom: 20px;
}

.result {
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# العنوان
# =========================

st.markdown(
    '<div class="main-title">🌱 PlantCare AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">نظام ذكي لمراقبة صحة النباتات</div>',
    unsafe_allow_html=True
)

st.write(
    "يساعدك النظام على معرفة حالة النبتة اعتمادًا على "
    "رطوبة التربة والإضاءة ودرجة الحرارة."
)

st.divider()

# =========================
# تصوير النبتة
# =========================

st.markdown("## 📷 صوري نبتتك")

photo = st.camera_input(
    "اضغطي هنا لفتح الكاميرا وتصوير النبتة"
)

if photo is not None:
    st.image(
        photo,
        caption="🌱 صورة النبتة",
        use_container_width=True
    )

    st.success("✅ تم التقاط صورة النبتة بنجاح!")

st.divider()

# =========================
# بيانات النبتة
# =========================

st.markdown("## 🌿 بيانات النبتة")

plant_type = st.selectbox(
    "اختاري نوع النبتة:",
    [
        "طماطم 🍅",
        "نعناع 🌿",
        "ورد 🌹",
        "صبار 🌵"
    ]
)

soil = st.slider(
    "💧 رطوبة التربة (%)",
    min_value=0,
    max_value=100,
    value=50
)

light = st.slider(
    "☀️ مستوى الإضاءة (%)",
    min_value=0,
    max_value=100,
    value=60
)

temperature = st.number_input(
    "🌡️ درجة الحرارة (°C)",
    min_value=-10.0,
    max_value=60.0,
    value=25.0,
    step=0.5
)

# =========================
# قواعد النباتات
# =========================

rules = {
    "طماطم 🍅": {
        "soil": 40,
        "light": 60,
        "min_temp": 18,
        "max_temp": 30
    },

    "نعناع 🌿": {
        "soil": 45,
        "light": 40,
        "min_temp": 15,
        "max_temp": 28
    },

    "ورد 🌹": {
        "soil": 35,
        "light": 55,
        "min_temp": 16,
        "max_temp": 30
    },

    "صبار 🌵": {
        "soil": 15,
        "light": 50,
        "min_temp": 15,
        "max_temp": 35
    }
}

rule = rules[plant_type]

# =========================
# التحليل
# =========================

st.divider()

st.markdown("## 🤖 تحليل حالة النبتة")

if st.button("🔎 تحليل النبتة", use_container_width=True):

    problems = []
    recommendations = []

    # الماء
    if soil < rule["soil"]:
        problems.append("💧 التربة جافة وقد تحتاج النبتة إلى ماء.")
        recommendations.append("اسقي النبتة تدريجيًا وتابعي رطوبة التربة.")

    elif soil > rule["soil"] + 35:
        problems.append("💦 رطوبة التربة مرتفعة وقد يكون هناك زيادة في الماء.")
        recommendations.append("خففي الري وتحققي من تصريف الماء.")

    # الإضاءة
    if light < rule["light"]:
        problems.append("☀️ الإضاءة منخفضة.")
        recommendations.append("ضعي النبتة في مكان يحصل على إضاءة مناسبة.")

    # الحرارة
    if temperature < rule["min_temp"]:
        problems.append("🥶 درجة الحرارة منخفضة.")
        recommendations.append("انقلي النبتة إلى مكان أكثر دفئًا.")

    elif temperature > rule["max_temp"]:
        problems.append("🔥 درجة الحرارة مرتفعة.")
        recommendations.append("حاولي وضع النبتة في مكان أكثر اعتدالًا.")

    # النتيجة
    if len(problems) == 0:
        status = "🌱 النبات بحالة جيدة"
        st.success(status)

    else:
        status = "⚠️ توجد بعض الأمور التي تحتاج إلى الانتباه"
        st.warning(status)

    # عرض المشاكل
    if problems:

        st.markdown("### 🔍 الملاحظات")

        for problem in problems:
            st.write(problem)

    # التوصيات
    if recommendations:

        st.markdown("### 💡 التوصيات")

        for recommendation in recommendations:
            st.write("• " + recommendation)

    else:

        st.info(
            "استمري على روتين العناية الحالي وراقبي النبتة بشكل مستمر."
        )

    # =========================
    # جدول البيانات
    # =========================

    st.markdown("### 📊 بيانات التحليل")

    data = {
        "العنصر": [
            "نوع النبتة",
            "رطوبة التربة",
            "الإضاءة",
            "درجة الحرارة"
        ],
        "القيمة": [
            plant_type,
            f"{soil}%",
            f"{light}%",
            f"{temperature}°C"
        ]
    }

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# =========================
# معلومات المشروع
# =========================

st.divider()

st.markdown("## ℹ️ عن المشروع")

st.write("""
PlantCare AI هو نموذج أولي لنظام ذكي يساعد أصحاب النباتات
على متابعة حالة نباتاتهم.

يعتمد النظام على تحليل بيانات رطوبة التربة والإضاءة ودرجة الحرارة
وفقًا لاحتياجات كل نوع من النباتات.

📷 يمكن استخدام الكاميرا لالتقاط صورة للنبتة.

🤖 التحليل الحالي يعتمد على قواعد ذكية محددة لكل نوع نبات،
ويمكن تطوير المشروع مستقبلًا باستخدام نماذج تعلم آلي ورؤية حاسوبية
للتعرف على النبات وتحليل الصور تلقائيًا.
""")

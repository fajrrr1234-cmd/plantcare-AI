import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌱",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    direction: rtl;
    text-align: right;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 19px;
    margin-bottom: 25px;
}

.result {
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🌱 PlantCare AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">نظام ذكي لمراقبة صحة النباتات الداخلية</div>',
    unsafe_allow_html=True
)

st.write(
    "صوّري نبتتك، ثم اختاري نوعها ليحلل النظام احتياجاتها "
    "من الماء والإضاءة ودرجة الحرارة."
)

st.divider()

# 📷 الكاميرا
st.markdown("## 📷 صوري نبتتك")

photo = st.camera_input(
    "اضغطي هنا لفتح الكاميرا وتصوير النبتة"
)

if photo is not None:
    st.image(
        photo,
        caption="🌿 صورة النبتة",
        use_container_width=True
    )

    st.success("✅ تم التقاط صورة النبتة بنجاح!")

st.divider()

# 🌿 اختيار النبات
st.markdown("## 🌿 التعرف على النبتة")

plant_type = st.selectbox(
    "اختاري نوع النبتة:",
    [
        "بوتس 🌿",
        "مونستيرا 🌱",
        "سانسيفيريا 🌵",
        "زنبق السلام 🌸",
        "نبات العنكبوت 🪴"
    ]
)

plant_data = {
    "بوتس 🌿": {
        "soil": 40,
        "light": 35,
        "min_temp": 18,
        "max_temp": 30
    },

    "مونستيرا 🌱": {
        "soil": 40,
        "light": 50,
        "min_temp": 18,
        "max_temp": 30
    },

    "سانسيفيريا 🌵": {
        "soil": 20,
        "light": 35,
        "min_temp": 15,
        "max_temp": 32
    },

    "زنبق السلام 🌸": {
        "soil": 45,
        "light": 30,
        "min_temp": 18,
        "max_temp": 30
    },

    "نبات العنكبوت 🪴": {
        "soil": 40,
        "light": 40,
        "min_temp": 15,
        "max_temp": 27
    }
}

data = plant_data[plant_type]

st.success(f"🌿 تم اختيار: **{plant_type}**")

st.divider()

# 📊 البيانات
st.markdown("## 📊 بيانات النبتة")

soil = st.slider(
    "💧 رطوبة التربة (%)",
    0,
    100,
    50
)

light = st.slider(
    "☀️ مستوى الإضاءة (%)",
    0,
    100,
    60
)

temperature = st.number_input(
    "🌡️ درجة الحرارة (°C)",
    -10.0,
    60.0,
    25.0,
    0.5
)

st.divider()

# 🤖 التحليل
if st.button(
    "🔎 تحليل صحة النبتة",
    use_container_width=True
):

    problems = []
    recommendations = []

    if soil < data["soil"]:
        problems.append(
            "💧 التربة جافة."
        )
        recommendations.append(
            "اسقي البوتس تدريجيًا وتابعي رطوبة التربة."
        )

    elif soil > data["soil"] + 35:
        problems.append(
            "💦 رطوبة التربة مرتفعة."
        )
        recommendations.append(
            "خففي الري وتأكدي من وجود تصريف جيد للماء."
        )

    if light < data["light"]:
        problems.append(
            "☀️ الإضاءة منخفضة."
        )
        recommendations.append(
            "ضعي البوتس بالقرب من نافذة بإضاءة غير مباشرة."
        )

    if temperature < data["min_temp"]:
        problems.append(
            "🥶 درجة الحرارة منخفضة."
        )
        recommendations.append(
            "حاولي إبقاء النبتة في مكان أكثر دفئًا."
        )

    elif temperature > data["max_temp"]:
        problems.append(
            "🔥 درجة الحرارة مرتفعة."
        )
        recommendations.append(
            "أبعدي النبتة عن الحرارة وأشعة الشمس المباشرة."
        )

    st.markdown("## 🌱 النتيجة")

    if len(problems) == 0:
        st.success(
            "🌱 البوتس بحالة ممتازة!"
        )
        st.write(
            "استمري على روتين العناية الحالي."
        )

    else:
        st.warning(
            "⚠️ البوتس تحتاج إلى بعض الاهتمام."
        )

        st.markdown("### 🔍 الملاحظات")

        for problem in problems:
            st.write(problem)

        st.markdown("### 💡 التوصيات")

        for recommendation in recommendations:
            st.write("• " + recommendation)

    st.markdown("### 📋 ملخص التحليل")

    summary = pd.DataFrame({
        "العنصر": [
            "النبتة",
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
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.markdown("## ℹ️ عن المشروع")

st.write("""
PlantCare AI هو نموذج أولي لنظام ذكي لمراقبة صحة النباتات الداخلية.

📷 يسمح للمستخدم بتصوير النبتة.

🌿 يمكن اختيار نوع النبتة، مثل البوتس.

💧☀️🌡️ يحلل النظام رطوبة التربة والإضاءة ودرجة الحرارة.

🤖 ثم يقدم توصيات تساعد المستخدم على العناية بالنبتة.
""")

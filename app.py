import streamlit as st
import pandas as pd
from PIL import Image
from transformers import pipeline

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

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.box {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🌱 PlantCare AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">نظام ذكي للتعرف على النباتات ومراقبة صحتها</div>',
    unsafe_allow_html=True
)

st.write(
    "📷 صوّري نبتتك وسيحاول النظام التعرف على نوعها، "
    "ثم يعطيك توصيات مناسبة للعناية بها."
)

st.divider()

# تحميل نموذج التعرف على النباتات
@st.cache_resource
def load_model():
    return pipeline(
        "image-classification",
        model="umutbozdag/plant-identity"
    )

st.markdown("## 📷 صوري نبتتك")

photo = st.camera_input(
    "اضغطي هنا لفتح الكاميرا وتصوير النبتة"
)

# معلومات العناية بالنباتات الداخلية
plant_care = {
    "monstera": {
        "name": "مونستيرا 🌿",
        "soil": 40,
        "light": 50,
        "min_temp": 18,
        "max_temp": 30
    },
    "pothos": {
        "name": "بوتس 🌿",
        "soil": 40,
        "light": 35,
        "min_temp": 18,
        "max_temp": 30
    },
    "peace lily": {
        "name": "زنبق السلام 🌱",
        "soil": 45,
        "light": 30,
        "min_temp": 18,
        "max_temp": 30
    },
    "snake plant": {
        "name": "سانسيفيريا 🌵",
        "soil": 20,
        "light": 35,
        "min_temp": 15,
        "max_temp": 32
    },
    "zz plant": {
        "name": "نبتة ZZ 🌿",
        "soil": 25,
        "light": 30,
        "min_temp": 15,
        "max_temp": 30
    },
    "spider plant": {
        "name": "نبات العنكبوت 🌱",
        "soil": 40,
        "light": 40,
        "min_temp": 15,
        "max_temp": 27
    }
}

if photo is not None:

    image = Image.open(photo).convert("RGB")

    st.image(
        image,
        caption="🌱 صورة النبتة",
        use_container_width=True
    )

    st.success("✅ تم التقاط الصورة!")

    with st.spinner("🤖 جاري التعرف على النبتة..."):

        try:
            model = load_model()

            results = model(image, top_k=3)

            best_result = results[0]

            predicted_name = best_result["label"]
            confidence = best_result["score"] * 100

            st.markdown("## 🔎 نتيجة التعرف")

            st.success(
                f"🌿 النبتة المتوقعة: **{predicted_name}**"
            )

            st.metric(
                "نسبة الثقة",
                f"{confidence:.1f}%"
            )

            st.markdown("### 🤖 احتمالات التعرف")

            for result in results:
                st.write(
                    f"🌱 {result['label']} — "
                    f"{result['score'] * 100:.1f}%"
                )

            # البحث عن بيانات العناية
            predicted_lower = predicted_name.lower()

            matched_plant = None

            for key in plant_care:

                if key in predicted_lower or predicted_lower in key:
                    matched_plant = plant_care[key]
                    break

            if matched_plant:

                st.divider()

                st.markdown("## 🌿 بيانات العناية")

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

                if st.button(
                    "🔎 تحليل صحة النبتة",
                    use_container_width=True
                ):

                    problems = []
                    recommendations = []

                    if soil < matched_plant["soil"]:
                        problems.append(
                            "💧 التربة جافة وقد تحتاج النبتة إلى ماء."
                        )
                        recommendations.append(
                            "اسقي النبتة تدريجيًا وتابعي رطوبة التربة."
                        )

                    elif soil > matched_plant["soil"] + 35:
                        problems.append(
                            "💦 رطوبة التربة مرتفعة."
                        )
                        recommendations.append(
                            "خففي الري وتحققي من تصريف الماء."
                        )

                    if light < matched_plant["light"]:
                        problems.append(
                            "☀️ الإضاءة منخفضة."
                        )
                        recommendations.append(
                            "ضعي النبتة في مكان أكثر إضاءة."
                        )

                    if temperature < matched_plant["min_temp"]:
                        problems.append(
                            "🥶 درجة الحرارة منخفضة."
                        )
                        recommendations.append(
                            "انقلي النبتة إلى مكان أكثر دفئًا."
                        )

                    elif temperature > matched_plant["max_temp"]:
                        problems.append(
                            "🔥 درجة الحرارة مرتفعة."
                        )
                        recommendations.append(
                            "ضعي النبتة في مكان أكثر اعتدالًا."
                        )

                    st.markdown("## 🌱 حالة النبتة")

                    if not problems:
                        st.success(
                            "🌱 النبات بحالة جيدة!"
                        )
                    else:
                        st.warning(
                            "⚠️ توجد بعض الأمور التي تحتاج إلى الانتباه."
                        )

                    if problems:

                        st.markdown("### 🔍 الملاحظات")

                        for problem in problems:
                            st.write(problem)

                    if recommendations:

                        st.markdown("### 💡 التوصيات")

                        for recommendation in recommendations:
                            st.write("• " + recommendation)

            else:

                st.info(
                    "ℹ️ تم التعرف على النبتة، "
                    "لكن لا توجد لدينا بيانات عناية مخصصة لها حاليًا."
                )

        except Exception as e:

            st.error(
                "❌ حدث خطأ أثناء التعرف على النبتة."
            )

            st.write(str(e))

st.divider()

st.markdown("## ℹ️ عن المشروع")

st.write("""
PlantCare AI هو نموذج أولي لنظام ذكي يساعد أصحاب النباتات
على التعرف على نباتاتهم ومتابعة احتياجاتها.

📷 يستخدم صورة النبتة للتعرف على نوعها.

🤖 يستخدم نموذج تعلم آلي للتعرف على النبات.

🌱 بعد التعرف على النبات، يستخدم النظام بيانات العناية
لتقديم توصيات حول الماء والإضاءة ودرجة الحرارة.

🚀 يمكن تطوير المشروع مستقبلًا ليشمل التعرف على أمراض النباتات
وتحليل صور الأوراق بشكل أكثر دقة.
""")

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
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🌱 PlantCare AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">نظام ذكي للتعرف على النباتات الداخلية ومراقبة صحتها</div>',
    unsafe_allow_html=True
)

st.write(
    "📷 صوّري النبتة، وسيحاول الذكاء الاصطناعي التعرف عليها تلقائيًا."
)

st.divider()

# تحميل نموذج التعرف مرة واحدة
@st.cache_resource
def load_model():
    return pipeline(
        "image-classification",
        model="umutbozdag/plant-identity"
    )

# بيانات العناية
plant_data = {
    "Pothos": {
        "name": "البوتس 🌿",
        "soil": 40,
        "light": 35,
        "min_temp": 18,
        "max_temp": 30
    },
    "Monstera deliciosa": {
        "name": "المونستيرا 🌱",
        "soil": 40,
        "light": 50,
        "min_temp": 18,
        "max_temp": 30
    },
    "Snake plant": {
        "name": "السانسيفيريا 🌵",
        "soil": 20,
        "light": 35,
        "min_temp": 15,
        "max_temp": 32
    },
    "Peace lily": {
        "name": "زنبق السلام 🌸",
        "soil": 45,
        "light": 30,
        "min_temp": 18,
        "max_temp": 30
    },
    "Spider plant": {
        "name": "نبات العنكبوت 🪴",
        "soil": 40,
        "light": 40,
        "min_temp": 15,
        "max_temp": 27
    },
    "ZZ plant": {
        "name": "نبتة ZZ 🌿",
        "soil": 25,
        "light": 30,
        "min_temp": 15,
        "max_temp": 30
    }
}

st.markdown("## 📷 صوري نبتتك")

photo = st.camera_input(
    "اضغطي هنا لفتح الكاميرا وتصوير النبتة"
)

if photo is not None:

    image = Image.open(photo).convert("RGB")

    st.image(
        image,
        caption="🌿 صورة النبتة",
        use_container_width=True
    )

    st.success("✅ تم التقاط الصورة!")

    st.markdown("## 🤖 التعرف على النبتة")

    with st.spinner("🔎 جاري التعرف على النبتة..."):

        try:

            model = load_model()

            results = model(image, top_k=5)

            best = results[0]

            label = best["label"]
            confidence = best["score"] * 100

            # البحث عن النبات المطابق
            matched = None

            for key in plant_data:

                if key.lower() in label.lower() or label.lower() in key.lower():
                    matched = plant_data[key]
                    break

            if matched is not None:

                st.success(
                    f"🌿 تعرفت على النبتة: **{matched['name']}**"
                )

                st.metric(
                    "نسبة الثقة",
                    f"{confidence:.1f}%"
                )

            else:

                st.warning(
                    f"🌱 النموذج يتوقع: **{label}**"
                )

                st.info(
                    "هذه النبتة ليست ضمن أنواع العناية الموجودة في المشروع حاليًا."
                )

            st.markdown("### 🔍 احتمالات التعرف")

            for result in results:
                st.write(
                    f"🌿 {result['label']} — "
                    f"{result['score'] * 100:.1f}%"
                )

            # إذا تعرفنا على النبات نبدأ تحليل صحته
            if matched is not None:

                st.divider()

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

                if st.button(
                    "🔎 تحليل صحة النبتة",
                    use_container_width=True
                ):

                    problems = []
                    recommendations = []

                    if soil < matched["soil"]:
                        problems.append(
                            "💧 التربة جافة."
                        )
                        recommendations.append(
                            "اسقي النبتة تدريجيًا وتابعي رطوبة التربة."
                        )

                    elif soil > matched["soil"] + 35:
                        problems.append(
                            "💦 رطوبة التربة مرتفعة."
                        )
                        recommendations.append(
                            "خففي الري وتأكدي من تصريف الماء."
                        )

                    if light < matched["light"]:
                        problems.append(
                            "☀️ الإضاءة منخفضة."
                        )
                        recommendations.append(
                            "ضعي النبتة في مكان بإضاءة مناسبة وغير مباشرة."
                        )

                    if temperature < matched["min_temp"]:
                        problems.append(
                            "🥶 درجة الحرارة منخفضة."
                        )
                        recommendations.append(
                            "حاولي وضع النبتة في مكان أكثر دفئًا."
                        )

                    elif temperature > matched["max_temp"]:
                        problems.append(
                            "🔥 درجة الحرارة مرتفعة."
                        )
                        recommendations.append(
                            "أبعدي النبتة عن الحرارة وأشعة الشمس المباشرة."
                        )

                    st.markdown("## 🌱 النتيجة")

                    if not problems:

                        st.success(
                            f"🌱 {matched['name']} بحالة ممتازة!"
                        )

                    else:

                        st.warning(
                            "⚠️ النبتة تحتاج إلى بعض الاهتمام."
                        )

                        st.markdown("### 🔍 الملاحظات")

                        for problem in problems:
                            st.write(problem)

                        st.markdown("### 💡 التوصيات")

                        for recommendation in recommendations:
                            st.write("• " + recommendation)

                    summary = pd.DataFrame({
                        "العنصر": [
                            "نوع النبتة",
                            "رطوبة التربة",
                            "الإضاءة",
                            "درجة الحرارة"
                        ],
                        "القيمة": [
                            matched["name"],
                            f"{soil}%",
                            f"{light}%",
                            f"{temperature}°C"
                        ]
                    })

                    st.markdown("### 📋 ملخص التحليل")

                    st.dataframe(
                        summary,
                        use_container_width=True,
                        hide_index=True
                    )

        except Exception as e:

            st.error(
                "❌ حدث خطأ أثناء تشغيل نموذج التعرف."
            )

            st.code(str(e))

st.divider()

st.markdown("## ℹ️ عن المشروع")

st.write("""
PlantCare AI هو نظام ذكي لمراقبة صحة النباتات الداخلية.

📷 يصور المستخدم النبتة بالكاميرا.

🤖 يستخدم النظام نموذج تعلم آلي للتعرف على نوع النبتة من الصورة.

💧☀️🌡️ بعد التعرف عليها، يحلل النظام رطوبة التربة والإضاءة ودرجة الحرارة.

🌱 ثم يقدم توصيات مناسبة للعناية بالنبتة.
""")

import streamlit as st
import pandas as pd
from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from huggingface_hub import hf_hub_download
import json


# ==========================================
# إعداد الصفحة
# ==========================================

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
    '<div class="subtitle">نظام ذكي للتعرف على النباتات ومراقبة صحتها</div>',
    unsafe_allow_html=True
)

st.write(
    "📷 صوّري النبتة وسيحاول الذكاء الاصطناعي التعرف عليها تلقائيًا."
)

st.divider()


# ==========================================
# تحميل نموذج الذكاء الاصطناعي
# ==========================================

@st.cache_resource
def load_model():

    model = models.resnet18(
        weights=None,
        num_classes=1081
    )

    model_path = hf_hub_download(
        repo_id="cpoisson/plantnet300k-resnet18",
        filename="plantnet_resnet18.pth"
    )

    model.load_state_dict(
        torch.load(
            model_path,
            map_location="cpu",
            weights_only=True
        )
    )

    model.eval()

    return model


# ==========================================
# تحميل أسماء الأنواع
# ==========================================

@st.cache_data
def load_labels():

    labels_path = hf_hub_download(
        repo_id="cpoisson/plantnet300k-resnet18",
        filename="plantnet300K_species_id_2_name.json"
    )

    with open(
        labels_path,
        "r",
        encoding="utf-8"
    ) as f:
        species_map = json.load(f)

    return [
        species_map[key]
        for key in sorted(
            species_map,
            key=lambda x: int(x)
        )
    ]


# ==========================================
# قاعدة بيانات 100 نبتة
#
# الاسم العلمي,
# الاسم العربي,
# رطوبة التربة المطلوبة,
# الإضاءة,
# أقل حرارة,
# أعلى حرارة
# ==========================================

plants = [

("Epipremnum aureum", "البوتس 🌿", 40, 35, 18, 30),
("Monstera deliciosa", "المونستيرا 🌱", 40, 50, 18, 30),
("Dracaena trifasciata", "السانسيفيريا 🌵", 20, 35, 15, 32),
("Spathiphyllum wallisii", "زنبق السلام 🌸", 45, 30, 18, 30),
("Chlorophytum comosum", "نبات العنكبوت 🪴", 40, 40, 15, 27),
("Zamioculcas zamiifolia", "نبتة ZZ 🌿", 25, 30, 15, 30),
("Peperomia serpens", "بيبروميا سيربنز 🌿", 35, 45, 18, 30),
("Peperomia obtusifolia", "بيبروميا 🌿", 35, 40, 18, 30),
("Dracaena sanderiana", "ساق البامبو 🎋", 40, 30, 18, 30),
("Dracaena braunii", "البامبو 🎋", 40, 30, 18, 30),

("Aloe vera", "الألوفيرا 🌵", 20, 65, 15, 30),
("Ficus elastica", "نبات المطاط 🌿", 40, 50, 18, 30),
("Ficus lyrata", "فيكس ليراتا 🌿", 40, 65, 18, 30),
("Calathea orbifolia", "كالاتيا أوربيفوليا 🌿", 55, 30, 18, 28),
("Calathea roseopicta", "كالاتيا روزيوبيكتا 🌿", 55, 30, 18, 28),
("Fittonia albivenis", "فيتونيا 🌿", 55, 30, 18, 28),
("Crassula ovata", "نبات اليشم 🌱", 20, 60, 15, 30),
("Anthurium andraeanum", "الأنثوريوم 🌺", 50, 40, 18, 30),
("Nephrolepis exaltata", "سرخس بوسطن 🌿", 60, 35, 16, 27),
("Philodendron hederaceum", "فيلودندرون 🌿", 45, 40, 18, 30),

("Dieffenbachia seguine", "ديفنباخيا 🌿", 45, 35, 18, 30),
("Begonia rex", "بيغونيا ريكس 🌸", 45, 40, 18, 28),
("Begonia maculata", "بيغونيا ماكيولاتا 🌸", 45, 45, 18, 28),
("Tradescantia zebrina", "ترادسكانتيا 🌿", 35, 50, 18, 30),
("Syngonium podophyllum", "سينغونيوم 🌿", 45, 40, 18, 30),
("Aglaonema commutatum", "أجلونيما 🌿", 45, 30, 18, 30),
("Schefflera arboricola", "شيفليرا 🌿", 35, 45, 18, 30),
("Yucca elephantipes", "يوكا 🌴", 25, 60, 15, 30),
("Cordyline fruticosa", "كورديلين 🌿", 40, 50, 18, 30),
("Croton", "كروتون 🍂", 45, 60, 18, 30),

("Hoya carnosa", "هويا 🌿", 30, 50, 18, 30),
("Dischidia nummularia", "ديسكيديا 🌿", 30, 45, 18, 30),
("Ceropegia woodii", "سلسلة القلوب 💚", 20, 55, 15, 30),
("Senecio rowleyanus", "سلسلة اللؤلؤ 🌿", 20, 60, 15, 30),
("Epipremnum pinnatum", "بوتس متسلق 🌿", 40, 45, 18, 30),
("Scindapsus pictus", "سكندابسوس 🌿", 40, 40, 18, 30),
("Rhaphidophora tetrasperma", "رافيدوفورا 🌿", 40, 50, 18, 30),
("Philodendron erubescens", "فيلودندرون أحمر 🌿", 45, 45, 18, 30),
("Philodendron gloriosum", "فيلودندرون جلوريوزوم 🌿", 50, 40, 18, 30),
("Philodendron selloum", "فيلودندرون سيلوم 🌿", 45, 45, 18, 30),

("Alocasia amazonica", "ألوكاسيا 🌿", 50, 45, 18, 30),
("Alocasia macrorrhizos", "ألوكاسيا 🌿", 50, 50, 18, 30),
("Colocasia esculenta", "كولوكاسيا 🌿", 60, 50, 18, 30),
("Dieffenbachia maculata", "ديفنباخيا مبقعة 🌿", 45, 35, 18, 30),
("Maranta leuconeura", "مارانتا 🌿", 55, 30, 18, 28),
("Stromanthe sanguinea", "سترومانثي 🌿", 55, 30, 18, 28),
("Ctenanthe burle-marxii", "سنتانثي 🌿", 55, 30, 18, 28),
("Pilea peperomioides", "بيليا 🌿", 40, 45, 18, 28),
("Pilea cadierei", "بيليا ألمنيوم 🌿", 45, 40, 18, 28),
("Peperomia caperata", "بيبروميا مجعدة 🌿", 40, 35, 18, 28),

("Peperomia argyreia", "بيبروميا البطيخ 🍉", 40, 40, 18, 28),
("Pachira aquatica", "شجرة المال 🌳", 40, 45, 18, 30),
("Plectranthus verticillatus", "اللبلاب السويدي 🌿", 40, 45, 15, 28),
("Asparagus setaceus", "سرخس الهليون 🌿", 45, 40, 18, 28),
("Adiantum raddianum", "سرخس كزبرة البئر 🌿", 60, 30, 16, 27),
("Asplenium nidus", "سرخس عش الطائر 🌿", 55, 30, 18, 28),
("Davallia fejeensis", "سرخس الأرنب 🌿", 55, 35, 16, 27),
("Platycerium bifurcatum", "سرخس قرن الأيل 🌿", 45, 40, 18, 30),
("Tillandsia ionantha", "نبتة الهواء 🌿", 20, 50, 15, 30),
("Tillandsia xerographica", "نبتة هوائية 🌿", 20, 55, 15, 30),

("Echeveria elegans", "إشيفيريا 🌵", 15, 70, 10, 30),
("Haworthia cooperi", "هاورثيا 🌵", 15, 55, 10, 30),
("Haworthia attenuata", "هاورثيا 🌵", 15, 55, 10, 30),
("Gasteria carinata", "جاستيريا 🌵", 20, 50, 10, 30),
("Kalanchoe blossfeldiana", "كالانشو 🌺", 20, 60, 12, 30),
("Schlumbergera truncata", "صبار عيد الميلاد 🌵", 30, 45, 15, 28),
("Mammillaria", "ماميلاريا 🌵", 15, 70, 10, 32),
("Opuntia microdasys", "صبار الأرنب 🌵", 15, 75, 10, 35),
("Gymnocalycium mihanovichii", "صبار القمر 🌵", 15, 65, 10, 32),
("Euphorbia milii", "شوكة المسيح 🌵", 20, 65, 15, 32),

("Saintpaulia ionantha", "البنفسج الإفريقي 🌸", 45, 35, 18, 27),
("Phalaenopsis", "الأوركيد 🌸", 45, 40, 18, 30),
("Dendrobium", "أوركيد ديندروبيوم 🌸", 40, 50, 18, 30),
("Gardenia jasminoides", "الجاردينيا 🌸", 55, 55, 18, 30),
("Jasminum sambac", "الياسمين العربي 🌸", 45, 60, 18, 32),
("Hibiscus rosa-sinensis", "الكركديه 🌺", 50, 65, 18, 32),
("Bougainvillea", "الجهنمية 🌺", 25, 70, 15, 35),
("Pelargonium", "إبرة الراعي 🌸", 30, 60, 15, 30),
("Impatiens walleriana", "القطيفة 🌸", 55, 35, 18, 28),
("Primula vulgaris", "زهرة الربيع 🌸", 50, 35, 10, 22),

("Ficus benjamina", "فيكس بنجامينا 🌳", 40, 50, 18, 30),
("Ficus microcarpa", "فيكس ميكروكاربا 🌳", 35, 50, 18, 30),
("Schefflera actinophylla", "شيفليرا 🌿", 35, 50, 18, 30),
("Dracaena marginata", "دراسينا مارجيناتا 🌿", 30, 40, 18, 30),
("Dracaena fragrans", "دراسينا عطرية 🌿", 35, 35, 18, 30),
("Dracaena reflexa", "دراسينا ريفليكسا 🌿", 35, 40, 18, 30),
("Chamaedorea elegans", "نخلة الصالون 🌴", 45, 35, 18, 28),
("Areca catechu", "نخلة الأريكا 🌴", 45, 50, 18, 30),
("Howea forsteriana", "نخلة كنتيا 🌴", 40, 40, 18, 28),
("Dypsis lutescens", "نخلة الأريكا 🌴", 45, 50, 18, 30),

("Phoenix roebelenii", "نخلة روبليني 🌴", 35, 55, 18, 32),
("Cocos nucifera", "نخيل جوز الهند 🌴", 45, 70, 22, 32),
("Strelitzia reginae", "عصفور الجنة 🌿", 40, 65, 18, 32),
("Musa", "الموز 🍌", 60, 65, 20, 32),
("Caladium bicolor", "كالاتديوم 🌿", 60, 35, 18, 30),
("Dieffenbachia amoena", "ديفنباخيا 🌿", 45, 35, 18, 30),
("Spathiphyllum", "زنبق السلام 🌸", 45, 30, 18, 30),
("Aglaonema", "أجلونيما 🌿", 45, 30, 18, 30),
("Ficus", "فيكس 🌳", 40, 50, 18, 30),
("Begonia", "بيغونيا 🌸", 45, 40, 18, 28)

]


# ==========================================
# تحويل القائمة إلى قاعدة بيانات
# ==========================================

plant_data = {}

for scientific, arabic_name, soil, light, min_temp, max_temp in plants:

    plant_data[scientific] = {
        "name": arabic_name,
        "soil": soil,
        "light": light,
        "min_temp": min_temp,
        "max_temp": max_temp
    }


# ==========================================
# الكاميرا
# ==========================================

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

            # تحميل النموذج
            model = load_model()

            # تجهيز الصورة
            transform = transforms.Compose([

                transforms.Resize(256),

                transforms.CenterCrop(224),

                transforms.ToTensor(),

                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])

            input_tensor = transform(
                image
            ).unsqueeze(0)

            # تشغيل النموذج
            with torch.no_grad():

                logits = model(input_tensor)

                probs = torch.softmax(
                    logits,
                    dim=1
                )[0]

                top5 = probs.topk(5)

            # أسماء الأنواع
            labels = load_labels()

            # النتائج
            results = []

            for score, index in zip(
                top5.values,
                top5.indices
            ):

                results.append({
                    "label": labels[index.item()],
                    "score": score.item()
                })

            best = results[0]

            label = best["label"]

            confidence = best["score"] * 100

            # ==================================
            # مطابقة الاسم العلمي
            # ==================================

            matched_key = None

            label_lower = label.lower()

            for scientific_name in plant_data:

                if scientific_name.lower() in label_lower:

                    matched_key = scientific_name

                    break

            # ==================================
            # عرض التعرف
            # ==================================

            if matched_key is not None:

                matched = plant_data[matched_key]

                st.success(
                    f"🌿 تعرفت على النبتة: **{matched['name']}**"
                )

                st.metric(
                    "🎯 نسبة الثقة",
                    f"{confidence:.1f}%"
                )

            else:

                matched = None

                st.warning(
                    f"🌱 النموذج يتوقع: **{label}**"
                )

                st.info(
                    "تعرف الذكاء الاصطناعي على النبات، "
                    "لكن بيانات العناية بهذا النوع غير مضافة للمشروع حاليًا."
                )

            # ==================================
            # الاحتمالات
            # ==================================

            st.markdown("### 🔍 احتمالات التعرف")

            for result in results:

                st.write(
                    f"🌿 {result['label']} — "
                    f"{result['score'] * 100:.1f}%"
                )

            # ==================================
            # تحليل الصحة
            # ==================================

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

                    # التربة
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

                    # الإضاءة
                    if light < matched["light"]:

                        problems.append(
                            "☀️ الإضاءة منخفضة."
                        )

                        recommendations.append(
                            "ضعي النبتة في مكان بإضاءة مناسبة وغير مباشرة."
                        )

                    # الحرارة
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

                    # النتيجة
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

                            st.write(
                                "• " + recommendation
                            )

                    # ==================================
                    # الملخص
                    # ==================================

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

                    st.markdown(
                        "### 📋 ملخص التحليل"
                    )

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


# ==========================================
# عن المشروع
# ==========================================

st.divider()

st.markdown("## ℹ️ عن المشروع")

st.write("""
🌱 PlantCare AI

نظام ذكي للتعرف على النباتات من الصور ومساعد المستخدم
على معرفة احتياجات النبتة من الماء والإضاءة ودرجة الحرارة.

📷 تصوير النبتة
🤖 التعرف عليها بالذكاء الاصطناعي
💧 تحليل رطوبة التربة
☀️ تحليل الإضاءة
🌡️ تحليل درجة الحرارة
🌱 تقديم توصيات للعناية
""")

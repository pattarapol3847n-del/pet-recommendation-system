import streamlit as st
from neo4j import GraphDatabase
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pet Recommendation System",
    page_icon="🐾",
    layout="wide"
)


# =========================================================
# CUSTOM STYLE
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #f3fbf4 0%,
            #ffffff 50%,
            #eef8f0 100%
        );
    }

    section[data-testid="stSidebar"] {
        background-color: #e8f5e9;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #236b3b;
        margin-bottom: 5px;
    }

    .main-subtitle {
        text-align: center;
        font-size: 18px;
        color: #5f6f63;
        margin-bottom: 30px;
    }

    .welcome-box {
        background: rgba(255, 255, 255, 0.92);
        border-radius: 18px;
        padding: 25px;
        border: 1px solid #d9eadc;
        box-shadow: 0 5px 18px rgba(40, 80, 50, 0.08);
        margin-bottom: 25px;
    }

    .pet-title {
        color: #236b3b;
        font-size: 25px;
        font-weight: 700;
        margin-top: 10px;
    }

    .pet-section {
        color: #36764a;
        font-weight: 700;
        font-size: 16px;
        margin-top: 10px;
        margin-bottom: 3px;
    }

    .pet-text {
        color: #4e5d52;
        font-size: 15px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# IMAGE FOLDER
# =========================================================

IMAGE_DIR = Path(__file__).parent / "images"


def get_pet_image(pet_name):

    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    for extension in extensions:

        image_path = IMAGE_DIR / (
            pet_name.lower() + extension
        )

        if image_path.exists():
            return image_path

    return None


# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("🐾 Pet Recommendation")

st.sidebar.markdown(
    "เลือกเมนูที่ต้องการ"
)

page = st.sidebar.radio(
    "Menu",
    [
        "🏠 Home",
        "🐾 Pet Guide"
    ]
)


# =========================================================
# NEO4J CONNECTION
# =========================================================

@st.cache_resource
def get_driver():

    driver = GraphDatabase.driver(
        st.secrets["NEO4J_URI"],
        auth=(
            st.secrets["NEO4J_USERNAME"],
            st.secrets["NEO4J_PASSWORD"]
        )
    )

    driver.verify_connectivity()

    return driver


# =========================================================
# HOME PAGE
# =========================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">🐾 Pet Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'ค้นหาสัตว์เลี้ยงที่เหมาะสมกับไลฟ์สไตล์ของคุณ'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="welcome-box">

        <h3>🐾 ค้นหาสัตว์เลี้ยงที่เหมาะกับคุณ</h3>

        <p>
        ตอบคำถามเกี่ยวกับพื้นที่อยู่อาศัย งบประมาณ
        และเวลาที่สามารถใช้ในการดูแลสัตว์เลี้ยง
        ระบบจะนำข้อมูลไปวิเคราะห์และแนะนำสัตว์เลี้ยง
        ที่มีความเหมาะสมกับความต้องการของคุณ
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📋 ข้อมูลของคุณ")

    user_space = st.selectbox(
        "🏠 คุณอาศัยอยู่ในพื้นที่แบบใด?",
        [
            "House",
            "Condo",
            "Farm",
            "Outdoor Space"
        ]
    )

    user_budget = st.selectbox(
        "💰 งบประมาณในการเลี้ยงสัตว์",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    user_time = st.selectbox(
        "⏰ เวลาที่สามารถใช้ดูแลสัตว์เลี้ยง",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    if st.button(
        "🐾 ค้นหาสัตว์เลี้ยงที่เหมาะกับฉัน",
        use_container_width=True
    ):

        try:

            driver = get_driver()

            result = driver.execute_query(
                """
                MATCH (p:Pet)

                OPTIONAL MATCH
                    (p)-[:SUITABLE_FOR]->(space:LivingSpace)

                OPTIONAL MATCH
                    (p)-[:COST_LEVEL]->(budget:Budget)

                OPTIONAL MATCH
                    (p)-[:NEEDS_TIME]->(time:TimeAvailable)

                WITH
                    p,
                    collect(DISTINCT space.name) AS spaces,
                    collect(DISTINCT budget.name)[0] AS budget,
                    collect(DISTINCT time.name)[0] AS time

                WITH
                    p,
                    spaces,
                    budget,
                    time,

                    CASE
                        WHEN $space IN spaces THEN 1
                        ELSE 0
                    END +

                    CASE
                        WHEN budget = $budget THEN 1
                        ELSE 0
                    END +

                    CASE
                        WHEN time = $time THEN 1
                        ELSE 0
                    END AS score

                RETURN
                    p.name AS Pet,
                    p.description AS Description,
                    score AS Score,
                    spaces AS SuitableSpace,
                    budget AS Budget,
                    time AS TimeAvailable

                ORDER BY Score DESC, Pet
                """,

                space=user_space,
                budget=user_budget,
                time=user_time
            )

            st.markdown("---")

            st.subheader(
                "🐾 ผลการแนะนำสัตว์เลี้ยง"
            )

            for record in result.records:

                st.markdown("---")

                st.subheader(
                    f"🐾 {record['Pet']} — "
                    f"{record['Score']}/3"
                )

                st.write(
                    record["Description"]
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.info(
                        "🏠 พื้นที่ที่เหมาะสม\n\n"
                        + ", ".join(
                            record["SuitableSpace"]
                        )
                    )

                with col2:

                    st.info(
                        f"💰 ระดับงบประมาณ\n\n"
                        f"{record['Budget']}"
                    )

                with col3:

                    st.info(
                        f"⏰ ระดับเวลาในการดูแล\n\n"
                        f"{record['TimeAvailable']}"
                    )

        except Exception as e:

            st.error(
                "ไม่สามารถเชื่อมต่อกับ Neo4j ได้"
            )

            st.write(str(e))


# =========================================================
# PET GUIDE PAGE
# =========================================================

elif page == "🐾 Pet Guide":

    st.markdown(
        '<div class="main-title">🐾 คู่มือแนะนำสัตว์เลี้ยง</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'ทำความรู้จักกับสัตว์เลี้ยงแต่ละประเภท '
        'ก่อนตัดสินใจเลือกสัตว์ที่เหมาะกับคุณ'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # PET DATA
    # =====================================================

    pets = [

        {
            "name": "Dog",
            "title": "สุนัข",
            "personality": "เป็นมิตร เข้าสังคม และชอบทำกิจกรรม",
            "description": "สุนัขเป็นสัตว์เลี้ยงที่เป็นมิตรและชอบอยู่ร่วมกับผู้คน เหมาะสำหรับผู้ที่มีเวลาในการดูแลและพาออกกำลังกาย",
            "care": "ต้องการอาหาร น้ำสะอาด การออกกำลังกาย การดูแลสุขภาพ และการเอาใจใส่อย่างสม่ำเสมอ"
        },

        {
            "name": "Cat",
            "title": "แมว",
            "personality": "รักอิสระ ปรับตัวได้ดี และค่อนข้างสงบ",
            "description": "แมวเป็นสัตว์เลี้ยงที่รักอิสระและสามารถปรับตัวให้เข้ากับสภาพแวดล้อมภายในบ้านได้ดี",
            "care": "ต้องการอาหาร น้ำสะอาด กระบะทราย พื้นที่สำหรับพักผ่อน และการดูแลสุขภาพอย่างสม่ำเสมอ"
        },

        {
            "name": "Bird",
            "title": "นก",
            "personality": "ชอบเข้าสังคม กระตือรือร้น และร่าเริง",
            "description": "นกเป็นสัตว์เลี้ยงขนาดเล็กที่มีความกระตือรือร้น และสามารถสร้างความเพลิดเพลินให้กับผู้เลี้ยงได้",
            "care": "ต้องการกรงที่เหมาะสม อาหาร น้ำสะอาด และการดูแลความสะอาดของกรงอย่างสม่ำเสมอ"
        },

        {
            "name": "Rabbit",
            "title": "กระต่าย",
            "personality": "อ่อนโยน สงบ และไม่ก้าวร้าว",
            "description": "กระต่ายเป็นสัตว์เลี้ยงขนาดเล็กที่มีนิสัยอ่อนโยน และค่อนข้างเงียบ เหมาะสำหรับผู้ที่ชอบสัตว์เลี้ยงที่สงบ",
            "care": "ต้องการพื้นที่อยู่อาศัยที่สะอาด อาหารที่เหมาะสม น้ำสะอาด และการดูแลสุขภาพอย่างสม่ำเสมอ"
        },

        {
            "name": "Fish",
            "title": "ปลา",
            "personality": "สงบ เงียบ และดูแลง่าย",
            "description": "ปลาเป็นสัตว์เลี้ยงที่เงียบและเหมาะสำหรับผู้ที่ต้องการสัตว์เลี้ยงที่ใช้พื้นที่ไม่มาก",
            "care": "ต้องการตู้ปลาที่เหมาะสม น้ำสะอาด อาหารที่เหมาะสม และการดูแลคุณภาพน้ำเป็นประจำ"
        },

        {
            "name": "Hamster",
            "title": "แฮมสเตอร์",
            "personality": "ตัวเล็ก กระตือรือร้น และชอบสำรวจ",
            "description": "แฮมสเตอร์เป็นสัตว์เลี้ยงขนาดเล็กที่สามารถเลี้ยงในพื้นที่จำกัด และมีพฤติกรรมที่น่าสนใจให้สังเกต",
            "care": "ต้องการกรงที่สะอาด อาหาร น้ำสะอาด และอุปกรณ์สำหรับออกกำลังกายที่เหมาะสม"
        },

        {
            "name": "Duck",
            "title": "เป็ด",
            "personality": "ชอบเข้าสังคม กระตือรือร้น และชอบอยู่รวมกัน",
            "description": "เป็ดเป็นสัตว์ที่ชอบอยู่รวมกันและต้องการพื้นที่สำหรับเดินเล่นและทำกิจกรรมกลางแจ้ง",
            "care": "ต้องการพื้นที่กลางแจ้ง น้ำสะอาด อาหารที่เหมาะสม ที่พักอาศัย และการดูแลอย่างสม่ำเสมอ"
        },

        {
            "name": "Sheep",
            "title": "แกะ",
            "personality": "รักสงบ ชอบอยู่รวมกัน และเข้าสังคมได้ดี",
            "description": "แกะเป็นสัตว์เลี้ยงในพื้นที่เกษตรที่มักอยู่รวมกันเป็นฝูง และต้องการพื้นที่สำหรับใช้ชีวิตอย่างเหมาะสม",
            "care": "ต้องการพื้นที่สำหรับเลี้ยง อาหาร น้ำสะอาด ที่พัก และการดูแลสุขภาพอย่างเหมาะสม"
        },

        {
            "name": "Turtle",
            "title": "เต่า",
            "personality": "สงบ เงียบ และเคลื่อนไหวช้า",
            "description": "เต่าเป็นสัตว์ที่ค่อนข้างสงบและเงียบ เหมาะสำหรับผู้ที่ชอบสังเกตพฤติกรรมของสัตว์",
            "care": "ต้องการพื้นที่อยู่อาศัยที่เหมาะสม อาหารที่เหมาะกับชนิดของเต่า น้ำสะอาด และการดูแลสภาพแวดล้อมอย่างสม่ำเสมอ"
        },

        {
            "name": "Horse",
            "title": "ม้า",
            "personality": "กระตือรือร้น แข็งแรง และต้องการการเคลื่อนไหว",
            "description": "ม้าเป็นสัตว์ขนาดใหญ่ที่มีความกระตือรือร้น และต้องการพื้นที่กว้างสำหรับการเคลื่อนไหวและออกกำลังกาย",
            "care": "ต้องการพื้นที่กลางแจ้งขนาดใหญ่ อาหาร น้ำสะอาด การออกกำลังกาย และการดูแลสุขภาพอย่างสม่ำเสมอ"
        }

    ]


    # =====================================================
    # DISPLAY PET CARDS
    # =====================================================

    for i in range(0, len(pets), 3):

        columns = st.columns(3)

        for j, col in enumerate(columns):

            if i + j >= len(pets):
                continue

            pet = pets[i + j]

            with col:

                # ใช้ container ของ Streamlit แทน HTML div
                with st.container(border=True):

                    image_path = get_pet_image(
                        pet["name"]
                    )

                    if image_path:

                        st.image(
                            str(image_path),
                            use_container_width=True
                        )

                    else:

                        st.warning(
                            f"ไม่พบรูปของ {pet['title']}"
                        )

                    st.markdown(
                        f"""
                        <div class="pet-title">
                            🐾 {pet["title"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="pet-section">
                            💚 ลักษณะนิสัย
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="pet-text">
                            {pet["personality"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="pet-section">
                            📖 ลักษณะทั่วไป
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="pet-text">
                            {pet["description"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="pet-section">
                            🧡 การดูแลเบื้องต้น
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="pet-text">
                            {pet["care"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("---")

    st.info(
        "💡 ข้อมูลในหน้านี้ใช้สำหรับแนะนำลักษณะทั่วไปของสัตว์ "
        "ส่วนการเลือกสัตว์ที่เหมาะสมกับผู้ใช้งาน "
        "สามารถใช้ระบบแนะนำจากหน้า Home ได้"
    )
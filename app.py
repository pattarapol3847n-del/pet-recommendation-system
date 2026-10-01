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
# IMAGE FOLDER
# =========================================================

IMAGE_DIR = Path(__file__).parent / "images"


def get_pet_image(pet_name):
    """
    Find the image file for each pet.
    Supports jpg, jpeg, png and webp.
    """

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

    st.title("🐾 Pet Recommendation System")

    st.write(
        "Find a pet that matches your lifestyle."
    )

    st.subheader("Tell us about your lifestyle")

    user_space = st.selectbox(
        "Where do you live?",
        [
            "House",
            "Condo",
            "Farm",
            "Outdoor Space"
        ]
    )

    user_budget = st.selectbox(
        "What is your pet budget?",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    user_time = st.selectbox(
        "How much time can you spend caring for a pet?",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    if st.button("🐾 Recommend Pets"):

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

            st.subheader("🐾 Recommended Pets")

            for record in result.records:

                st.markdown("---")

                st.subheader(
                    f"🐾 {record['Pet']} — {record['Score']}/3"
                )

                st.write(
                    record["Description"]
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        "🏠 Suitable Space: "
                        + ", ".join(
                            record["SuitableSpace"]
                        )
                    )

                with col2:

                    st.write(
                        f"💰 Budget: {record['Budget']}"
                    )

                with col3:

                    st.write(
                        f"⏰ Time: {record['TimeAvailable']}"
                    )

        except Exception as e:

            st.error(
                "Unable to connect to Neo4j."
            )

            st.write(str(e))


# =========================================================
# PET GUIDE PAGE
# =========================================================

elif page == "🐾 Pet Guide":

    st.title("🐾 คู่มือแนะนำสัตว์เลี้ยง")

    st.write(
        "ทำความรู้จักกับสัตว์เลี้ยงแต่ละประเภท "
        "ลักษณะนิสัย ลักษณะทั่วไป และการดูแลเบื้องต้น"
    )

    st.markdown("---")


    # =====================================================
    # PET INFORMATION
    # =====================================================

    pets = [

        {
            "name": "Dog",
            "title": "สุนัข",

            "personality":
                "เป็นมิตร เข้าสังคม และชอบทำกิจกรรม",

            "description":
                "สุนัขเป็นสัตว์เลี้ยงที่เป็นมิตรและชอบอยู่ร่วมกับผู้คน "
                "เหมาะสำหรับผู้ที่มีเวลาในการดูแลและพาออกกำลังกาย",

            "care":
                "ต้องการอาหาร น้ำสะอาด การออกกำลังกาย "
                "การดูแลสุขภาพ และการเอาใจใส่อย่างสม่ำเสมอ"
        },


        {
            "name": "Cat",
            "title": "แมว",

            "personality":
                "รักอิสระ ปรับตัวได้ดี และค่อนข้างสงบ",

            "description":
                "แมวเป็นสัตว์เลี้ยงที่รักอิสระและสามารถปรับตัว "
                "ให้เข้ากับสภาพแวดล้อมภายในบ้านได้ดี",

            "care":
                "ต้องการอาหาร น้ำสะอาด กระบะทราย "
                "พื้นที่สำหรับพักผ่อน และการดูแลสุขภาพอย่างสม่ำเสมอ"
        },


        {
            "name": "Bird",
            "title": "นก",

            "personality":
                "ชอบเข้าสังคม กระตือรือร้น และร่าเริง",

            "description":
                "นกเป็นสัตว์เลี้ยงขนาดเล็กที่มีความกระตือรือร้น "
                "และสามารถสร้างความเพลิดเพลินให้กับผู้เลี้ยงได้",

            "care":
                "ต้องการกรงที่เหมาะสม อาหาร น้ำสะอาด "
                "และการดูแลความสะอาดของกรงอย่างสม่ำเสมอ"
        },


        {
            "name": "Rabbit",
            "title": "กระต่าย",

            "personality":
                "อ่อนโยน สงบ และไม่ก้าวร้าว",

            "description":
                "กระต่ายเป็นสัตว์เลี้ยงขนาดเล็กที่มีนิสัยอ่อนโยน "
                "และค่อนข้างเงียบ เหมาะสำหรับผู้ที่ชอบสัตว์เลี้ยงที่สงบ",

            "care":
                "ต้องการพื้นที่อยู่อาศัยที่สะอาด อาหารที่เหมาะสม "
                "น้ำสะอาด และการดูแลสุขภาพอย่างสม่ำเสมอ"
        },


        {
            "name": "Fish",
            "title": "ปลา",

            "personality":
                "สงบ เงียบ และดูแลง่าย",

            "description":
                "ปลาเป็นสัตว์เลี้ยงที่เงียบและเหมาะสำหรับผู้ที่ต้องการ "
                "สัตว์เลี้ยงที่ใช้พื้นที่ไม่มาก",

            "care":
                "ต้องการตู้ปลาที่เหมาะสม น้ำสะอาด "
                "อาหารที่เหมาะสม และการดูแลคุณภาพน้ำเป็นประจำ"
        },


        {
            "name": "Hamster",
            "title": "แฮมสเตอร์",

            "personality":
                "ตัวเล็ก กระตือรือร้น และชอบสำรวจ",

            "description":
                "แฮมสเตอร์เป็นสัตว์เลี้ยงขนาดเล็กที่สามารถเลี้ยง "
                "ในพื้นที่จำกัด และมีพฤติกรรมที่น่าสนใจให้สังเกต",

            "care":
                "ต้องการกรงที่สะอาด อาหาร น้ำสะอาด "
                "และอุปกรณ์สำหรับออกกำลังกายที่เหมาะสม"
        },


        {
            "name": "Duck",
            "title": "เป็ด",

            "personality":
                "ชอบเข้าสังคม กระตือรือร้น และชอบอยู่รวมกัน",

            "description":
                "เป็ดเป็นสัตว์ที่ชอบอยู่รวมกันและต้องการพื้นที่ "
                "สำหรับเดินเล่นและทำกิจกรรมกลางแจ้ง",

            "care":
                "ต้องการพื้นที่กลางแจ้ง น้ำสะอาด อาหารที่เหมาะสม "
                "ที่พักอาศัย และการดูแลอย่างสม่ำเสมอ"
        },


        {
            "name": "Sheep",
            "title": "แกะ",

            "personality":
                "รักสงบ ชอบอยู่รวมกัน และเข้าสังคมได้ดี",

            "description":
                "แกะเป็นสัตว์เลี้ยงในพื้นที่เกษตรที่มักอยู่รวมกันเป็นฝูง "
                "และต้องการพื้นที่สำหรับใช้ชีวิตอย่างเหมาะสม",

            "care":
                "ต้องการพื้นที่สำหรับเลี้ยง อาหาร น้ำสะอาด "
                "ที่พัก และการดูแลสุขภาพอย่างเหมาะสม"
        },


        {
            "name": "Turtle",
            "title": "เต่า",

            "personality":
                "สงบ เงียบ และเคลื่อนไหวช้า",

            "description":
                "เต่าเป็นสัตว์ที่ค่อนข้างสงบและเงียบ "
                "เหมาะสำหรับผู้ที่ชอบสังเกตพฤติกรรมของสัตว์",

            "care":
                "ต้องการพื้นที่อยู่อาศัยที่เหมาะสม "
                "อาหารที่เหมาะกับชนิดของเต่า น้ำสะอาด "
                "และการดูแลสภาพแวดล้อมอย่างสม่ำเสมอ"
        },


        {
            "name": "Horse",
            "title": "ม้า",

            "personality":
                "กระตือรือร้น แข็งแรง และต้องการการเคลื่อนไหว",

            "description":
                "ม้าเป็นสัตว์ขนาดใหญ่ที่มีความกระตือรือร้น "
                "และต้องการพื้นที่กว้างสำหรับการเคลื่อนไหวและออกกำลังกาย",

            "care":
                "ต้องการพื้นที่กลางแจ้งขนาดใหญ่ อาหาร น้ำสะอาด "
                "การออกกำลังกาย และการดูแลสุขภาพอย่างสม่ำเสมอ"
        }

    ]


    # =====================================================
    # PET CARDS
    # =====================================================

    for i in range(0, len(pets), 3):

        columns = st.columns(3)

        for j, col in enumerate(columns):

            if i + j >= len(pets):
                continue

            pet = pets[i + j]

            with col:

                # -----------------------------------------
                # PET IMAGE
                # -----------------------------------------

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


                # -----------------------------------------
                # PET NAME
                # -----------------------------------------

                st.subheader(
                    f"🐾 {pet['title']}"
                )


                # -----------------------------------------
                # PERSONALITY
                # -----------------------------------------

                st.markdown(
                    "**ลักษณะนิสัย**"
                )

                st.write(
                    pet["personality"]
                )


                # -----------------------------------------
                # DESCRIPTION
                # -----------------------------------------

                st.markdown(
                    "**ลักษณะทั่วไป**"
                )

                st.write(
                    pet["description"]
                )


                # -----------------------------------------
                # CARE
                # -----------------------------------------

                st.markdown(
                    "**การดูแลเบื้องต้น**"
                )

                st.write(
                    pet["care"]
                )


                st.markdown("---")


    # =====================================================
    # INFORMATION
    # =====================================================

    st.info(
        "💡 ข้อมูลในหน้านี้ใช้สำหรับแนะนำลักษณะทั่วไปของสัตว์ "
        "ส่วนการเลือกสัตว์ที่เหมาะสมกับผู้ใช้งาน "
        "สามารถใช้ระบบแนะนำจากหน้า Home ได้"
    )
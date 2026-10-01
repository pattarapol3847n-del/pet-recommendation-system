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

st.markdown("""
<style>
.pet-section-title {
    color: #D4A017;
    font-weight: bold;
    font-size: 18px;
    margin-top: 10px;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# IMAGE FOLDER
# =========================================================

IMAGE_DIR = Path(__file__).parent / "images"


def get_pet_image(pet_name):
    extensions = [".jpg", ".jpeg", ".png", ".webp"]

    for extension in extensions:
        image_path = IMAGE_DIR / (pet_name.lower() + extension)

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
        "🐾 Pet Guide",
        "🔐 Admin"
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
                        + ", ".join(record["SuitableSpace"])
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

    pets = [

        {
            "name": "Dog",
            "title": "สุนัข",
            "personality": "เป็นมิตร เข้าสังคม และชอบทำกิจกรรม",
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
            "personality": "รักอิสระ ปรับตัวได้ดี และค่อนข้างสงบ",
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
            "personality": "ชอบเข้าสังคม กระตือรือร้น และร่าเริง",
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
            "personality": "อ่อนโยน สงบ และไม่ก้าวร้าว",
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
            "personality": "สงบ เงียบ และดูแลง่าย",
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
            "personality": "ตัวเล็ก กระตือรือร้น และชอบสำรวจ",
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
            "personality": "ชอบเข้าสังคม กระตือรือร้น และชอบอยู่รวมกัน",
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
            "personality": "รักสงบ ชอบอยู่รวมกัน และเข้าสังคมได้ดี",
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
            "personality": "สงบ เงียบ และเคลื่อนไหวช้า",
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
            "personality": "กระตือรือร้น แข็งแรง และต้องการการเคลื่อนไหว",
            "description":
                "ม้าเป็นสัตว์ขนาดใหญ่ที่มีความกระตือรือร้น "
                "และต้องการพื้นที่กว้างสำหรับการเคลื่อนไหวและออกกำลังกาย",
            "care":
                "ต้องการพื้นที่กลางแจ้งขนาดใหญ่ อาหาร น้ำสะอาด "
                "การออกกำลังกาย และการดูแลสุขภาพอย่างสม่ำเสมอ"
        }

    ]

    for i in range(0, len(pets), 3):

        columns = st.columns(3)

        for j, col in enumerate(columns):

            if i + j >= len(pets):
                continue

            pet = pets[i + j]

            with col:

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

                st.subheader(
                    f"🐾 {pet['title']}"
                )

                st.markdown(
                    '<div class="pet-section-title">ลักษณะนิสัย</div>',
                    unsafe_allow_html=True
                )
                st.write(pet["personality"])

                st.markdown(
                    '<div class="pet-section-title">ลักษณะทั่วไป</div>',
                    unsafe_allow_html=True
                )
                st.write(pet["description"])

                st.markdown(
                    '<div class="pet-section-title">การดูแลเบื้องต้น</div>',
                    unsafe_allow_html=True
                )
                st.write(pet["care"])

                st.markdown("---")

    st.info(
        "💡 ข้อมูลในหน้านี้ใช้สำหรับแนะนำลักษณะทั่วไปของสัตว์ "
        "ส่วนการเลือกสัตว์ที่เหมาะสมกับผู้ใช้งาน "
        "สามารถใช้ระบบแนะนำจากหน้า Home ได้"
    )


# =========================================================
# ADMIN PAGE
# =========================================================

elif page == "🔐 Admin":

    st.title("🔐 Admin")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    # =====================================================
    # LOGIN
    # =====================================================

    if not st.session_state.admin_logged_in:

        st.subheader("🔑 Admin Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("🔐 Login"):

            # สำหรับงานส่ง/เดโม
            # Username: admin
            # Password: admin123

            if (
                username == "admin"
                and password == "admin123"
            ):

                st.session_state.admin_logged_in = True

                st.success(
                    "เข้าสู่ระบบ Admin สำเร็จ"
                )

                st.rerun()

            else:

                st.error(
                    "Username หรือ Password ไม่ถูกต้อง"
                )

    # =====================================================
    # DASHBOARD
    # =====================================================

    else:

        st.title("🔧 Admin Dashboard")

        st.success(
            "เข้าสู่ระบบ Admin แล้ว"
        )

        if st.button("🚪 Logout"):

            st.session_state.admin_logged_in = False

            st.rerun()

        st.markdown("---")

        # =================================================
        # ADD PET
        # =================================================

        st.subheader("➕ เพิ่มสัตว์เลี้ยง")

        add_col1, add_col2 = st.columns(2)

        with add_col1:

            new_pet_name = st.text_input(
                "ชื่อสัตว์เลี้ยง",
                key="new_pet_name"
            )

        with add_col2:

            new_pet_description = st.text_area(
                "รายละเอียด",
                key="new_pet_description"
            )

        add_col3, add_col4, add_col5 = st.columns(3)

        with add_col3:

            new_pet_space = st.selectbox(
                "พื้นที่ที่เหมาะสม",
                [
                    "House",
                    "Condo",
                    "Farm",
                    "Outdoor Space"
                ],
                key="new_pet_space"
            )

        with add_col4:

            new_pet_budget = st.selectbox(
                "งบประมาณ",
                [
                    "Low",
                    "Medium",
                    "High"
                ],
                key="new_pet_budget"
            )

        with add_col5:

            new_pet_time = st.selectbox(
                "เวลาที่ใช้ดูแล",
                [
                    "Low",
                    "Medium",
                    "High"
                ],
                key="new_pet_time"
            )

        if st.button(
            "➕ Add Pet",
            key="add_pet_button"
        ):

            if (
                new_pet_name.strip() == ""
                or new_pet_description.strip() == ""
            ):

                st.warning(
                    "กรุณากรอกชื่อและรายละเอียดสัตว์เลี้ยง"
                )

            else:

                try:

                    driver = get_driver()

                    driver.execute_query(
                        """
                        MERGE (p:Pet {name: $name})

                        SET p.description = $description

                        WITH p

                        MERGE (space:LivingSpace {
                            name: $space
                        })

                        MERGE (budget:Budget {
                            name: $budget
                        })

                        MERGE (time:TimeAvailable {
                            name: $time
                        })

                        MERGE (p)-[:SUITABLE_FOR]->(space)

                        MERGE (p)-[:COST_LEVEL]->(budget)

                        MERGE (p)-[:NEEDS_TIME]->(time)
                        """,
                        name=new_pet_name.strip(),
                        description=new_pet_description.strip(),
                        space=new_pet_space,
                        budget=new_pet_budget,
                        time=new_pet_time
                    )

                    st.success(
                        f"เพิ่ม {new_pet_name} สำเร็จ"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "ไม่สามารถเพิ่มข้อมูลได้"
                    )

                    st.write(str(e))

        st.markdown("---")

        # =================================================
        # MANAGE PETS
        # =================================================

        st.subheader("🐾 จัดการข้อมูลสัตว์เลี้ยง")

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

                RETURN
                    p.name AS name,
                    p.description AS description,
                    collect(DISTINCT space.name)[0] AS space,
                    collect(DISTINCT budget.name)[0] AS budget,
                    collect(DISTINCT time.name)[0] AS time

                ORDER BY name
                """
            )

            if len(result.records) == 0:

                st.info(
                    "ยังไม่มีข้อมูลสัตว์เลี้ยงใน Neo4j"
                )

            for record in result.records:

                pet_name = record["name"]

                with st.expander(
                    f"🐾 {pet_name}"
                ):

                    st.markdown("### ✏️ แก้ไขข้อมูล")

                    edit_name = st.text_input(
                        "ชื่อสัตว์เลี้ยง",
                        value=record["name"],
                        key=f"edit_name_{pet_name}"
                    )

                    edit_description = st.text_area(
                        "รายละเอียด",
                        value=record["description"] or "",
                        key=f"edit_description_{pet_name}"
                    )

                    spaces = [
                        "House",
                        "Condo",
                        "Farm",
                        "Outdoor Space"
                    ]

                    budgets = [
                        "Low",
                        "Medium",
                        "High"
                    ]

                    times = [
                        "Low",
                        "Medium",
                        "High"
                    ]

                    current_space = (
                        record["space"]
                        if record["space"] in spaces
                        else spaces[0]
                    )

                    current_budget = (
                        record["budget"]
                        if record["budget"] in budgets
                        else budgets[0]
                    )

                    current_time = (
                        record["time"]
                        if record["time"] in times
                        else times[0]
                    )

                    edit_col1, edit_col2, edit_col3 = st.columns(3)

                    with edit_col1:

                        edit_space = st.selectbox(
                            "พื้นที่",
                            spaces,
                            index=spaces.index(current_space),
                            key=f"edit_space_{pet_name}"
                        )

                    with edit_col2:

                        edit_budget = st.selectbox(
                            "งบประมาณ",
                            budgets,
                            index=budgets.index(current_budget),
                            key=f"edit_budget_{pet_name}"
                        )

                    with edit_col3:

                        edit_time = st.selectbox(
                            "เวลาที่ดูแล",
                            times,
                            index=times.index(current_time)
                            ,
                            key=f"edit_time_{pet_name}"
                        )

                    save_col, delete_col = st.columns(2)

                    with save_col:

                        if st.button(
                            "💾 Save Changes",
                            key=f"save_{pet_name}"
                        ):

                            if edit_name.strip() == "":

                                st.warning(
                                    "กรุณากรอกชื่อสัตว์เลี้ยง"
                                )

                            else:

                                try:

                                    driver.execute_query(
                                        """
                                        MATCH (p:Pet {
                                            name: $old_name
                                        })

                                        SET
                                            p.name = $name,
                                            p.description = $description

                                        WITH p

                                        OPTIONAL MATCH
                                            (p)-[r:SUITABLE_FOR|COST_LEVEL|NEEDS_TIME]->()

                                        DELETE r

                                        WITH p

                                        MERGE (space:LivingSpace {
                                            name: $space
                                        })

                                        MERGE (budget:Budget {
                                            name: $budget
                                        })

                                        MERGE (time:TimeAvailable {
                                            name: $time
                                        })

                                        MERGE
                                            (p)-[:SUITABLE_FOR]->(space)

                                        MERGE
                                            (p)-[:COST_LEVEL]->(budget)

                                        MERGE
                                            (p)-[:NEEDS_TIME]->(time)
                                        """,
                                        old_name=record["name"],
                                        name=edit_name.strip(),
                                        description=edit_description.strip(),
                                        space=edit_space,
                                        budget=edit_budget,
                                        time=edit_time
                                    )

                                    st.success(
                                        f"แก้ไข {edit_name} สำเร็จ"
                                    )

                                    st.rerun()

                                except Exception as e:

                                    st.error(
                                        "ไม่สามารถแก้ไขข้อมูลได้"
                                    )

                                    st.write(str(e))

                    with delete_col:

                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_{pet_name}"
                        ):

                            try:

                                driver.execute_query(
                                    """
                                    MATCH (p:Pet {
                                        name: $name
                                    })

                                    DETACH DELETE p
                                    """,
                                    name=record["name"]
                                )

                                st.success(
                                    f"ลบ {record['name']} สำเร็จ"
                                )

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    "ไม่สามารถลบข้อมูลได้"
                                )

                                st.write(str(e))

        except Exception as e:

            st.error(
                "Unable to connect to Neo4j."
            )

            st.write(str(e))

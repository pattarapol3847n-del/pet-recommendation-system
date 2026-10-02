import streamlit as st
from neo4j import GraphDatabase
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ระบบแนะนำสัตว์เลี้ยง",
    page_icon="🐾",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #6B4F3A;
        text-align: center;
        margin-bottom: 10px;
    }

    .sub-title {
        font-size: 20px;
        color: #777;
        text-align: center;
        margin-bottom: 30px;
    }

    .pet-card {
        background-color: #FFF8F0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #E8D8C8;
    }

    .pet-name {
        font-size: 25px;
        font-weight: bold;
        color: #6B4F3A;
    }

    .score {
        font-size: 18px;
        font-weight: bold;
        color: #D17A22;
    }

    .info-box {
        background-color: #F5F5F5;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# IMAGE DIRECTORY
# =========================================================

IMAGE_DIR = Path(__file__).parent / "images"


def get_pet_image(pet_name):
    """
    ค้นหารูปสัตว์เลี้ยงจากโฟลเดอร์ images
    """

    possible_names = {
        "Dog": ["dog.jpg", "dog.png", "สุนัข.jpg", "สุนัข.png"],
        "Cat": ["cat.jpg", "cat.png", "แมว.jpg", "แมว.png"],
        "Bird": ["bird.jpg", "bird.png", "นก.jpg", "นก.png"],
        "Rabbit": ["rabbit.jpg", "rabbit.png", "กระต่าย.jpg", "กระต่าย.png"],
        "Fish": ["fish.jpg", "fish.png", "ปลา.jpg", "ปลา.png"],
        "Hamster": ["hamster.jpg", "hamster.png", "แฮมสเตอร์.jpg", "แฮมสเตอร์.png"],
        "Duck": ["duck.jpg", "duck.png", "เป็ด.jpg", "เป็ด.png"],
        "Sheep": ["sheep.jpg", "sheep.png", "แกะ.jpg", "แกะ.png"],
        "Turtle": ["turtle.jpg", "turtle.png", "เต่า.jpg", "เต่า.png"],
        "Horse": ["horse.jpg", "horse.png", "ม้า.jpg", "ม้า.png"]
    }

    if pet_name not in possible_names:
        return None

    for filename in possible_names[pet_name]:
        path = IMAGE_DIR / filename

        if path.exists():
            return path

    return None


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
# TRANSLATION
# =========================================================

PET_TH = {
    "Dog": "สุนัข",
    "Cat": "แมว",
    "Bird": "นก",
    "Rabbit": "กระต่าย",
    "Fish": "ปลา",
    "Hamster": "แฮมสเตอร์",
    "Duck": "เป็ด",
    "Sheep": "แกะ",
    "Turtle": "เต่า",
    "Horse": "ม้า"
}

SPACE_TH = {
    "House": "บ้าน",
    "Condo": "คอนโด",
    "Farm": "ฟาร์ม",
    "Outdoor Space": "พื้นที่กลางแจ้ง"
}

BUDGET_TH = {
    "Low": "ต่ำ",
    "Medium": "ปานกลาง",
    "High": "สูง"
}

TIME_TH = {
    "Low": "น้อย",
    "Medium": "ปานกลาง",
    "High": "มาก"
}

DESCRIPTION_TH = {
    "Dog": "สุนัขเป็นสัตว์ที่ซื่อสัตย์และเข้ากับคนได้ดี เหมาะสำหรับผู้ที่มีเวลาในการดูแลและพาออกกำลังกาย",

    "Cat": "แมวเป็นสัตว์ที่ดูแลง่าย ใช้พื้นที่ไม่มาก และสามารถอยู่ในบ้านหรือคอนโดได้",

    "Bird": "นกเป็นสัตว์เลี้ยงที่ใช้พื้นที่ไม่มาก เหมาะสำหรับผู้ที่ชอบสัตว์ขนาดเล็ก",

    "Rabbit": "กระต่ายเป็นสัตว์ขนาดเล็ก น่ารัก และสามารถเลี้ยงในพื้นที่จำกัดได้",

    "Fish": "ปลาเป็นสัตว์เลี้ยงที่ไม่ต้องใช้พื้นที่มาก เหมาะสำหรับผู้ที่มีเวลาหรือพื้นที่จำกัด",

    "Hamster": "แฮมสเตอร์เป็นสัตว์ขนาดเล็ก ใช้พื้นที่ไม่มาก และเหมาะสำหรับผู้ที่ต้องการสัตว์เลี้ยงที่ดูแลง่าย",

    "Duck": "เป็ดเหมาะกับพื้นที่ที่กว้างและผู้ที่สามารถดูแลเรื่องพื้นที่และอาหารได้",

    "Sheep": "แกะเหมาะกับพื้นที่ขนาดใหญ่ เช่น ฟาร์ม และต้องการพื้นที่สำหรับเดินและกินอาหาร",

    "Turtle": "เต่าเป็นสัตว์ที่ค่อนข้างดูแลง่าย แต่ต้องจัดสภาพแวดล้อมและอาหารให้เหมาะสม",

    "Horse": "ม้าต้องการพื้นที่ขนาดใหญ่ งบประมาณและเวลาในการดูแลค่อนข้างมาก"
}


# =========================================================
# SIDEBAR
# =========================================================

page = st.sidebar.radio(
    "เมนู",
    [
        "🏠 หน้าหลัก",
        "🐾 คู่มือสัตว์เลี้ยง",
        "🔐 ผู้ดูแลระบบ"
    ]
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "🏠 หน้าหลัก":

    st.markdown(
        '<div class="main-title">🐾 ระบบแนะนำสัตว์เลี้ยง</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">เลือกข้อมูลของคุณเพื่อค้นหาสัตว์เลี้ยงที่เหมาะสม</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    st.subheader("👤 ข้อมูลผู้ใช้")

    user_names = [
        "มิน",
        "น้ำ",
        "สา",
        "กร",
        "กุล",
        "นน",
        "ปิ่น",
        "สุข",
        "ยิ้ม",
        "จ๋า"
    ]

    selected_user = st.selectbox(
        "ชื่อของคุณ",
        user_names
    )

    # -----------------------------------------------------
    # FRIENDS
    # -----------------------------------------------------

    st.subheader("👥 เพื่อน")

    friend_options = [
        name for name in user_names
        if name != selected_user
    ]

    selected_friends = st.multiselect(
        "คุณเป็นเพื่อนกับใคร?",
        friend_options,
        placeholder="เลือกเพื่อน"
    )

    # -----------------------------------------------------
    # LIFESTYLE
    # -----------------------------------------------------

    st.subheader("🏠 รูปแบบการใช้ชีวิต")

    col1, col2, col3 = st.columns(3)

    # -------------------------
    # SPACE
    # -------------------------

    with col1:

        space_th = st.selectbox(
            "ที่อยู่อาศัย",
            [
                "บ้าน",
                "คอนโด",
                "ฟาร์ม",
                "พื้นที่กลางแจ้ง"
            ]
        )

    user_space = {
        "บ้าน": "House",
        "คอนโด": "Condo",
        "ฟาร์ม": "Farm",
        "พื้นที่กลางแจ้ง": "Outdoor Space"
    }[space_th]

    # -------------------------
    # BUDGET
    # -------------------------

    with col2:

        budget_th = st.selectbox(
            "งบประมาณ",
            [
                "ต่ำ",
                "ปานกลาง",
                "สูง"
            ]
        )

    user_budget = {
        "ต่ำ": "Low",
        "ปานกลาง": "Medium",
        "สูง": "High"
    }[budget_th]

    # -------------------------
    # TIME
    # -------------------------

    with col3:

        time_th = st.selectbox(
            "เวลาที่มีในการดูแล",
            [
                "น้อย",
                "ปานกลาง",
                "มาก"
            ]
        )

    user_time = {
        "น้อย": "Low",
        "ปานกลาง": "Medium",
        "มาก": "High"
    }[time_th]

    st.divider()

    # =====================================================
    # RECOMMEND BUTTON
    # =====================================================

    if st.button(
        "🐾 บันทึกข้อมูลและแนะนำสัตว์เลี้ยง",
        use_container_width=True
    ):

        try:

            driver = get_driver()

            # =================================================
            # SAVE USER + FRIENDS + LIFESTYLE TO NEO4J
            # =================================================

            save_query = """

            // -----------------------------------------------
            // สร้าง User ถ้ายังไม่มี
            // -----------------------------------------------

            MERGE (u:User {name: $user})

            // -----------------------------------------------
            // ลบเพื่อนเดิมของ User คนนี้
            // -----------------------------------------------

            WITH u

            OPTIONAL MATCH
                (u)-[oldFriend:FRIEND_OF]-(:User)

            DELETE oldFriend

            // -----------------------------------------------
            // ลบข้อมูล Lifestyle เดิม
            // -----------------------------------------------

            WITH u

            OPTIONAL MATCH
                (u)-[oldSpace:LIVES_IN]->()

            DELETE oldSpace

            WITH u

            OPTIONAL MATCH
                (u)-[oldBudget:HAS_BUDGET]->()

            DELETE oldBudget

            WITH u

            OPTIONAL MATCH
                (u)-[oldTime:HAS_TIME]->()

            DELETE oldTime

            // -----------------------------------------------
            // สร้างเพื่อน
            // -----------------------------------------------

            WITH u

            FOREACH (
                friendName IN $friends |

                MERGE (f:User {name: friendName})

                MERGE (u)-[:FRIEND_OF]-(f)
            )

            // -----------------------------------------------
            // เชื่อมที่อยู่อาศัย
            // -----------------------------------------------

            WITH u

            MERGE (space:LivingSpace {name: $space})

            MERGE (u)-[:LIVES_IN]->(space)

            // -----------------------------------------------
            // เชื่อมงบประมาณ
            // -----------------------------------------------

            WITH u

            MERGE (budget:Budget {name: $budget})

            MERGE (u)-[:HAS_BUDGET]->(budget)

            // -----------------------------------------------
            // เชื่อมเวลาที่มี
            // -----------------------------------------------

            WITH u

            MERGE (time:TimeAvailable {name: $time})

            MERGE (u)-[:HAS_TIME]->(time)

            RETURN u.name AS User

            """

            driver.execute_query(
                save_query,
                user=selected_user,
                friends=selected_friends,
                space=user_space,
                budget=user_budget,
                time=user_time
            )

            # =================================================
            # SUCCESS MESSAGE
            # =================================================

            st.success(
                f"✅ บันทึกข้อมูลของ {selected_user} ลง Neo4j แล้ว"
            )

            if selected_friends:

                st.info(
                    "👥 เพื่อนที่บันทึก: "
                    + ", ".join(selected_friends)
                )

            else:

                st.info(
                    "👥 ผู้ใช้คนนี้ยังไม่ได้เลือกเพื่อน"
                )

            # =================================================
            # RECOMMEND PET
            # =================================================

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
                        WHEN $space IN spaces
                        THEN 1
                        ELSE 0
                    END

                    +

                    CASE
                        WHEN budget = $budget
                        THEN 1
                        ELSE 0
                    END

                    +

                    CASE
                        WHEN time = $time
                        THEN 1
                        ELSE 0
                    END

                    AS score

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

            # =================================================
            # RECOMMENDATION TITLE
            # =================================================

            st.divider()

            st.subheader(
                f"🐾 สัตว์เลี้ยงที่เหมาะกับ {selected_user}"
            )

            # =================================================
            # DISPLAY RESULTS
            # =================================================

            records = result.records

            if not records:

                st.warning(
                    "ไม่พบข้อมูลสัตว์เลี้ยงใน Neo4j"
                )

            else:

                for record in records:

                    pet_name = record["Pet"]

                    description = (
                        DESCRIPTION_TH.get(
                            pet_name,
                            record["Description"] or ""
                        )
                    )

                    score = record["Score"]

                    spaces = record["SuitableSpace"] or []

                    budget = record["Budget"]

                    time_available = record["TimeAvailable"]

                    pet_th = PET_TH.get(
                        pet_name,
                        pet_name
                    )

                    image_path = get_pet_image(
                        pet_name
                    )

                    # -----------------------------------------
                    # CARD
                    # -----------------------------------------

                    st.markdown(
                        '<div class="pet-card">',
                        unsafe_allow_html=True
                    )

                    col_img, col_info = st.columns(
                        [1, 2]
                    )

                    # -----------------------------------------
                    # IMAGE
                    # -----------------------------------------

                    with col_img:

                        if image_path:

                            st.image(
                                image_path,
                                use_container_width=True
                            )

                        else:

                            st.info(
                                "ยังไม่มีรูป"
                            )

                    # -----------------------------------------
                    # INFORMATION
                    # -----------------------------------------

                    with col_info:

                        st.markdown(
                            f'<div class="pet-name">{pet_th}</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'<div class="score">คะแนนความเหมาะสม: {score}/3</div>',
                            unsafe_allow_html=True
                        )

                        st.write(
                            description
                        )

                        # Suitable spaces

                        thai_spaces = [
                            SPACE_TH.get(
                                x,
                                x
                            )
                            for x in spaces
                        ]

                        st.write(
                            "🏠 พื้นที่ที่เหมาะสม: "
                            + (
                                ", ".join(thai_spaces)
                                if thai_spaces
                                else "-"
                            )
                        )

                        # Budget

                        st.write(
                            "💰 งบประมาณ: "
                            + BUDGET_TH.get(
                                budget,
                                budget or "-"
                            )
                        )

                        # Time

                        st.write(
                            "⏰ เวลาที่ต้องใช้ดูแล: "
                            + TIME_TH.get(
                                time_available,
                                time_available or "-"
                            )
                        )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        except Exception as e:

            st.error(
                "❌ เกิดข้อผิดพลาดในการเชื่อมต่อหรือบันทึกข้อมูล"
            )

            st.code(
                str(e)
            )


# =========================================================
# PET GUIDE PAGE
# =========================================================

elif page == "🐾 คู่มือสัตว์เลี้ยง":

    st.markdown(
        '<div class="main-title">🐾 คู่มือสัตว์เลี้ยง</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">ข้อมูลเบื้องต้นเกี่ยวกับสัตว์เลี้ยงแต่ละชนิด</div>',
        unsafe_allow_html=True
    )

    try:

        driver = get_driver()

        result = driver.execute_query(
            """

            MATCH (p:Pet)

            RETURN
                p.name AS Pet,
                p.description AS Description

            ORDER BY Pet

            """
        )

        records = result.records

        if not records:

            st.warning(
                "ไม่พบข้อมูลสัตว์เลี้ยง"
            )

        else:

            for record in records:

                pet_name = record["Pet"]

                pet_th = PET_TH.get(
                    pet_name,
                    pet_name
                )

                description = DESCRIPTION_TH.get(
                    pet_name,
                    record["Description"] or ""
                )

                image_path = get_pet_image(
                    pet_name
                )

                col1, col2 = st.columns(
                    [1, 2]
                )

                with col1:

                    if image_path:

                        st.image(
                            image_path,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "ยังไม่มีรูป"
                        )

                with col2:

                    st.subheader(
                        pet_th
                    )

                    st.write(
                        description
                    )

                st.divider()

    except Exception as e:

        st.error(
            "ไม่สามารถโหลดข้อมูลสัตว์เลี้ยงได้"
        )

        st.code(
            str(e)
        )


# =========================================================
# ADMIN PAGE
# =========================================================

elif page == "🔐 ผู้ดูแลระบบ":

    st.markdown(
        '<div class="main-title">🔐 ผู้ดูแลระบบ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">จัดการข้อมูลสัตว์เลี้ยง</div>',
        unsafe_allow_html=True
    )

    try:

        driver = get_driver()

        # =================================================
        # GET PETS
        # =================================================

        result = driver.execute_query(
            """

            MATCH (p:Pet)

            RETURN
                p.name AS Pet,
                p.description AS Description

            ORDER BY Pet

            """
        )

        pet_records = result.records

        # =================================================
        # ADD PET
        # =================================================

        st.subheader(
            "➕ เพิ่มสัตว์เลี้ยง"
        )

        with st.form("add_pet_form"):

            new_pet_name = st.text_input(
                "ชื่อสัตว์เลี้ยง"
            )

            new_description = st.text_area(
                "คำอธิบาย"
            )

            new_spaces = st.multiselect(
                "พื้นที่ที่เหมาะสม",
                [
                    "House",
                    "Condo",
                    "Farm",
                    "Outdoor Space"
                ]
            )

            new_budget = st.selectbox(
                "งบประมาณ",
                [
                    "Low",
                    "Medium",
                    "High"
                ]
            )

            new_time = st.selectbox(
                "เวลาที่ต้องใช้ดูแล",
                [
                    "Low",
                    "Medium",
                    "High"
                ]
            )

            add_submit = st.form_submit_button(
                "เพิ่มสัตว์เลี้ยง",
                use_container_width=True
            )

        if add_submit:

            if not new_pet_name.strip():

                st.warning(
                    "กรุณากรอกชื่อสัตว์เลี้ยง"
                )

            else:

                try:

                    driver.execute_query(
                        """

                        MERGE (p:Pet {
                            name: $name
                        })

                        SET p.description = $description

                        WITH p

                        FOREACH (
                            spaceName IN $spaces |

                            MERGE (
                                s:LivingSpace {
                                    name: spaceName
                                }
                            )

                            MERGE (
                                p)-[:SUITABLE_FOR]->(s)
                            )
                        
                        WITH p

                        MERGE (
                            b:Budget {
                                name: $budget
                            }
                        )

                        MERGE (
                            p)-[:COST_LEVEL]->(b)
                        )

                        WITH p

                        MERGE (
                            t:TimeAvailable {
                                name: $time
                            }
                        )

                        MERGE (
                            p)-[:NEEDS_TIME]->(t)

                        """,

                        name=new_pet_name.strip(),
                        description=new_description,
                        spaces=new_spaces,
                        budget=new_budget,
                        time=new_time
                    )

                    st.success(
                        f"เพิ่ม {new_pet_name} สำเร็จ"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "ไม่สามารถเพิ่มข้อมูลได้"
                    )

                    st.code(
                        str(e)
                    )

        st.divider()

        # =================================================
        # EDIT PET
        # =================================================

        st.subheader(
            "✏️ แก้ไขสัตว์เลี้ยง"
        )

        if pet_records:

            pet_names = [
                r["Pet"]
                for r in pet_records
            ]

            selected_pet = st.selectbox(
                "เลือกสัตว์เลี้ยง",
                pet_names,
                key="edit_pet"
            )

            selected_data = next(
                (
                    r for r in pet_records
                    if r["Pet"] == selected_pet
                ),
                None
            )

            current_description = (
                selected_data["Description"]
                if selected_data
                else ""
            )

            with st.form("edit_pet_form"):

                edit_description = st.text_area(
                    "คำอธิบาย",
                    value=current_description or ""
                )

                edit_spaces = st.multiselect(
                    "พื้นที่ที่เหมาะสม",
                    [
                        "House",
                        "Condo",
                        "Farm",
                        "Outdoor Space"
                    ]
                )

                edit_budget = st.selectbox(
                    "งบประมาณ",
                    [
                        "Low",
                        "Medium",
                        "High"
                    ]
                )

                edit_time = st.selectbox(
                    "เวลาที่ต้องใช้ดูแล",
                    [
                        "Low",
                        "Medium",
                        "High"
                    ]
                )

                edit_submit = st.form_submit_button(
                    "บันทึกการแก้ไข",
                    use_container_width=True
                )

            if edit_submit:

                try:

                    driver.execute_query(
                        """

                        MATCH (p:Pet {
                            name: $name
                        })

                        SET p.description = $description

                        // ลบความสัมพันธ์เดิม

                        OPTIONAL MATCH
                            (p)-[
                                r:SUITABLE_FOR|
                                COST_LEVEL|
                                NEEDS_TIME
                            ]->()

                        DELETE r

                        WITH p

                        // สร้างพื้นที่ใหม่

                        FOREACH (
                            spaceName IN $spaces |

                            MERGE (
                                s:LivingSpace {
                                    name: spaceName
                                }
                            )

                            MERGE (
                                p)-[:SUITABLE_FOR]->(s)
                        )

                        WITH p

                        // สร้างงบประมาณใหม่

                        MERGE (
                            b:Budget {
                                name: $budget
                            }
                        )

                        MERGE (
                            p)-[:COST_LEVEL]->(b)

                        WITH p

                        // สร้างเวลาที่ต้องใช้ใหม่

                        MERGE (
                            t:TimeAvailable {
                                name: $time
                            }
                        )

                        MERGE (
                            p)-[:NEEDS_TIME]->(t)

                        """,

                        name=selected_pet,
                        description=edit_description,
                        spaces=edit_spaces,
                        budget=edit_budget,
                        time=edit_time
                    )

                    st.success(
                        f"แก้ไข {selected_pet} สำเร็จ"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "ไม่สามารถแก้ไขข้อมูลได้"
                    )

                    st.code(
                        str(e)
                    )

        else:

            st.info(
                "ยังไม่มีข้อมูลสัตว์เลี้ยง"
            )

        st.divider()

        # =================================================
        # DELETE PET
        # =================================================

        st.subheader(
            "🗑️ ลบสัตว์เลี้ยง"
        )

        if pet_records:

            delete_pet = st.selectbox(
                "เลือกสัตว์เลี้ยงที่ต้องการลบ",
                [
                    r["Pet"]
                    for r in pet_records
                ],
                key="delete_pet"
            )

            if st.button(
                "🗑️ ลบสัตว์เลี้ยง",
                use_container_width=True
            ):

                try:

                    driver.execute_query(
                        """

                        MATCH (
                            p:Pet {
                                name: $name
                            }
                        )

                        DETACH DELETE p

                        """,

                        name=delete_pet
                    )

                    st.success(
                        f"ลบ {delete_pet} สำเร็จ"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "ไม่สามารถลบข้อมูลได้"
                    )

                    st.code(
                        str(e)
                    )

        else:

            st.info(
                "ไม่มีข้อมูลสำหรับลบ"
            )

    except Exception as e:

        st.error(
            "ไม่สามารถเชื่อมต่อ Neo4j ได้"
        )

        st.code(
            str(e)
        )
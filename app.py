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

st.markdown(
    """
    <style>

    .stApp {
        background-color: #ffffff;
    }

    h1, h2, h3 {
        color: #333333;
    }

    p, label, div {
        font-size: 18px;
    }

    .pet-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-bottom: 20px;
        background-color: #fafafa;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# IMAGE
# =========================================================

IMAGE_DIR = Path(__file__).parent / "images"


def get_pet_image(pet_name):

    file_names = [
        f"{pet_name.lower()}.jpg",
        f"{pet_name.lower()}.jpeg",
        f"{pet_name.lower()}.png",
        f"{pet_name.lower()}.webp"
    ]

    for file_name in file_names:

        image_path = IMAGE_DIR / file_name

        if image_path.exists():
            return str(image_path)

    return None


# =========================================================
# PET TRANSLATION
# =========================================================

pet_thai = {

    "Dog": "สุนัข",
    "Cat": "แมว",
    "Bird": "นก",
    "Rabbit": "กระต่าย",
    "Fish": "ปลา",
    "Hamster": "หนูแฮมสเตอร์",
    "Duck": "เป็ด",
    "Sheep": "แกะ",
    "Turtle": "เต่า",
    "Horse": "ม้า"

}


# =========================================================
# PET DESCRIPTION
# =========================================================

pet_description = {

    "Dog":
        "สุนัขเป็นสัตว์เลี้ยงที่รักเจ้าของและสามารถฝึกฝนได้ เหมาะกับผู้ที่มีเวลาในการดูแลและต้องการสัตว์เลี้ยงที่สามารถทำกิจกรรมร่วมกันได้",

    "Cat":
        "แมวเป็นสัตว์เลี้ยงที่ดูแลง่ายและค่อนข้างเป็นอิสระ เหมาะกับผู้ที่อาศัยอยู่ในบ้านหรือคอนโด",

    "Bird":
        "นกเป็นสัตว์เลี้ยงที่ใช้พื้นที่ไม่มาก และสามารถเลี้ยงในบ้านได้ เหมาะกับผู้ที่ต้องการสัตว์เลี้ยงขนาดเล็ก",

    "Rabbit":
        "กระต่ายเป็นสัตว์เลี้ยงขนาดเล็กที่น่ารัก ต้องการพื้นที่สะอาดและการดูแลอย่างสม่ำเสมอ",

    "Fish":
        "ปลาเป็นสัตว์เลี้ยงที่ใช้พื้นที่ไม่มาก เหมาะกับผู้ที่มีพื้นที่จำกัดและต้องการสัตว์เลี้ยงที่ดูแลไม่ซับซ้อน",

    "Hamster":
        "หนูแฮมสเตอร์เป็นสัตว์เลี้ยงขนาดเล็ก ใช้พื้นที่ไม่มาก และเหมาะกับการเลี้ยงภายในบ้าน",

    "Duck":
        "เป็ดต้องการพื้นที่และการดูแลมากกว่าสัตว์เลี้ยงขนาดเล็ก เหมาะกับบ้านหรือพื้นที่ที่มีบริเวณกว้าง",

    "Sheep":
        "แกะต้องการพื้นที่ในการเลี้ยงและอาหารที่เหมาะสม เหมาะกับผู้ที่มีพื้นที่กว้างหรือพื้นที่ฟาร์ม",

    "Turtle":
        "เต่าเป็นสัตว์เลี้ยงที่ค่อนข้างดูแลง่าย แต่ต้องจัดสภาพแวดล้อมและอาหารให้เหมาะสม",

    "Horse":
        "ม้าต้องการพื้นที่กว้าง เวลาในการดูแล และค่าใช้จ่ายค่อนข้างสูง เหมาะกับผู้ที่มีพื้นที่และมีเวลาในการดูแล"

}


# =========================================================
# NEO4J
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
# SIDEBAR
# =========================================================

st.sidebar.title("🐾 ระบบแนะนำสัตว์เลี้ยง")

page = st.sidebar.radio(
    "เมนู",
    [
        "🏠 หน้าหลัก",
        "🐾 คู่มือสัตว์เลี้ยง",
        "🔐 ผู้ดูแลระบบ"
    ]
)


# =========================================================
# HOME
# =========================================================

if page == "🏠 หน้าหลัก":

    st.title("🐾 ระบบแนะนำสัตว์เลี้ยง")

    st.write(
        "เลือกลักษณะของคุณ แล้วระบบจะแนะนำสัตว์เลี้ยงที่เหมาะสม"
    )

    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

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
    # FRIEND
    # -----------------------------------------------------

    friend_options = [
        name
        for name in user_names
        if name != selected_user
    ]

    selected_friends = st.multiselect(
        "คุณเป็นเพื่อนกับใคร?",
        friend_options
    )

    # -----------------------------------------------------
    # LIVING SPACE
    # -----------------------------------------------------

    space_thai = {
        "บ้าน": "House",
        "คอนโด": "Condo",
        "ฟาร์ม": "Farm",
        "พื้นที่กลางแจ้ง": "Outdoor Space"
    }

    selected_space_thai = st.selectbox(
        "คุณอาศัยอยู่ที่ไหน?",
        list(space_thai.keys())
    )

    user_space = space_thai[selected_space_thai]

    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    budget_thai = {
        "ต่ำ": "Low",
        "ปานกลาง": "Medium",
        "สูง": "High"
    }

    selected_budget_thai = st.selectbox(
        "งบประมาณในการเลี้ยง",
        list(budget_thai.keys())
    )

    user_budget = budget_thai[selected_budget_thai]

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    time_thai = {
        "น้อย": "Low",
        "ปานกลาง": "Medium",
        "มาก": "High"
    }

    selected_time_thai = st.selectbox(
        "เวลาที่มีสำหรับดูแลสัตว์",
        list(time_thai.keys())
    )

    user_time = time_thai[selected_time_thai]

    # =====================================================
    # RECOMMEND BUTTON
    # =====================================================

    if st.button(
        "🐾 แนะนำสัตว์เลี้ยง",
        use_container_width=True
    ):

        try:

            driver = get_driver()

            # =================================================
            # 1. SAVE USER / FRIEND / LIFESTYLE
            # =================================================

            driver.execute_query(
                """
                MERGE (u:User {name: $user})

                // ---------------------------------------------
                // ลบเพื่อนเดิม
                // ---------------------------------------------

                WITH u

                OPTIONAL MATCH
                    (u)-[oldFriend:FRIEND_OF]-(:User)

                DELETE oldFriend

                // ---------------------------------------------
                // ลบที่อยู่อาศัยเดิม
                // ---------------------------------------------

                WITH u

                OPTIONAL MATCH
                    (u)-[oldSpace:LIVES_IN]->()

                DELETE oldSpace

                // ---------------------------------------------
                // ลบงบประมาณเดิม
                // ---------------------------------------------

                WITH u

                OPTIONAL MATCH
                    (u)-[oldBudget:HAS_BUDGET]->()

                DELETE oldBudget

                // ---------------------------------------------
                // ลบเวลาเดิม
                // ---------------------------------------------

                WITH u

                OPTIONAL MATCH
                    (u)-[oldTime:HAS_TIME]->()

                DELETE oldTime

                // ---------------------------------------------
                // ลบคำแนะนำเดิม
                // ---------------------------------------------

                WITH u

                OPTIONAL MATCH
                    (u)-[oldRecommendation:RECOMMENDED]->()

                DELETE oldRecommendation

                // ---------------------------------------------
                // สร้างเพื่อน
                // ---------------------------------------------

                WITH u

                FOREACH (
                    friendName IN $friends |

                    MERGE (f:User {
                        name: friendName
                    })

                    MERGE (u)-[:FRIEND_OF]->(f)
                )

                // ---------------------------------------------
                // ที่อยู่อาศัย
                // ---------------------------------------------

                WITH u

                MERGE (
                    space:LivingSpace {
                        name: $space
                    }
                )

                MERGE (u)-[:LIVES_IN]->(space)

                // ---------------------------------------------
                // งบประมาณ
                // ---------------------------------------------

                WITH u

                MERGE (
                    budget:Budget {
                        name: $budget
                    }
                )

                MERGE (u)-[:HAS_BUDGET]->(budget)

                // ---------------------------------------------
                // เวลา
                // ---------------------------------------------

                WITH u

                MERGE (
                    time:TimeAvailable {
                        name: $time
                    }
                )

                MERGE (u)-[:HAS_TIME]->(time)

                RETURN u.name AS User
                """,

                user=selected_user,
                friends=selected_friends,
                space=user_space,
                budget=user_budget,
                time=user_time
            )

            # =================================================
            # 2. CALCULATE PET SCORE
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

            records = result.records

            # =================================================
            # NO PET
            # =================================================

            if not records:

                st.warning(
                    "ไม่พบข้อมูลสัตว์เลี้ยงใน Neo4j"
                )

            else:

                # =================================================
                # 3. FIND MAX SCORE
                # =================================================

                max_score = max(
                    record["Score"]
                    for record in records
                )

                # =================================================
                # 4. SAVE RECOMMENDED RELATIONSHIP
                # =================================================

                driver.execute_query(
                    """
                    MATCH (u:User {
                        name: $user
                    })

                    MATCH (p:Pet)

                    OPTIONAL MATCH
                        (p)-[:SUITABLE_FOR]->(space:LivingSpace)

                    OPTIONAL MATCH
                        (p)-[:COST_LEVEL]->(budget:Budget)

                    OPTIONAL MATCH
                        (p)-[:NEEDS_TIME]->(time:TimeAvailable)

                    WITH
                        u,
                        p,
                        collect(DISTINCT space.name) AS spaces,
                        collect(DISTINCT budget.name)[0] AS budget,
                        collect(DISTINCT time.name)[0] AS time

                    WITH
                        u,
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
                        END AS score

                    WHERE score = $max_score

                    MERGE (u)-[r:RECOMMENDED]->(p)

                    SET r.score = score

                    RETURN
                        u.name AS User,
                        p.name AS Pet,
                        r.score AS Score
                    """,

                    user=selected_user,
                    space=user_space,
                    budget=user_budget,
                    time=user_time,
                    max_score=max_score
                )

                # =================================================
                # 5. SHOW RECOMMENDATIONS
                # =================================================

                st.success(
                    f"พบสัตว์เลี้ยงที่เหมาะสมกับคุณ "
                    f"คะแนนสูงสุด {max_score}/3"
                )

                st.subheader("🐾 สัตว์เลี้ยงที่แนะนำ")

                # เรียงจากคะแนนมากไปน้อย
                sorted_records = sorted(
                    records,
                    key=lambda x: x["Score"],
                    reverse=True
                )

                for record in sorted_records:

                    pet_name = record["Pet"]
                    thai_name = pet_thai.get(
                        pet_name,
                        pet_name
                    )

                    score = record["Score"]

                    description = pet_description.get(
                        pet_name,
                        record["Description"] or ""
                    )

                    image_path = get_pet_image(
                        pet_name
                    )

                    with st.container():

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
                                    "ไม่มีรูปภาพ"
                                )

                        with col2:

                            st.subheader(
                                f"🐾 {thai_name}"
                            )

                            st.write(
                                f"คะแนนความเหมาะสม: "
                                f"**{score}/3**"
                            )

                            st.write(
                                description
                            )

                        st.divider()

                # =================================================
                # 6. GET GRAPH DATA
                # =================================================

                graph_result = driver.execute_query(
                    """
                    MATCH (u:User {
                        name: $user
                    })-[r]-(x)

                    RETURN
                        u.name AS User,
                        type(r) AS Relationship,
                        labels(x)[0] AS NodeType,
                        x.name AS Target,
                        CASE
                            WHEN type(r) = "RECOMMENDED"
                            THEN r.score
                            ELSE null
                        END AS Score

                    ORDER BY Relationship, Target
                    """,

                    user=selected_user
                )

                graph_records = graph_result.records

                # =================================================
                # 7. STREAMLIT GRAPH
                # =================================================

                st.subheader(
                    "🔗 กราฟความสัมพันธ์"
                )

                st.caption(
                    "กราฟนี้แสดงข้อมูลตามตัวเลือกที่คุณเลือก "
                    "และสัตว์เลี้ยงที่ระบบแนะนำ"
                )

                # -------------------------------------------------
                # DOT GRAPH
                # -------------------------------------------------

                dot_lines = []

                dot_lines.append(
                    'digraph G {'
                )

                dot_lines.append(
                    'graph [rankdir=LR, bgcolor="white"];'
                )

                dot_lines.append(
                    'node [shape=box, style="rounded,filled", fontname="Tahoma"];'
                )

                dot_lines.append(
                    'edge [fontname="Tahoma"];'
                )

                # -------------------------------------------------
                # User node
                # -------------------------------------------------

                user_id = "user_main"

                dot_lines.append(
                    f'"{user_id}" '
                    f'[label="👤 {selected_user}", '
                    f'fillcolor="#FFF3CD"];'
                )

                # -------------------------------------------------
                # Create unique node names
                # -------------------------------------------------

                node_counter = 0

                target_nodes = {}

                for record in graph_records:

                    target = record["Target"]
                    node_type = record["NodeType"]

                    if target not in target_nodes:

                        node_counter += 1

                        target_id = (
                            f"node_{node_counter}"
                        )

                        target_nodes[
                            target
                        ] = target_id

                        # -----------------------------------------
                        # User
                        # -----------------------------------------

                        if node_type == "User":

                            label = (
                                f"👤 {target}"
                            )

                            fill_color = "#E3F2FD"

                        # -----------------------------------------
                        # Pet
                        # -----------------------------------------

                        elif node_type == "Pet":

                            label = (
                                f"🐾 "
                                f"{pet_thai.get(target, target)}"
                            )

                            fill_color = "#E8F5E9"

                        # -----------------------------------------
                        # Living Space
                        # -----------------------------------------

                        elif node_type == "LivingSpace":

                            space_labels = {
                                "House": "🏠 บ้าน",
                                "Condo": "🏢 คอนโด",
                                "Farm": "🌾 ฟาร์ม",
                                "Outdoor Space":
                                    "🌳 พื้นที่กลางแจ้ง"
                            }

                            label = space_labels.get(
                                target,
                                target
                            )

                            fill_color = "#FFF3E0"

                        # -----------------------------------------
                        # Budget
                        # -----------------------------------------

                        elif node_type == "Budget":

                            budget_labels = {
                                "Low": "💰 งบต่ำ",
                                "Medium": "💰 งบปานกลาง",
                                "High": "💰 งบสูง"
                            }

                            label = budget_labels.get(
                                target,
                                target
                            )

                            fill_color = "#FCE4EC"

                        # -----------------------------------------
                        # Time
                        # -----------------------------------------

                        elif node_type == "TimeAvailable":

                            time_labels = {
                                "Low": "⏰ เวลาน้อย",
                                "Medium":
                                    "⏰ เวลาปานกลาง",
                                "High": "⏰ เวลามาก"
                            }

                            label = time_labels.get(
                                target,
                                target
                            )

                            fill_color = "#EDE7F6"

                        else:

                            label = target
                            fill_color = "#F5F5F5"

                        dot_lines.append(
                            f'"{target_id}" '
                            f'[label="{label}", '
                            f'fillcolor="{fill_color}"];'
                        )

                # -------------------------------------------------
                # Edges
                # -------------------------------------------------

                for record in graph_records:

                    target = record["Target"]
                    relationship = record[
                        "Relationship"
                    ]

                    target_id = target_nodes[
                        target
                    ]

                    # -----------------------------
                    # Thai relationship names
                    # -----------------------------

                    relationship_thai = {

                        "FRIEND_OF":
                            "เป็นเพื่อน",

                        "LIVES_IN":
                            "อาศัยอยู่",

                        "HAS_BUDGET":
                            "งบประมาณ",

                        "HAS_TIME":
                            "เวลาที่มี",

                        "RECOMMENDED":
                            "แนะนำ"

                    }

                    edge_label = relationship_thai.get(
                        relationship,
                        relationship
                    )

                    # -----------------------------
                    # Recommendation score
                    # -----------------------------

                    score = record["Score"]

                    if (
                        relationship == "RECOMMENDED"
                        and score is not None
                    ):

                        edge_label = (
                            f"แนะนำ "
                            f"(คะแนน {score}/3)"
                        )

                    dot_lines.append(
                        f'"{user_id}" -> '
                        f'"{target_id}" '
                        f'[label="{edge_label}"];'
                    )

                dot_lines.append(
                    "}"
                )

                dot_graph = "\n".join(
                    dot_lines
                )

                st.graphviz_chart(
                    dot_graph,
                    use_container_width=True
                )

                # =================================================
                # 8. DEBUG RELATIONSHIP
                # =================================================

                with st.expander(
                    "ดูข้อมูลความสัมพันธ์ที่บันทึกใน Neo4j"
                ):

                    for record in graph_records:

                        if (
                            record["Relationship"]
                            == "RECOMMENDED"
                        ):

                            st.write(
                                f"👤 {record['User']} "
                                f"— {record['Relationship']} "
                                f"→ 🐾 "
                                f"{pet_thai.get(record['Target'], record['Target'])} "
                                f"(คะแนน {record['Score']}/3)"
                            )

                        else:

                            st.write(
                                f"👤 {record['User']} "
                                f"— {record['Relationship']} "
                                f"→ {record['Target']}"
                            )

        except Exception as e:

            st.error(
                "เกิดข้อผิดพลาดในการเชื่อมต่อหรือบันทึกข้อมูล"
            )

            st.code(
                str(e)
            )


# =========================================================
# PET GUIDE
# =========================================================

elif page == "🐾 คู่มือสัตว์เลี้ยง":

    st.title("🐾 คู่มือสัตว์เลี้ยง")

    pets = [
        "Dog",
        "Cat",
        "Bird",
        "Rabbit",
        "Fish",
        "Hamster",
        "Duck",
        "Sheep",
        "Turtle",
        "Horse"
    ]

    for pet in pets:

        thai_name = pet_thai.get(
            pet,
            pet
        )

        image_path = get_pet_image(
            pet
        )

        st.subheader(
            f"🐾 {thai_name}"
        )

        if image_path:

            st.image(
                image_path,
                width=300
            )

        st.write(
            pet_description.get(
                pet,
                "ไม่มีคำอธิบาย"
            )
        )

        st.divider()


# =========================================================
# ADMIN
# =========================================================

elif page == "🔐 ผู้ดูแลระบบ":

    st.title("🔐 ผู้ดูแลระบบ")

    admin_username = st.text_input(
        "ชื่อผู้ใช้"
    )

    admin_password = st.text_input(
        "รหัสผ่าน",
        type="password"
    )

    if st.button("เข้าสู่ระบบ"):

        if (
            admin_username == "admin"
            and admin_password == "admin123"
        ):

            st.session_state["admin_login"] = True

        else:

            st.error(
                "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
            )

    if st.session_state.get(
        "admin_login",
        False
    ):

        st.success(
            "เข้าสู่ระบบผู้ดูแลสำเร็จ"
        )

        try:

            driver = get_driver()

            # =================================================
            # ADMIN STATISTICS
            # =================================================

            st.subheader(
                "📊 ข้อมูลในระบบ"
            )

            pet_count_result = driver.execute_query(
                """
                MATCH (p:Pet)
                RETURN count(p) AS count
                """
            )

            user_count_result = driver.execute_query(
                """
                MATCH (u:User)
                RETURN count(u) AS count
                """
            )

            relationship_count_result = driver.execute_query(
                """
                MATCH ()-[r]->()
                RETURN count(r) AS count
                """
            )

            pet_count = (
                pet_count_result.records[0]["count"]
            )

            user_count = (
                user_count_result.records[0]["count"]
            )

            relationship_count = (
                relationship_count_result.records[0]["count"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "สัตว์เลี้ยง",
                    pet_count
                )

            with col2:

                st.metric(
                    "ผู้ใช้",
                    user_count
                )

            with col3:

                st.metric(
                    "ความสัมพันธ์",
                    relationship_count
                )

            # =================================================
            # SHOW PETS
            # =================================================

            st.subheader(
                "🐾 สัตว์เลี้ยงในระบบ"
            )

            pet_result = driver.execute_query(
                """
                MATCH (p:Pet)
                RETURN
                    p.name AS name,
                    p.description AS description
                ORDER BY p.name
                """
            )

            for record in pet_result.records:

                st.write(
                    f"🐾 **{pet_thai.get(record['name'], record['name'])}**"
                )

                st.write(
                    record["description"] or ""
                )

                st.divider()

        except Exception as e:

            st.error(
                "ไม่สามารถโหลดข้อมูล Admin ได้"
            )

            st.code(
                str(e)
            )
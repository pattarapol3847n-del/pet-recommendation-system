import streamlit as st
from neo4j import GraphDatabase


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pet Recommendation System",
    page_icon="🐾",
    layout="wide"
)


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

    st.title("🐾 Pet Guide")

    st.write(
        "Learn about different types of pets, "
        "their personality, characteristics, and care needs."
    )

    st.markdown("---")


    # =====================================================
    # PET INFORMATION
    # =====================================================

    pets = [

        {
            "name": "Dog",
            "emoji": "🐶",
            "personality": "Friendly and social",
            "description": "Dogs are friendly, social, and active companions.",
            "care": "Needs regular exercise, attention, and daily care."
        },

        {
            "name": "Cat",
            "emoji": "🐱",
            "personality": "Independent and adaptable",
            "description": "Cats are independent animals that can adapt well to different homes.",
            "care": "Needs food, clean water, litter care, and regular health care."
        },

        {
            "name": "Bird",
            "emoji": "🐦",
            "personality": "Social and active",
            "description": "Birds are small companions that can be social and active.",
            "care": "Needs a suitable cage, clean water, food, and social interaction."
        },

        {
            "name": "Rabbit",
            "emoji": "🐰",
            "personality": "Gentle and quiet",
            "description": "Rabbits are gentle and relatively quiet small companions.",
            "care": "Needs clean living space, proper food, and regular care."
        },

        {
            "name": "Fish",
            "emoji": "🐟",
            "personality": "Quiet and calm",
            "description": "Fish are quiet aquatic pets that can be suitable for small living spaces.",
            "care": "Needs a suitable aquarium, clean water, and regular feeding."
        },

        {
            "name": "Hamster",
            "emoji": "🐹",
            "personality": "Small and active",
            "description": "Hamsters are small companions that are easy to observe and care for.",
            "care": "Needs a clean enclosure, food, water, and suitable exercise equipment."
        },

        {
            "name": "Duck",
            "emoji": "🦆",
            "personality": "Social and active",
            "description": "Ducks are social animals that need suitable outdoor space.",
            "care": "Needs outdoor space, clean water, food, and regular care."
        },

        {
            "name": "Sheep",
            "emoji": "🐑",
            "personality": "Social and calm",
            "description": "Sheep are social farm animals that require outdoor space.",
            "care": "Needs suitable land, food, shelter, and regular animal care."
        },

        {
            "name": "Turtle",
            "emoji": "🐢",
            "personality": "Quiet and calm",
            "description": "Turtles are quiet animals and can have a long lifespan.",
            "care": "Needs a suitable habitat, proper food, clean water, and regular care."
        },

        {
            "name": "Horse",
            "emoji": "🐴",
            "personality": "Active and energetic",
            "description": "Horses are large active animals that need significant space.",
            "care": "Needs large outdoor space, regular exercise, food, and extensive care."
        }

    ]


    # =====================================================
    # DISPLAY PET CARDS
    # =====================================================

    for i in range(0, len(pets), 3):

        columns = st.columns(3)

        for j, col in enumerate(columns):

            if i + j < len(pets):

                pet = pets[i + j]

                with col:

                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #444;
                            border-radius: 15px;
                            padding: 20px;
                            margin-bottom: 20px;
                            min-height: 300px;
                            background-color: rgba(255,255,255,0.04);
                        ">
                            <div style="
                                font-size: 70px;
                                text-align: center;
                            ">
                                {pet["emoji"]}
                            </div>

                            <h2 style="
                                text-align: center;
                            ">
                                {pet["name"]}
                            </h2>

                            <p>
                                <b>Personality:</b>
                                {pet["personality"]}
                            </p>

                            <p>
                                <b>Description:</b>
                                {pet["description"]}
                            </p>

                            <p>
                                <b>Care:</b>
                                {pet["care"]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


    st.markdown("---")

    st.info(
        "💡 The information and images on this page "
        "can be expanded later to provide more details "
        "about each pet."
    )
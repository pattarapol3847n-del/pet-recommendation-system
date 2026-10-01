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
        "Explore different types of pets and learn about "
        "their personality, characteristics, and care needs."
    )

    st.markdown("---")


    # =====================================================
    # PET INFORMATION
    # =====================================================

    pets = [

        {
            "name": "Dog",
            "personality": "Friendly and social",
            "description": (
                "Dogs are friendly and social companions. "
                "They often enjoy spending time with people "
                "and regular activities."
            ),
            "care": (
                "Needs regular exercise, attention, "
                "food, clean water, and health care."
            )
        },

        {
            "name": "Cat",
            "personality": "Independent and adaptable",
            "description": (
                "Cats are independent animals that can "
                "adapt well to different home environments."
            ),
            "care": (
                "Needs food, clean water, litter care, "
                "playtime, and regular health care."
            )
        },

        {
            "name": "Bird",
            "personality": "Social and active",
            "description": (
                "Birds are small companions that can be "
                "social, active, and enjoyable to observe."
            ),
            "care": (
                "Needs a suitable cage, clean water, "
                "proper food, and social interaction."
            )
        },

        {
            "name": "Rabbit",
            "personality": "Gentle and quiet",
            "description": (
                "Rabbits are gentle and relatively quiet "
                "small companions."
            ),
            "care": (
                "Needs a clean living space, suitable food, "
                "fresh water, and regular care."
            )
        },

        {
            "name": "Fish",
            "personality": "Quiet and calm",
            "description": (
                "Fish are quiet aquatic pets that can be "
                "suitable for small living spaces."
            ),
            "care": (
                "Needs a suitable aquarium, clean water, "
                "proper food, and regular tank maintenance."
            )
        },

        {
            "name": "Hamster",
            "personality": "Small and active",
            "description": (
                "Hamsters are small companions that are "
                "interesting to observe and care for."
            ),
            "care": (
                "Needs a clean enclosure, suitable food, "
                "fresh water, and exercise equipment."
            )
        },

        {
            "name": "Duck",
            "personality": "Social and active",
            "description": (
                "Ducks are social animals that are active "
                "and need suitable outdoor space."
            ),
            "care": (
                "Needs outdoor space, clean water, proper "
                "food, shelter, and regular care."
            )
        },

        {
            "name": "Sheep",
            "personality": "Social and calm",
            "description": (
                "Sheep are social farm animals that live "
                "well in suitable groups."
            ),
            "care": (
                "Needs suitable land, food, shelter, "
                "clean water, and regular animal care."
            )
        },

        {
            "name": "Turtle",
            "personality": "Quiet and calm",
            "description": (
                "Turtles are quiet animals and can have "
                "a long lifespan."
            ),
            "care": (
                "Needs a suitable habitat, proper food, "
                "clean water, and regular care."
            )
        },

        {
            "name": "Horse",
            "personality": "Active and energetic",
            "description": (
                "Horses are large active animals that need "
                "significant space and regular activity."
            ),
            "care": (
                "Needs large outdoor space, regular exercise, "
                "proper food, shelter, and extensive care."
            )
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
                        f"Image not found for {pet['name']}"
                    )

                st.subheader(
                    f"🐾 {pet['name']}"
                )

                st.markdown(
                    f"**Personality**  \n"
                    f"{pet['personality']}"
                )

                st.markdown(
                    f"**Description**  \n"
                    f"{pet['description']}"
                )

                st.markdown(
                    f"**Care**  \n"
                    f"{pet['care']}"
                )

                st.markdown("---")


    st.info(
        "💡 Choose a pet based on your living space, "
        "budget, and available time."
    )
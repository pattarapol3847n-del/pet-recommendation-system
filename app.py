import streamlit as st
from neo4j import GraphDatabase


st.set_page_config(
    page_title="Pet Recommendation System",
    page_icon="🐾",
    layout="wide"
)


st.title("🐾 Pet Recommendation System")
st.write("Find a pet that matches your lifestyle.")


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


st.subheader("Tell us about your lifestyle")


user_space = st.selectbox(
    "Where do you live?",
    ["House", "Condo", "Farm", "Outdoor Space"]
)


user_budget = st.selectbox(
    "What is your pet budget?",
    ["Low", "Medium", "High"]
)


user_time = st.selectbox(
    "How much time can you spend caring for a pet?",
    ["Low", "Medium", "High"]
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

            st.write(record["Description"])

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

        st.error("Unable to connect to Neo4j.")
        st.write(str(e))
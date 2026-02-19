import streamlit as st
from auth_db import csr, conn


st.title("Welcome to my WebPage")
st.header("My Todo App")


# ----------------------------------
# Journey Plans According To Level
# ----------------------------------

BEGINNER_PLAN = [
    ("Day 1-2: Python Basics", "Variables, loops, data types"),
    ("Day 3: Numpy Basics", "Arrays & operations"),
    ("Day 4: Pandas Basics", "DataFrames & filtering"),
    ("Day 5: Visualization", "Matplotlib basics"),
    ("Day 6: Statistics", "Mean, median, probability"),
    ("Day 7: Mini Project", "Simple data analysis project")
]

INTERMEDIATE_PLAN = [
    ("Day 1: Advanced Pandas", "Data cleaning & grouping"),
    ("Day 2: Data Visualization", "Advanced charts"),
    ("Day 3: SQL Practice", "Joins & aggregations"),
    ("Day 4: EDA Project", "Analyze dataset"),
    ("Day 5: Machine Learning Intro", "Regression basics")
]

EXPERT_PLAN = [
    ("Day 1: ML Model Building", "Regression & classification"),
    ("Day 2: Model Evaluation", "Accuracy & metrics"),
    ("Day 3: Deploy ML Model", "Streamlit deployment"),
    ("Day 4: Build Portfolio", "Upload to GitHub"),
    ("Day 5: Apply Jobs", "Internships & LinkedIn optimization")
]


# -------------------------
# Session Defaults
# -------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "level_selected" not in st.session_state:
    st.session_state.level_selected = False


# -------------------------
# Logged In Section
# -------------------------

if st.session_state.authenticated:

    st.subheader("Select Your Experience Level")

    level = st.selectbox(
        "Choose your level",
        ["Select Level", "Beginner", "Intermediate", "Expert"]
    )

    if level != "Select Level":
        st.session_state.level_selected = True

    # -------------------------
    # Start Journey Button
    # -------------------------

    if st.button("Start My Journey"):

        if level == "Select Level":
            st.warning("Please select your level first!")
        else:

            # Check if already started
            csr.execute(
                """
                SELECT COUNT(*)
                FROM mytodos
                WHERE todo_added=%s
                """,
                (st.session_state.username,)
            )
            exists = csr.fetchone()[0]

            if exists > 0:
                st.info("You have already started your journey!")
            else:

                if level == "Beginner":
                    plan = BEGINNER_PLAN
                elif level == "Intermediate":
                    plan = INTERMEDIATE_PLAN
                else:
                    plan = EXPERT_PLAN

                for title, desc in plan:
                    csr.execute(
                        """
                        INSERT INTO mytodos 
                        (todo_added, todo_title, todo_desc, todo_done, user_level)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            st.session_state.username,
                            title,
                            desc,
                            False,
                            level
                        )
                    )

                conn.commit()
                st.success(f"{level} Journey Started Successfully!")
                st.rerun()


    # -------------------------
    # Show Todos
    # -------------------------

    st.header("My Todos")

    csr.execute(
        """
        SELECT todo_id, todo_title, todo_desc, todo_done
        FROM mytodos
        WHERE todo_added=%s
        ORDER BY todo_id
        """,
        (st.session_state.username,)
    )

    todos = csr.fetchall()

    if todos:
        total = len(todos)
        completed = sum(1 for t in todos if t[3])
        st.progress(completed / total)
        st.write(f"Progress: {completed}/{total} completed")

    for todo_id, title, desc, done in todos:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            checked = st.checkbox(
                "Done",
                value=bool(done),
                key=f"done_{todo_id}"
            )

            if checked != bool(done):
                csr.execute(
                    "UPDATE mytodos SET todo_done=%s WHERE todo_id=%s",
                    (checked, todo_id)
                )
                conn.commit()
                st.rerun()

        with col2:
            st.write(title)

        with col3:
            st.write(desc)

        with col4:
            if st.button("Delete", key=f"del_{todo_id}"):
                csr.execute(
                    "DELETE FROM mytodos WHERE todo_id=%s",
                    (todo_id,)
                )
                conn.commit()
                st.rerun()

        st.divider()


else:
    st.warning("Please login first")
    st.markdown("[Go to Login Page](./login)")




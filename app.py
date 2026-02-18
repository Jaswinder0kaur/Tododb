import streamlit as st
from auth_db import csr, conn

st.title("Welcome to my WebPage")
st.header("My Todo App")


# -------------------------
# Default Data Analytics Todos
# -------------------------
DATA_ANALYTICS_TODOS = [
    ("Learn Python Basics", "Variables, loops, functions, data types"),
    ("Learn Numpy", "Arrays, operations, indexing"),
    ("Learn Pandas", "DataFrames, data cleaning, filtering"),
    ("Data Visualization", "Matplotlib & Seaborn"),
    ("Statistics Basics", "Mean, median, probability"),
    ("Learn SQL", "Queries, joins, aggregations"),
    ("Excel for Analytics", "Pivot tables, formulas"),
    ("Exploratory Data Analysis", "Finding patterns in datasets"),
    ("Build Real Projects", "Work on real-world datasets"),
    ("Machine Learning Basics", "Regression & classification"),
    ("Create Portfolio", "Upload projects on GitHub"),
    ("Apply for Jobs / Internships", "Start your career")
]


# -------------------------
# Session defaults
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""


# -------------------------
# If Logged In
# -------------------------
if st.session_state.authenticated:

    # =========================
    # Career Journey Section
    # =========================
    st.subheader("Choose Your Career Journey")

    journey = st.selectbox(
        "Select a predefined todo journey",
        ["None", "Data Analytics"]
    )

    if st.button("Start Journey"):

        if journey == "Data Analytics":

            # Check if journey already exists for user
            csr.execute(
                """
                SELECT COUNT(*)
                FROM mytodos
                WHERE todo_added=%s
                AND todo_title=%s
                """,
                (st.session_state.username, "Learn Python Basics")
            )

            exists = csr.fetchone()[0]

            if exists > 0:
                st.info("You have already started this journey!")
            else:
                for title, desc in DATA_ANALYTICS_TODOS:
                    csr.execute(
                        """
                        INSERT INTO mytodos 
                        (todo_added, todo_title, todo_desc, todo_done)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (st.session_state.username, title, desc, False)
                    )

                conn.commit()
                st.success("Data Analytics Journey added successfully!")
                st.rerun()


    # =========================
    # Add Todo (Your Original Feature)
    # =========================
    st.subheader(f"Add Todo ({st.session_state.username})")

    title = st.text_input("Enter todo Title")
    desc = st.text_area("Brief about todo")

    if st.button("Add Todo"):

        if not title or not desc:
            st.warning("Please fill all fields")

        else:
            csr.execute(
                """
                INSERT INTO mytodos 
                (todo_added, todo_title, todo_desc, todo_done)
                VALUES (%s, %s, %s, %s)
                """,
                (st.session_state.username, title, desc, False)
            )
            conn.commit()

            st.success("Todo added successfully!")
            st.rerun()


    # =========================
    # Show Todos
    # =========================
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


    # -------- Progress Bar --------
    if todos:
        total = len(todos)
        completed = sum(1 for t in todos if t[3])

        st.progress(completed / total)
        st.write(f"✅ Progress: {completed}/{total} completed")


    # -------- Todo List --------
    for todo_id, title, desc, done in todos:

        c1, c2, c3, c4 = st.columns(4)

        # Done checkbox
        with c1:
            checked = st.checkbox("Done", value=bool(done), key=f"done_{todo_id}")

            if checked != bool(done):
                csr.execute(
                    "UPDATE mytodos SET todo_done=%s WHERE todo_id=%s",
                    (checked, todo_id)
                )
                conn.commit()
                st.rerun()

        # Title
        with c2:
            st.write(title)

        # Description
        with c3:
            st.write(desc)

        # Delete
        with c4:
            if st.button("⛔ Delete", key=f"del_{todo_id}"):
                csr.execute(
                    "DELETE FROM mytodos WHERE todo_id=%s",
                    (todo_id,)
                )
                conn.commit()
                st.rerun()

        st.divider()


# -------------------------
# Not Logged In
# -------------------------
else:
    st.warning("Please login first")
    st.markdown("[Go to Login Page](./login)")



import streamlit as st
from auth_db import csr, conn

st.title("Welcome to my WebPage")
st.header("My Todo App")


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

    st.subheader(f"Add Todo ({st.session_state.username})")

    title = st.text_input("Enter todo Title")
    desc = st.text_area("Brief about todo")

    if st.button("Add Todo"):

        if not title or not desc:
            st.warning("Please fill all fields")

        else:
            csr.execute(
                """
                INSERT INTO mytodos (todo_added, todo_title, todo_desc, todo_done)
                VALUES (%s, %s, %s, %s)
                """,
                (st.session_state.username, title, desc, False)
            )
            conn.commit()

            st.success("Todo added successfully!")
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
        """,
        (st.session_state.username,)
    )

    todos = csr.fetchall()


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


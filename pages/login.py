import streamlit as st
import bcrypt
from auth_db import get_connection


st.title("Login")

username = st.text_input("Enter your Username")
password = st.text_input("Enter Your Password", type="password")

btn = st.button("Login")


if btn:

    if not username or not password:
        st.error("Please fill all fields")

    else:
        try:
            # safer select only required columns
            csr.execute(
                "SELECT username, fullname, password_hash FROM users WHERE username=%s",
                (username,)
            )

            user = csr.fetchone()

            if user is None:
                st.warning("Username not found")

            else:
                db_username, fullname, stored_hash = user

                # fix: ensure bytes
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode()

                if bcrypt.checkpw(password.encode(), stored_hash):

                    st.session_state.authenticated = True
                    st.session_state.username = db_username
                    st.session_state.fullname = fullname

                    st.success(f"Welcome {fullname} 👋")

                    # ❌ remove rerun (causes invisible success)
                    # st.rerun()

                else:
                    st.error("Invalid password")

        except Exception as e:
            st.error(str(e))
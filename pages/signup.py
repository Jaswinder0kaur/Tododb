import streamlit as st
from auth_db import get_connection


import bcrypt

st.title("Signup")

username = st.text_input("Enter your Username")
fullname = st.text_input("Enter your Full Name")
email = st.text_input("Enter your Email")
phonenumber = st.text_input("Enter your Phone Number")
city = st.text_input("Enter your City Name")

password = st.text_input("Enter your Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")


btn = st.button("SignUp")
if btn:
    if not all([username, fullname, email, phonenumber, city, password, confirm_password]):
        st.error("Please fill up all fields")
    # if username == "" or fullname == "" or email == "" or phonenumber == "" or city == "" or password == "" or confirm_password=="":
    #     st.error("Please fill up all fields")
    #     st.snow()
    
    else:
        if password != confirm_password:
            st.warning("conform password do not matchh..")
            st.snow()
        else:
            try:
                # csr.execute(f"insert into signup_user(username, fullname,email, phone_number,city, password1) values('{username}', '{fullname}','{email}',{phonenumber},{city} '{password}')")
                hashed_password = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
                ).decode()
                
                csr.execute(
                """
                INSERT INTO users
                (username, fullname, email, phone_number, city, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (username, fullname, email, phonenumber, city, hashed_password)
                )

                conn.commit()
                st.success("Signup sucessfulllyyy..!")
                st.balloons()
                st.markdown("[Go to login page](./login)")
            
            except Exception as e:
                if "Duplicate" in str(e):
                    st.error("Username or Email already exists")
                else:
                    st.error(str(e))

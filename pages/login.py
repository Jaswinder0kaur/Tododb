import streamlit as st
st.title("Welcome to my login  Page")
Username = st.text_input("Enter your Username")
Password = st.text_input("Enter Your Password", type="password")

btn = st.button("Login")

if btn:
    pass
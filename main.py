import pymysql
import credentials as cr
import streamlit as st

connection = pymysql.connect(
    host=cr.host,
    user=cr.user,
    password=cr.password,
    database=cr.database
)

def main():
    st.title("Registration form")
    st.switch_page("pages/login.py")


if __name__ == "__main__":
    main()
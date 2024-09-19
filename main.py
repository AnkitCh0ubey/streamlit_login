import streamlit as st
import credentials as cr

def main():
    st.title("Registration form")
    cr.state = True
    st.switch_page("pages/login.py")



if __name__ == "__main__":
    main()
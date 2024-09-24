import streamlit as st
from click import launch

import credentials as cr
import os
import pandas as pd

st.set_page_config(layout="centered")

hide_sidebar_style = """
       <style>
           [data-testid="stSidebar"] {
               display: none;
           }
       </style>
   """

st.markdown(hide_sidebar_style, unsafe_allow_html=True)
if cr.key == 1:
    st.success("Welcome to dashboard")

    def display(filename='user_data1.xlsx'):
        if os.path.exists(filename):
            df = pd.read_excel(filename)
            st.dataframe(df)
        else:
            st.warning("No data available to show, reach out to admin")

    if st.button('Load Data'):
        display()

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state.pop('user_name', None)
        st.session_state.pop('user_email', None)
        cr.key = 0
        st.rerun()
      # Rerun the app to reflect changes

else:
    st.warning("Login First")
    st.write('<meta http-equiv="refresh" content="0; url=/login" />', unsafe_allow_html=True)

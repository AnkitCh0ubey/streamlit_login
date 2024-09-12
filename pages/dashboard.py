import streamlit as st
import credentials as cr
import os
import pandas as pd
if cr.key == 1:
    st.session_state['authenticated'] = True

# Check if user is authenticated
query_params = st.session_state.get("query_params", {})
if st.session_state['authenticated'] or query_params.get("logged_in") == ["true"]:
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
        st.session_state.logged_in = False
        cr.key = 0
        st.write('<meta http-equiv="refresh" content="0; url=/login" />', unsafe_allow_html=True)
      # Rerun the app to reflect changes

else:
    st.warning("Login First")

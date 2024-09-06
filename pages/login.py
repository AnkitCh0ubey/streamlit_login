import streamlit as st
import pymysql
import credentials as cr

st.set_page_config(page_title="Login")

connection = pymysql.connect(
    host=cr.host,
    user=cr.user,
    password=cr.password,
    database=cr.database
)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    st.subheader("Login")
    mail = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    try:
        cur = connection.cursor()
        if st.button("Login"):
            if mail == "" or password == "":
                st.error("Please enter both email and password.")
            else:
                sql = "select * from student_register where email=%s and password=%s"
                val = (mail, password)
                cur.execute(sql, val)
                row = cur.fetchone()
                if row is None:
                    st.warning("Error! Invalid EMAIL or PASSWORD")
                else:
                    st.session_state['authenticated'] = True
                    st.success("Login successful! Redirecting to Dashboard...")
                    st.experimental_set_query_params(logged_in="true")
                    st.rerun()
        cur.close()
        connection.close()

    except Exception as e:
        st.error("An unexpected error occurred. Please try again.")


if __name__ == "__main__":
    query_params = st.session_state.get("query_params", {})
    if st.session_state['authenticated'] or query_params.get("logged_in") == ["true"]:
        # Redirect to the dashboard once logged in
        cr.key = 1
        st.write('<meta http-equiv="refresh" content="0; url=/dashboard" />', unsafe_allow_html=True)
    else:
        login()

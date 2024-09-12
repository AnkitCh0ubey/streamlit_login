import streamlit as st
import credentials as cr
import yaml

st.set_page_config(page_title="Login")


def load_credentials():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['users']


def authenticate(mail, password):
    users = load_credentials()
    if mail in users and users[mail]['password'] == password:
        return users[mail]['role']
    return None


if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = None

def login():
    st.subheader("Login")
    mail = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    try:
        if st.button("Login"):
            role = authenticate(mail, password)

            if role == "admin":
                st.session_state['authenticated'] = True
                st.session_state['role'] = role
                st.success("Login successful! Welcome Admin, Redirecting to your workspace...")
                cr.key = 2
                st.write('<meta http-equiv="refresh" content="0; url=/admin_dashboard" />', unsafe_allow_html=True)

            elif mail == "" or password == "":
                st.error("Please enter both email and password.")

            elif role == "user":
                st.session_state['authenticated'] = True
                st.session_state['role'] = role
                st.success("Login successful! Redirecting to Dashboard...")
                cr.key = 1
                st.experimental_set_query_params(logged_in="true")
                st.rerun()

            else:
                st.error("ERROR: Invalid Credentials")

    except Exception as e:
        st.error("An unexpected error occurred. Please try again.")


if __name__ == "__main__":
    query_params = st.session_state.get("query_params", {})
    if st.session_state['authenticated'] or query_params.get("logged_in") == ["true"]:
        # Redirect to the dashboard once logged in
        if cr.key == 1:
            st.write('<meta http-equiv="refresh" content="0; url=/dashboard" />', unsafe_allow_html=True)
        elif cr.key ==2:
            st.write('<meta http-equiv="refresh" content="0; url=/admin_dashboard" />', unsafe_allow_html=True)
    else:
        login()

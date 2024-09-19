import bcrypt
import streamlit as st
from yaml import SafeLoader
import credentials as cr
import yaml
import streamlit_authenticator as stauth


st.set_page_config(page_title="Login")
# if 'authenticated' not in st.session_state:
#     st.session_state['authenticated'] = False





# def authenticate(mail, password):
#     users = load_credentials()
#     if mail in users and users[mail]:
#         stored_password = users[mail]['password']
#         if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
#             return users[mail]['role']
#     return None
#
#


# def login():
#     st.subheader("Login")
#
#     mail = st.text_input("Email Address")
#     password = st.text_input("Password", type="password")
#
#     try:
#         if st.button("Login"):
#             role = authenticate(mail, password)
#
#             if role == "admin":
#                 st.session_state['authenticated'] = True
#                 st.session_state['role'] = role
#                 st.success("Login successful! Welcome Admin, Redirecting to your workspace...")
#                 cr.key = 2
#                 st.write('<meta http-equiv="refresh" content="0; url=/admin_dashboard" />', unsafe_allow_html=True)
#
#             elif mail == "" or password == "":
#                 st.error("Please enter both email and password.")
#
#             elif role == "user":
#                 st.session_state['authenticated'] = True
#                 st.session_state['role'] = role
#                 st.success("Login successful! Redirecting to Dashboard...")
#                 cr.key = 1
#                 st.experimental_set_query_params(logged_in="true")
#                 st.write('<meta http-equiv="refresh" content="0; url=/dashboard" />', unsafe_allow_html=True)
#
#             else:
#                 st.error("ERROR: Invalid Credentials")
#
#     except Exception as e:
#         st.error(f"An unexpected error occurred. Please try again. {e}")

def load_credentials():
    with open('./config.yaml') as file:
      config = yaml.load(file, Loader=SafeLoader)
    return config


def login():
    st.subheader("Login")

    config = load_credentials()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    #login form using authenticator (idk what the hell is this)
    name, auth_status, email = authenticator.login("main")

    if auth_status:
        # If login is successful, get the user's role from the config
        user_role = config['credentials']['usernames'][email]['role']

        # Check if the user is an admin or a regular user
        if user_role == "admin":
            cr.key = 2
            st.success(f"Login successful! Welcome Admin, {name}. Redirecting to your workspace...")
            st.write('<meta http-equiv="refresh" content="0; url=/admin_dashboard" />', unsafe_allow_html=True)

        elif user_role == "user":
            cr.key = 1
            st.success(f"Login successful! Welcome, {name}. Redirecting to your Dashboard...")
            st.write('<meta http-equiv="refresh" content="0; url=/dashboard" />', unsafe_allow_html=True)

        # Add a logout button for the authenticated user
        authenticator.logout("Logout")

    elif auth_status is False:
        st.error("ERROR: Invalid Credentials. Please try again.")

    elif auth_status is None:
        st.warning("Please enter your email and password.")


if __name__ == "__main__":
     # Redirect to the dashboard once logged in
    if cr.key == 1:
        st.write('<meta http-equiv="refresh" content="0; url=/dashboard" />', unsafe_allow_html=True)
    elif cr.key == 2:
        st.write('<meta http-equiv="refresh" content="0; url=/admin_dashboard" />', unsafe_allow_html=True)
    else:
        login()

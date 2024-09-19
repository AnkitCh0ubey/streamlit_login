import streamlit as st
from yaml import SafeLoader
import credentials as cr
import yaml
import streamlit_authenticator as stauth


st.set_page_config(page_title="Login")

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

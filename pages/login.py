import streamlit as st
from yaml import SafeLoader
import credentials as cr
import yaml
import streamlit_authenticator as stauth



# Add custom CSS to center the button
button_css = """
    <style>
    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
"""

# Render the CSS
st.markdown(button_css, unsafe_allow_html=True)


def load_credentials():
    with open('./config.yaml') as file:
      config = yaml.load(file, Loader=SafeLoader)
    return config


def login():

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


    elif auth_status is False:
        st.error("ERROR: Invalid Credentials. Please try again.")

    elif auth_status is None:
        st.warning("Please enter your email and password.")


    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("Sign Up"):
        st.write('<meta http-equiv="refresh" content="0; url=/Signup" />', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



if __name__ == "__main__":
     # Redirect to the dashboard once logged in
    if cr.key == 1:
        st.write('<meta http-equiv="refresh" content="0; url=/dashboard" />', unsafe_allow_html=True)
    elif cr.key == 2:
        st.write('<meta http-equiv="refresh" content="0; url=/admin_dashboard" />', unsafe_allow_html=True)
    else:
        login()

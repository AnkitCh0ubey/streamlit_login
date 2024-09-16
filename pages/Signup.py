import streamlit as st
import yaml
import bcrypt

st.set_page_config(page_title="Sign Up")

def load_credentials():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config['users']


def save_credentials(new_user):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    config['users'].update(new_user)

    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)


def signup():
    st.subheader("Sign Up")
    name = st.text_input("Your Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    try:
        if st.button("Sign Up"):
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'),salt)
            if email and password and name:
                users = load_credentials()
                if email in users:
                    st.error("Username already exists!")
                else:
                    new_user = {
                        email: {
                            'role': 'user',
                            'password': hashed_pw.decode('utf-8')
                        }
                    }
                    save_credentials(new_user)
                    st.success("Registration Successful redirecting to login")
                    st.write('<meta http-equiv="refresh" content="0; url=/login" />', unsafe_allow_html=True)
            else:
                st.error("Please enter all the details")
    except Exception as e:
        st.error(f"Error: An error occured: {e}")
if __name__ == "__main__":
    signup()
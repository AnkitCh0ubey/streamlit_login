import pymysql
import credentials as cr
import streamlit as st
import yaml

connection = pymysql.connect(
    host=cr.host,
    user=cr.user,
    password=cr.password,
    database=cr.database
)

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



def main():
    st.title("Registration form")
    st.switch_page("pages/login.py")


if __name__ == "__main__":
    main()
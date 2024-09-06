import streamlit as st
import pymysql
import credentials as cr

st.set_page_config(page_title="Sign Up")

connection = pymysql.connect(
    host=cr.host,
    user=cr.user,
    password=cr.password,
    database=cr.database
)


def signup():
    st.subheader("Sign Up")
    f_name = st.text_input("Your First Name")
    l_name = st.text_input("Your Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    try:
        cur = connection.cursor()
        if st.button("Sign Up"):

            cur.execute("select * from student_register where email=%s", email)
            row = cur.fetchone()

            if row is not None:
                st.error("Error!", "The email id is already exists, please try again with another email id")
            else:
                if f_name == "" or l_name == "" or email == "" or password == "":
                    st.error("One or more field is empty. Please enter all the details")
                else:
                    sql = "insert into student_register(f_name, l_name, email, password) values(%s,%s,%s,%s)"
                    val = (f_name, l_name, email, password)
                    cur.execute(sql, val)
                    connection.commit()

                    st.success("Registration Successful redirecting to login")
                    st.write('<meta http-equiv="refresh" content="0; url=/login" />', unsafe_allow_html=True)

        cur.close()
    except Exception as e:
        st.error("An unexpected error occured. Please try again")
    finally:
        connection.close()

if __name__ == "__main__":
    signup()
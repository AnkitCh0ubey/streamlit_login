import pymysql
import credentials as cr
import streamlit as st

connection = pymysql.connect(
    host=cr.host,
    user=cr.user,
    password=cr.password,
    database=cr.database
)



def main():
    st.title("Registration form")

    option = st.sidebar.selectbox("Login/Sign Up",("Login", "Sign Up"))

    if option == "Login":
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
                        st.success("Yooo, All set!!!")
            cur.close()
            connection.close()

        except Exception as e:
            st.error("An unexpected error occurred. Please try again.")

    else:
        st.subheader("Sign Up")
        f_name = st.text_input("Your First Name")
        l_name = st.text_input("Your Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        try:
            cur = connection.cursor()

            if st.button("Sign Up"):
                cur.execute("select * from student_register where email=%s",email)
                row = cur.fetchone()
                if row is not None:
                    st.error("Error!","The email id is already exists, please try again with another email id")
                else:
                    if f_name == "" or l_name == "" or email == "" or password == "":
                        st.error("One or more field is empty. Please enter all the details")
                    else:
                        sql = "insert into student_register(f_name, l_name, email, password) values(%s,%s,%s,%s)"
                        val = (f_name, l_name, email, password)
                        cur.execute(sql, val)
                        connection.commit()

                        st.success("Registration Successful")

            cur.close()
        except Exception as e:
            st.error("An unexpected error occured. Please try again")
        finally:
            connection.close()


if __name__ == "__main__":
    main()
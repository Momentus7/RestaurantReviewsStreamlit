import streamlit as st
import mysql.connector
import re

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'your-database-host'),  # Update to your actual host
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'Mpag@88rbtsm'),
            database=os.getenv('DB_NAME', 'reviews_db')
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# User login
def login_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM accounts WHERE username=%s AND password=%s', (username, password))
    account = cursor.fetchone()
    connection.close()
    return account

# User registration
def register_user(username, password, email, cuisine, ambience, cleanliness, food, remarks):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO accounts (username, password, email, cuisine, ambience, cleanliness, food, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                   (username, password, email, cuisine, ambience, cleanliness, food, remarks))
    connection.commit()
    connection.close()

# Update user review
def update_user_review(username, password, email, cuisine, ambience, cleanliness, food, remarks, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE accounts SET username=%s, password=%s, email=%s, cuisine=%s, ambience=%s, cleanliness=%s, food=%s, remarks=%s WHERE id=%s', 
                   (username, password, email, cuisine, ambience, cleanliness, food, remarks, user_id))
    connection.commit()
    connection.close()

# Streamlit app
st.title("SM Restaurant Reviews")

# Sidebar for navigation
menu = ["Login", "Register", "Display", "Update", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        account = login_user(username, password)
        if account:
            st.session_state['loggedin'] = True
            st.session_state['id'] = account['id']
            st.session_state['username'] = account['username']
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password!")

elif choice == "Register":
    st.subheader("Registration Section")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    email = st.text_input("Email")
    cuisine = st.text_input("Cuisine")
    ambience = st.text_input("Ambience")
    cleanliness = st.text_input("Cleanliness")
    food = st.text_input("Food")
    remarks = st.text_area("Remarks")
    if st.button("Register"):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            st.error("Invalid email address!")
        elif not re.match(r'[A-Za-z0-9]+', username):
            st.error("Username must contain only characters and numbers!")
        else:
            register_user(username, password, email, cuisine, ambience, cleanliness, food, remarks)
            st.success("You have successfully given your review!")

elif choice == "Display":
    if 'loggedin' in st.session_state:
        st.subheader("Display Review")
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE id=%s', (st.session_state['id'],))
        account = cursor.fetchone()
        connection.close()
        if account:
            st.write("Username:", account['username'])
            st.write("Email:", account['email'])
            st.write("Cuisine:", account['cuisine'])
            st.write("Ambience:", account['ambience'])
            st.write("Cleanliness:", account['cleanliness'])
            st.write("Food:", account['food'])
            st.write("Remarks:", account['remarks'])
        else:
            st.error("No review found!")
    else:
        st.warning("Please login first")

elif choice == "Update":
    if 'loggedin' in st.session_state:
        st.subheader("Update Review")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        email = st.text_input("Email")
        cuisine = st.text_input("Cuisine")
        ambience = st.text_input("Ambience")
        cleanliness = st.text_input("Cleanliness")
        food = st.text_input("Food")
        remarks = st.text_area("Remarks")
        if st.button("Update"):
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                st.error("Invalid email address!")
            elif not re.match(r'[A-Za-z0-9]+', username):
                st.error("Username must contain only characters and numbers!")
            else:
                update_user_review(username, password, email, cuisine, ambience, cleanliness, food, remarks, st.session_state['id'])
                st.success("You have successfully updated your review!")
    else:
        st.warning("Please login first")

elif choice == "Logout":
    if 'loggedin' in st.session_state:
        st.session_state.pop('loggedin', None)
        st.session_state.pop('id', None)
        st.session_state.pop('username', None)
        st.success("Logged out successfully!")
        st.experimental_rerun()
    else:
        st.warning("You are not logged in")

import streamlit as st
import bcrypt
import mysql.connector

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saquib@123",
        database="court_db"
    )

# ---------- Customer Functions ----------
def register(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_password.decode('utf-8')))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, password FROM customers WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        user_id, name, hashed_password = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return user_id, name
    return None, None

# ---------- Advocate Functions ----------
def add_advocate(name, specialty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO advocates (name, specialty) VALUES (%s, %s)", (name, specialty))
    conn.commit()
    cursor.close()
    conn.close()

def list_advocates():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM advocates")
    advocates = cursor.fetchall()
    cursor.close()
    conn.close()
    return advocates

# ---------- Appointment Booking ----------
def book_appointment(customer_id, advocate_id, appointment_date, appointment_time):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO appointments (customer_id, advocate_id, appointment_date, appointment_time)
            VALUES (%s, %s, %s, %s)
        """, (customer_id, advocate_id, appointment_date, appointment_time))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Booking failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- Streamlit App ----------
st.set_page_config(page_title="Advocate Appointment System", page_icon="⚖️")
st.title("⚖️ Advocate Appointment System")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = ""

menu = ["Register", "Login", "Admin - Add Advocate"]
choice = st.sidebar.selectbox("Menu", menu)

# --------- Register ---------
if choice == "Register":
    st.subheader("Create a New Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register(name, email, password):
            st.success("✅ Registered successfully. You can now log in.")
        else:
            st.error("❌ Email already exists or registration failed.")

# --------- Login ---------
elif choice == "Login":
    if not st.session_state.logged_in:
        st.subheader("Login to Book an Appointment")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user_id, name = login(email, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.user_name = name
                st.success(f"Welcome, {name}!")
            else:
                st.error("Invalid credentials.")

# --------- Advocate Appointment Booking (Post Login) ---------
if st.session_state.logged_in:
    st.subheader(f"Hello, {st.session_state.user_name} 👋")
    st.subheader("📋 Available Advocates")

    advocates = list_advocates()
    if advocates:
        for adv in advocates:
            st.write(f"**{adv[0]}**: Adv. {adv[1]} — {adv[2]}")

        advocate_id = st.number_input("Enter Advocate ID", min_value=1, step=1)
        date = st.date_input("Appointment Date")
        time = st.time_input("Appointment Time")

        if st.button("Book Appointment"):
            if book_appointment(
                st.session_state.user_id,
                advocate_id,
                date.isoformat(),
                time.strftime("%H:%M:%S")
            ):
                st.success("✅ Appointment booked successfully.")
    else:
        st.warning("⚠️ No advocates found.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = ""
        st.success("Logged out.")

# --------- Admin Panel ---------
elif choice == "Admin - Add Advocate":
    st.subheader("Admin Panel: Add Advocate")
    name = st.text_input("Advocate Name")
    specialty = st.text_input("Specialty")
    if st.button("Add Advocate"):
        if name and specialty:
            add_advocate(name, specialty)
            st.success("✅ Advocate added.")
        else:
            st.warning("Please enter both name and specialty.")

import bcrypt
from db import get_connection

def register(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)",
                       (name, email, hashed_password.decode('utf-8')))
        conn.commit()
        print("Registered successfully.")
    except:
        print("Email already exists.")
    finally:
        cursor.close()
        conn.close()


def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch the hashed password for the email
    cursor.execute("SELECT id, name, password FROM customers WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        user_id, name, hashed_password = result
        # Check the entered password against the hashed one
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print(f"Welcome, {name}!")
            return user_id
        else:
            print("Incorrect password.")
            return None
    else:
        print("Email not found.")
        return None

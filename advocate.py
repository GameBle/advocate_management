from db import get_connection

def add_advocate(name, specialty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO advocates (name, specialty) VALUES (%s, %s)", (name, specialty))
    conn.commit()
    print("Advocate added.")
    cursor.close()
    conn.close()

def list_advocates():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM advocates")  # fixed table name
    advocates = cursor.fetchall()
    print("\nAvailable Advocates:")
    for adv in advocates:
        print(f"{adv[0]}. Adv. {adv[1]} - {adv[2]}")
    cursor.close()
    conn.close()

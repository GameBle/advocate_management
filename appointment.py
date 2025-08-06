from db import get_connection

def book_appointment(customer_id, advocate_id, appointment_date, appointment_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (customer_id, advocate_id, appointment_date, appointment_time)
        VALUES (%s, %s, %s, %s)
    """, (customer_id, advocate_id, appointment_date, appointment_time))
    conn.commit()
    print("Appointment booked.")
    cursor.close()
    conn.close()

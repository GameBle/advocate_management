from customer import register, login
from advocate import add_advocate, list_advocates
from appointment import book_appointment

def main():
    print("Welcome to Advocate Appointment System")
    while True:
        print("\n1. Register\n2. Login\n3. Add Advocate (Admin)\n4. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            register(name, email, password)

        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            customer_id = login(email, password)
            if customer_id:
                list_advocates()
                advocate_id = int(input("Enter Advocate ID to book: "))
                date = input("Enter date (YYYY-MM-DD): ")
                time = input("Enter time (HH:MM:SS): ")
                book_appointment(customer_id, advocate_id, date, time)

        elif choice == "3":
            name = input("Advocate name: ")
            specialty = input("Specialty: ")
            add_advocate(name, specialty)

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

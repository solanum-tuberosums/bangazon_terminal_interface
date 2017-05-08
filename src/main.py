from methods import *
import datetime

def run_ordering_system():
    print("*********************************************************")
    print("**  Welcome to Bangazon! Command Line Ordering System  **")
    print("*********************************************************")
    print("1. Create a customer account")
    print("2. Choose active customer")
    print("3. Create a payment option")
    print("4. Add product to shopping cart")
    print("5. Complete an order")
    print("6. See product popularity")
    print("7. Leave Bangazon!")

    menu_command = int(input("Please select the number that corresponds to your menu option\n"))

    if menu_command == 1:
        print("Enter customer name")
        customer_name = input()
        print("Enter street address")
        street_address = input()
        print("Enter city")
        city = input()
        print("Enter state")
        state = input()
        print("Enter postal code")
        postal_code = input()
        print("Enter phone number")
        phone_number = input()
        
        customer_values = list()
        #need to split customer_name into first, middle, last and import Date.now stuff
        customer_values.extend([customer_name, street_address, city, state, postal_code, phone_number, datetime.datetime.now()])
        active_customer_id = save_to_db("Customer", customer_values)
        run_ordering_system()

    if menu_command == 2:
        pass   
    if menu_command == 3:
        pass    
    if menu_command == 4:
        pass    
    if menu_command == 5:
        pass    
    if menu_command == 6:
        pass    
    if menu_command == 7:
        pass



if __name__ == "__main__":
    run_ordering_system()
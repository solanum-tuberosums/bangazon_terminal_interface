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
    global active_customer_id

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

        #need to split customer_name into first, middle, last
        customer_values.extend([customer_name, street_address, city, state, postal_code, phone_number, datetime.datetime.now()])
        active_customer_id = save_to_db("Customer", customer_values)
        print("You added a new customer")
        run_ordering_system()

    if menu_command == 2:
        print("Which customer will be active?")
        customer_list = get_all_from_table("Customer")

        # Print list of all customer
        for counter, customer in enumerate(customer_list):
            print(str(counter+1)+". ", customer[1], customer[2], customer[3])
        chosen_customer_from_menu = int(input())

        # Set Active Customer
        active_customer_id = customer_list[chosen_customer_from_menu-1][0]
        print("Your active customer is", customer_list[chosen_customer_from_menu-1][1], customer_list[chosen_customer_from_menu-1][3])
        run_ordering_system()

    if menu_command == 3:
        pass   
    if menu_command == 4:
        pass    
    if menu_command == 5:
        pass    
    if menu_command == 6:
        pass    
    if menu_command == 7:
        print("See ya Sucka, thanks for visiting Bangazon.")
        pass



if __name__ == "__main__":
    run_ordering_system()
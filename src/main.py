from methods import *
import datetime

active_customer_id = None

def run_ordering_system(menu_command=None):
    global active_customer_id

    if menu_command == None:
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
        if active_customer_id:
            print("Name this payment account")
            account_label = input()
            print("Enter payment type (e.g. AmEx, Visa, Checking)")
            account_type = input()
            print("Enter account number")  
            account_number = input()
            customer_id = active_customer_id
            payment_type_values = list()
            payment_type_values.extend([account_label, account_type, account_number, customer_id])
            save_to_db("PaymentType", payment_type_values)
            print("Your payment type was saved")
            run_ordering_system()
        else: 
            print("Please select an active customer or create a new customer. Press any key to return to main menu")
            input()
            run_ordering_system()

    if menu_command == 4:
        if active_customer_id:
            try:
                order_id = get_active_customer_order(active_customer_id)
            except:
                order_values = [None, datetime.datetime.now(), active_customer_id, None]
                order_id = save_to_db("CustomerOrder", order_vales)
            product_list = get_all_from_table("Product")
            exit_command = (9999,9999,"Done Adding Products")
            product_list.append(exit_command)
            # Print list of all customer
            for counter, product in enumerate(product_list):
                print(str(counter+1)+". ", product[2])
            chosen_product_from_menu = int(input())
            # Check to see if they exited program
            if len(product_list) == chosen_product_from_menu:
                run_ordering_system()
            else:
                product_id = product_list[chosen_product_from_menu-1][0]
                save_to_db("ProductOrder", (order_id, product_id))
                run_ordering_system(menu_command=4)

        else: 
            print("Please select an active customer or create a new customer. Press any key to return to main menu")
            input()
            run_ordering_system()  
    if menu_command == 5:
        pass    
    if menu_command == 6:
        pass    
    if menu_command == 7:
        print("See ya Sucka, thanks for visiting Bangazon.")
        pass



if __name__ == "__main__":
    run_ordering_system()
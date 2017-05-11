"""
--- Description ---
    Main Bangazon Command Line Interface module that contains all of the 
    methods' invocations/calls and the logic for managing the user's 
    interaction with this program.
"""

import datetime
import os.path
from methods import *


active_customer_id = None
total_revenue = int()
total_orders = int()
total_customers = int()

def run_ordering_system(menu_command=None):
    """
    This method is invoked to start and manage the lifecycle of this command 
    line interface.

    ---Arguments---
    menu_command(int/None):     This argument represents the numbered menu 
                                choice made by the user. It is defaulted to 
                                None so that the menu options are immediately
                                printed.

    ---Return Value---
     None

    Author: Blaise Roberts, Jessica Younker
    """

    while menu_command != 7:
        if menu_command is None:
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
            try:
                menu_command = int(input
                    ('''Please select the number that corresponds to your menu 
                        option\n > '''))
                if menu_command <= 0:
                    # This type error will cause the except block below to run
                    raise TypeError
            except:
                print("\n --- MUST ENTER A POSITIVE INTEGER ---\n")
                menu_command = None
        elif menu_command == 1:
            print("Enter customer first name")
            customer_first_name = input(' > ')
            print("Enter customer middle initial")
            customer_middle_name = input(' > ')
            print("Enter customer last name")
            customer_last_name = input(' > ')
            print("Enter street address")
            street_address = input(' > ')
            print("Enter city")
            city = input(' > ')
            print("Enter state")
            state = input(' > ')
            print("Enter postal code")
            postal_code = input(' > ')
            print("Enter phone number")
            phone_number = input(' > ')
            customer_values = list()
            #need to split customer_name into first, middle, last
            customer_values.extend(
                                [customer_first_name, customer_middle_name, 
                                customer_last_name, street_address, city, 
                                state, postal_code, phone_number, 
                                datetime.datetime.now()]
                                )
            active_customer_id = save_to_db("Customer", customer_values)
            print("\n --- NEW CUSTOMER ADDED ---\n")
            menu_command = None
        elif menu_command == 2:
            print("\nWhich customer will be active?")
            customer_list = get_all_from_table("Customer")
            # Print list of all customers
            for counter, customer in enumerate(customer_list):
                print(
                    str(counter+1)+". ", customer[1], customer[2], customer[3]
                    )
            try:
                chosen_customer_from_menu = int(input(' > '))
            except:
                chosen_customer_from_menu = 0
            # Added this because if user entered 0:
            #   the last index of the list would be set as the active customer
            if chosen_customer_from_menu <= 0:
                print('\n --- CUSTOMER DOES NOT EXIST ---\n')
                menu_command = 2
            else:
                # Set Active Customer
                try:
                    active_customer_id = customer_list[
                        chosen_customer_from_menu-1][0]
                    print(
                        "\n *** NEW ACTIVE CUSTOMER: ", 
                            customer_list[chosen_customer_from_menu-1][1], 
                            customer_list[chosen_customer_from_menu-1][3] + 
                            " ***\n"
                        )
                    menu_command = None
                except:
                    print("\n --- CUSTOMER DOES NOT EXIST ---\n")
        elif menu_command == 3:
            if active_customer_id:
                print("Name this payment account")
                account_label = input(' > ')
                if len(account_label) <= 0:
                    print("\n --- PLEASE GIVE YOUR PAYMENT TYPE A NAME ---\n")
                    menu_command = 3
                else:
                    print("Enter payment type (e.g. AmEx, Visa, Checking)")
                    account_type = input(' > ')
                    print("Enter account number")
                    account_number = input(' > ')
                    customer_id = active_customer_id
                    payment_type_values = list()
                    payment_type_values.extend(
                        [account_label, account_type, account_number, 
                        customer_id]
                        )
                    save_to_db("PaymentType", payment_type_values)
                    print("\n *** PAYMENT TYPE SAVED *** \n")
                    menu_command = None
            else:
                input('''Please select an active customer or create a new 
                    customer. Press enter to return to main menu.\n > ''')
                menu_command = None
        elif menu_command == 4:
            # Check active_customer and get/create order
            if active_customer_id:
                try:
                    order_tuple = get_active_customer_order(active_customer_id)
                    order_id = order_tuple[0]
                except IndexError:
                    order_values = [None, datetime.datetime.now(), 
                                    active_customer_id, None]
                    order_id = save_to_db("CustomerOrder", order_values)
                # Print list of all products
                product_list = get_all_from_table("Product")
                exit_command = (9999,9999," *** DONE ADDING PRODUCTS ***")
                product_list.append(exit_command)
                for counter, product in enumerate(product_list):
                    print(str(counter+1)+". ", product[2])
                try:
                    chosen_product_from_menu = int(input(' > '))
                except:
                    chosen_product_from_menu = 0
                if chosen_product_from_menu <= 0:
                    print('\n --- PRODUCT DOES NOT EXIST ---\n')
                else:
                    # Check to see if they exited program
                    if len(product_list) == chosen_product_from_menu:
                        menu_command = None
                    # Add product to order and reopen product menu
                    else:
                        try:
                            product_id = product_list[
                                chosen_product_from_menu-1][0]
                            save_to_db("ProductOrder", (product_id, order_id))
                            print("\n *** PRODUCT ADDED ***\n")
                            menu_command = 4
                        except:
                            print("\n --- PRODUCT DOES NOT EXIST ---\n")
                            # menu_command = None
            else:
                print('''\n --- PLEASE SELECT AN ACTIVE CUSTOMER OR CREATE A 
                    NEW CUSTOMER \n --- Press any key to return to main menu.
                    \n''')
                input()
                menu_command = None
        elif menu_command == 5:
            # Check active_customer and get order
            if active_customer_id:
                try:
                    order_tuple = get_active_customer_order(active_customer_id)
                    order_id = order_tuple[0]
                except IndexError:
                    order_values = [None, datetime.datetime.now(), 
                                    active_customer_id, None]
                    order_id = save_to_db("CustomerOrder", order_values)
                order_total = get_order_total(order_id)
                # Check order total
                if order_total != None:
                    rounded_order_total = round(order_total, 2)
                    print('''Your order total is ${}. Ready to purchase? (Y/N)
                        '''.format(rounded_order_total))
                    response = input(" > ")
                    if response.lower() == "y":
                        # Get payment types for customer
                        payment_type_list = get_all_from_table("PaymentType", 
                                                customer_id=active_customer_id)
                        if len(payment_type_list) > 0:
                            print("Choose a payment option")
                            for counter, payment in enumerate(payment_type_list):
                                print(str(counter+1)+". ", payment[1], 
                                    payment[2])
                            try:
                                chosen_payment_type = int(input(' > '))
                                chosen_payment_type_id = payment_type_list[
                                    chosen_payment_type-1][0]
                                # Update order with chosen payment type id and 
                                # date paid
                                complete_order(order_id, 
                                                chosen_payment_type_id)
                                input('''Your order is complete! Press enter to
                                 return to main menu.\n''')
                                menu_command = None
                            except:
                                print('''\n --- MUST ENTER A SHOWN INTEGER ---
                                    \n''')
                        else:
                            temp_command = input('''Customer has no payment 
                                types. Would you like to create a payment type? 
                                (Y/N)\n > ''')
                            if temp_command.lower() == '''y
                                ''' or temp_command.lower() == 'yes':
                                print('\nCREATING PAYMENT TYPE')
                                menu_command = 3
                            else:
                                menu_command = None
                    elif response.lower() == "n":
                        menu_command = None
                    else:
                        input("Please press Y or N")
                        menu_command = 5
                else:
                    input('''Please add some products to your order first. 
                        Press enter to return to main menu.\n''')
                    menu_command = None
            else:
                input('''Please select an active customer or create a new 
                    customer. Press enter to return to main menu.\n''')
                menu_command = None
        elif menu_command == 6:
            # Get list of tuples for the popular products
            popular_product_list = get_popular_products()
            if len(popular_product_list)>0:
                # Set the max column width
                product_column_total_spaces = 18
                order_column_total_spaces = 11
                customer_column_total_spaces = 11
                revenue_column_total_spaces = 14
                # Set up Table
                print("Product           Orders     Customers  Revenue")
                print('''****************************************************
                    ***''')
                #Loop Through list of tuples to print each row in table
                for product in popular_product_list:
                    #Add columns for use in table totals
                    total_orders += product[1]
                    total_customers += product[2]
                    total_revenue += product[3]
                    # Convert Tuple to list and truncate longer values in 
                    # each column
                    product = list(product)
                    product[3] = round(product[3], 2)
                    if len(str(product[0]))>14:
                        product[0] = str(product[0])[:14]+"..."
                    if len(str(product[1]))>7:
                        product[1] = str(product[1])[:7]+"..."
                    if len(str(product[2]))>7:
                        product[2] = str(product[2])[:7]+"..."
                    if len(str(product[3]))>10:
                        product[3] = str(product[3])[:10]+"..."
                    # Calcualte spaces for each column in each row in table
                    space = " "
                    product_column_spaces = product_column_total_spaces-len(
                        str(product[0]))
                    order_column_spaces = order_column_total_spaces-len(
                        str(product[1]))
                    customer_column_spaces = customer_column_total_spaces-len(
                        str(product[2]))
                    # Print each row in table
                    print(str(product[0])+(space*product_column_spaces)+str(
                        product[1])+(space*order_column_spaces)+str(
                        product[2])+(space*customer_column_spaces)+"$"+str(
                        product[3]))
                print('''****************************************************
                    ***''')
                rounded_total_revenue = round(total_revenue, 2)
                # Truncate values to fit into columns
                if len(str(total_orders))>7:
                    total_orders = str(total_orders)[:7]+"..."
                if len(str(total_customers))>7:
                    total_customers = str(total_customers)[:7]+"..."
                if len(str(total_revenue))>10:
                    total_revenue = str(total_revenue)[:10]+"..."
                # Calculate the number of spaces needed for each column
                total_orders_spaces = order_column_total_spaces-len(str(
                    total_orders))
                total_customers_spaces = customer_column_total_spaces-len(str(
                    total_customers))
                total_revenue_spaces = revenue_column_total_spaces-len(str(
                    total_revenue))
                # Print totals in their perfectly sized columns
                print("Totals:           "+str(total_orders)+(
                    space*total_orders_spaces)+str(total_customers)+(
                    space*total_customers_spaces)+"$"+str(
                    rounded_total_revenue))
                input("Press enter to return to the main menu.\n")
                menu_command = None
            else:
                input('''Nothing has been purchased yet, there's no contest, 
                    broseph.\nPress enter to return to the main menu\n''')
                menu_command = None
        else:
            print('\n --- MUST ENTER A VALID MENU OPTION ---\n')
            menu_command = None
    if menu_command == 7:
        print("Cya, Sucka! Thanks for visiting Bangazon.")
if __name__ == "__main__":
    if os.path.isfile('db.sqlite3'):
        pass
    else:
        build_db()
    run_ordering_system()
from methods import *
import datetime

active_customer_id = None
total_revenue = int()
total_orders = int()
total_customers = int()

def run_ordering_system(menu_command=None):
    global active_customer_id
    global total_orders
    global total_customers
    global total_revenue

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
        print("Enter customer first name")
        customer_first_name = input()
        print("Enter customer middle initial")
        customer_middle_name = input()
        print("Enter customer last name")
        customer_last_name = input()
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
        customer_values.extend([customer_first_name, customer_middle_name, customer_last_name, street_address, city, state, postal_code, phone_number, datetime.datetime.now()])
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
            input("Please select an active customer or create a new customer. Press any key to return to main menu.\n")
            run_ordering_system()

    if menu_command == 4:
        # Check active_customer and get/create order
        if active_customer_id:
            try:
                order_tuple = get_active_customer_order(active_customer_id)
                order_id = order_tuple[0]
            except IndexError:
                order_values = [None, datetime.datetime.now(), active_customer_id, None]
                order_id = save_to_db("CustomerOrder", order_values)
            # Print list of all products
            product_list = get_all_from_table("Product")
            exit_command = (9999,9999,"Done Adding Products")
            product_list.append(exit_command)
            for counter, product in enumerate(product_list):
                print(str(counter+1)+". ", product[2])
            chosen_product_from_menu = int(input())
            # Check to see if they exited program
            if len(product_list) == chosen_product_from_menu:
                run_ordering_system()
            # Add product to order and reopen product menu
            else:
                product_id = product_list[chosen_product_from_menu-1][0]
                save_to_db("ProductOrder", (order_id, product_id))
                run_ordering_system(menu_command=4)
        else: 
            print("Please select an active customer or create a new customer. Press any key to return to main menu")
            input()
            run_ordering_system()  


    if menu_command == 5:
        # Check active_customer and get order
        if active_customer_id:
            try:
                order_tuple = get_active_customer_order(active_customer_id)
                order_id = order_tuple[0]
            except IndexError:
                order_values = [None, datetime.datetime.now(), active_customer_id, None]
                order_id = save_to_db("CustomerOrder", order_values)

            order_total = get_order_total(order_id)
            # Check order total
            if order_total != None:
                print("Your order total is ${}. Ready to purchase?".format(order_total))
                response = input("Y/N\t")
                if response.lower() == "y":
                    # Get payment types for customer
                    payment_type_list = get_all_from_table("PaymentType", customer_id=active_customer_id)
                    if len(payment_type_list) > 0:
                        print("Choose a payment option")
                        for counter, payment in enumerate(payment_type_list):
                            print(str(counter+1)+". ", payment[1], payment[2])
                        chosen_payment_type = int(input())
                        chosen_payment_type_id = payment_type_list[chosen_payment_type-1][0]
                        # Update order with chosen payment type id and date paid
                        complete_order(order_id, chosen_payment_type_id)
                        input("Your order is complete! Press any key to return to main menu.\n")
                        run_ordering_system()
                    else:
                        input("Please create a payment type for the customer")
                        run_ordering_system(menu_command=3)

                elif response.lower() == "n": 
                    run_ordering_system()
                else:
                    input("Please press Y or N")
                    run_ordering_system(menu_command=5)

            else:
                input("Please add some products to your order first. Press any key to return to main menu.\n")
                run_ordering_system()

        else: 
            input("Please select an active customer or create a new customer. Press any key to return to main menu.\n")
            run_ordering_system()

    if menu_command == 6:
        # Get list of tuples for the popular products
        popular_product_list = get_popular_products()

        # Set the max column width
        product_column_total_spaces = 18
        order_column_total_spaces = 11
        customer_column_total_spaces = 11
        revenue_column_total_spaces = 14

        # Set up Table
        print("Product           Orders     Customers  Revenue")
        print("*******************************************************")  

        #Loop Through list of tuples to print each row in table
        for product in popular_product_list:
            #Add columns for use in table totals
            total_orders += product[1]
            total_customers += product[2]
            total_revenue += product[3]
            
            # Convert Tuple to list and truncate longer values in each column
            product = list(product)
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
            product_column_spaces = product_column_total_spaces-len(str(product[0]))
            order_column_spaces = order_column_total_spaces-len(str(product[1]))
            customer_column_spaces = customer_column_total_spaces-len(str(product[2]))

            # Print each row in table
            print(str(product[0])+(space*product_column_spaces)+str(product[1])+(space*order_column_spaces)+str(product[2])+(space*customer_column_spaces)+"$"+str(product[3]))

        print("*******************************************************")

        # Truncate values to fit into columns
        if len(str(total_orders))>7:
            total_orders = str(total_orders)[:7]+"..."
        if len(str(total_customers))>7:
            total_customers = str(total_customers)[:7]+"..."
        if len(str(total_revenue))>10:
            total_revenue = str(total_revenue)[:10]+"..."

        # Calculate the number of spaces needed for each column
        total_orders_spaces = order_column_total_spaces-len(str(total_orders))
        total_customers_spaces = customer_column_total_spaces-len(str(total_customers))
        total_revenue_spaces = revenue_column_total_spaces-len(str(total_revenue))

        # Print totals in their perfectly sized columns
        print("Totals:           "+str(total_orders)+(space*total_orders_spaces)+str(total_customers)+(space*total_customers_spaces)+"$"+str(total_revenue))
        input("Press any key to return to the main menu.\n")
        run_ordering_system()
        
    if menu_command == 7:
        print("See ya Sucka, thanks for visiting Bangazon.")
        pass



if __name__ == "__main__":
    run_ordering_system()
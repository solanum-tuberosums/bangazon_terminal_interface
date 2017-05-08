import unittest
import sys; sys.path.append('../')
import faker
from src.methods import *

class TestDatabaseInteractions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.faker = faker.Faker()

        self.customer_values = [self.faker.first_name(), self.faker.first_name(), self.faker.last_name(),
            self.faker.street_address(), self.faker.city(), self.faker.state(), self.faker.zipcode(),
            self.faker.phone_number(), self.faker.date()]

    def test_save_customer(self):
        customer_id = save_to_db("Customer", self.customer_values)

        # Assert that every property for local customer equals properties of database customer
        self.assertIsNotNone(customer_id)

        # Removes customer data from db
        flush_table("Customer")


    def test_save_product(self):
        customer_id = save_to_db("Customer", self.customer_values)
        product_values = [self.faker.word(), self.faker.text(), self.faker.random_int(), customer_id,
            self.faker.random_int()]

        product_id = save_to_db("Product", product_values)

        # Assert that every property for local product equals properties of database product
        self.assertIsNotNone(product_id)

        # Removes customer and product data from db
        flush_table("Customer")
        flush_table("Product")


    def test_save_payment_type(self):
        # Insert customer and get ID
        customer_id = save_to_db("Customer", self.customer_values)

        # Create payment_type
        payment_type_values = [self.faker.word(), self.faker.credit_card_provider(),
            self.faker.credit_card_number(), customer_id]

        payment_type_id = save_to_db("PaymentType", payment_type_values)

        self.assertIsNotNone(payment_type_id)

        # Removes customer and payment_type data from db
        flush_table("Customer")
        flush_table("PaymentType")


    def test_add_product_to_order(self):
        # Insert customer and get ID
        customer_id = save_to_db("Customer", self.customer_values)

        # Insert order and get ID
        order_values = [None, self.faker.date(), customer_id, None]

        save_to_db("Order", order_values)

        order_id = get_active_customer_order(customer_id)

        # Insert products and get IDs
        first_product_values = [self.faker.word(), self.faker.text(), self.faker.random_int(), customer_id,
            self.faker.random_int()]

        first_product_id = save_to_db("Product", first_product_values)

        second_product_values = [self.faker.word(), self.faker.text(), self.faker.random_int(), customer_id,
            self.faker.random_int()]

        first_product_id = save_to_db("Product", first_product_values)
        second_product_id = save_to_db("Product", second_product_values)

        product_list = get_all_from_table("Product")

        first_chosen_product_from_menu = 1
        second_chosen_product_from_menu = 2
        chosen_product_pk_index = 0

        first_chosen_product_id = product_list[chosen_product_from_menu-1][chosen_product_pk_index]
        second_chosen_product_id = product_list[chosen_product_from_menu-1][chosen_product_pk_index]

        first_productorder_id = save_to_db("ProductOrder", [order_id, first_chosen_product_id])
        second_productorder_id = save_to_db("ProductOrder", [order_id, first_chosen_product_id])
        third_productorder_id = save_to_db("ProductOrder", [order_id, second_chosen_product_id])

        self.assertEqual(first_product_id, first_chosen_product_id)
        self.assertEqual(second_product_id, second_chosen_product_id)
        self.assertIsNotNone(order_id)
        self.assertIsNotNone(first_productorder_id)
        self.assertIsNotNone(second_productorder_id)
        self.assertIsNotNone(third_productorder_id)

        flush_table("Customer")
        flush_table("Product")
        flush_table("PaymentType")
        flush_table("Order")
        flush_table("ProductOrder")


    def test_complete_order(self):
        # Insert customer and get ID
        customer_id = save_to_db("Customer", self.customer_values)

        # Insert payment_type and get ID
        payment_type_values = [self.faker.word(), self.faker.credit_card_provider(),
            self.faker.credit_card_number(), customer_id]

        payment_type_id = save_to_db("PaymentType", payment_type_values)

        # Insert order and get ID
        order_values = [None, self.faker.date(), customer_id, None]

        save_to_db("Order", order_values)

        order_id = get_active_customer_order(customer_id)

        # Insert products and get IDs
        first_product_values = [self.faker.word(), self.faker.text(), self.faker.random_int(), customer_id,
            self.faker.random_int()]

        first_product_id = save_to_db("Product", first_product_values)

        second_product_values = [self.faker.word(), self.faker.text(), self.faker.random_int(), customer_id,
            self.faker.random_int()]

        save_to_db("ProductOrder", [order_id, first_product_id])
        save_to_db("ProductOrder", [order_id, first_product_id])
        save_to_db("ProductOrder", [order_id, second_product_id])

        ####### Important method, to update selected order ######
        order_tuple = complete_order(order_id, payment_type_id)

        # Checking the payment_type_id and the date_paid
        self.assertIsNotNone(order_tuple[1])
        self.assertIsNotNone(order_tuple[4])

        flush_table("Customer")
        flush_table("Product")
        flush_table("PaymentType")
        flush_table("Order")
        flush_table("ProductOrder")


    def test_get_all_from_customer_and_set_active_customer(self):
        # Insert customers
        customer_id = save_to_db("Customer", self.customer_values)
        save_to_db("Customer", self.customer_values)
        save_to_db("Customer", self.customer_values)
        save_to_db("Customer", self.customer_values)
        save_to_db("Customer", self.customer_values)

        # Get the list of all customers and set active customer id
        customer_list = get_all_from_table("Customer")

        chosen_customer_from_menu = 1
        chosen_customer_pk_index = 0

        active_customer_id = customer_list[chosen_customer_from_menu-1][chosen_customer_pk_index]

        # Check that we set the active customer id and
        #   that the customer id we inserted is equal to our active cusotmer id
        self.assertIsNotNone(active_customer_id)
        self.assertEqual(customer_id, active_customer_id)

        flush_table("Customer")
        flush_table("Product")
        flush_table("PaymentType")
        flush_table("Order")
        flush_table("ProductOrder")




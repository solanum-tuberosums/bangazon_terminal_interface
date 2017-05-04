import unittest
import sys; sys.path.append('../')
import faker
from src.Customer import *
from src.PaymentType import *


class TestDatabaseInteractions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
    	# Fakers
        self.faker = faker.Faker()
        # Customer
        customer = Customer()


    def test_save_customer(self):

        customer.id = customer.save()
        # Use self to get id from object that called method
        customer_from_db = customer.get_one()

        # Assert that every property for local customer equals properties of database customer
        self.assertIn(customer.id, customer_from_db)
        self.assertIn(customer.first_name, customer_from_db)
        self.assertIn(customer.middle_name, customer_from_db)
        self.assertIn(customer.last_name, customer_from_db)
        self.assertIn(customer.street_address, customer_from_db)
        self.assertIn(customer.city, customer_from_db.city)
        self.assertIn(customer.state, customer_from_db.state)
        self.assertIn(customer.postal_code, customer_from_db)
        self.assertIn(customer.phone_number, customer_from_db)
        self.assertIn(customer.date_created, customer_from_db)

        # Removes customer data from db
        customer.delete_from_db()


    def test_save_payment_type(self):
    	# Insert customer and get ID
    	customer.id = customer.save()

        # Create payment_type
        payment_type = PaymentType(customer.id)


    	# Assign customer's id to the new payment_type
    	payment_type.customer_id = customer.id

    	# Save the new payment type to db (with customer_id)
    	payment_type.id = payment_type.save()

    	# Returns tuple
    	payment_type_from_db = payment_type.get_one()

    	# PK
    	self.assertIn(payment_type.id, payment_type_from_db)
    	# Rest of properties
    	self.assertIn(payment_type.account_label, payment_type_from_db)
    	self.assertIn(payment_type.account_type, payment_type_from_db)
    	self.assertIn(payment_type.account_number, payment_type_from_db)
    	self.assertIn(payment_type.customer_id, payment_type_from_db)

        # Removes customer and payment_type data from db
    	customer.delete_from_db()
    	payment_type.delete_from_db()

    def test_create_order(self):
        customer.id = customer.save()
        order = Order(customer.id)
        order.id = order.save()
        order_from_db = order.get_one()
        self.assertIn(order.customer_id, order_from_db)
        self.assertIn(order.date, order_from_db)
        self.assertIn(order.payment_type_id, order_from_db)

        customer.delete_from_db()
        order.delete_from_db()

    def get_all_products(self):
        customer.id = customer.save()
        product_type_one_id = 1
        product_type_two_id = 2
        product_one = Product(customer.id, product_type_one_id)
        product_two = Product(customer.id, product_type_two_id)
        product_one.id = product_one.save()
        product_two.id = product_two.save()
       
        product_list = Product.get_all()

        self.assertIn(product_one.id, product_list[0])


    def test_add_product_to_order(self):

        customer.id = customer.save()
        order = Order(customer.id)
        order.id = order.save()
        product_type_id = 1
        product = Product(customer.id, product_type_id)
        product.id = product.save()
        order.add_product_to_order(product.id)
        product_order_from_db = order.get_line_items(order.id) 

        self.assertIn(product.id, product_order_from_db[0])
        self.assertIn(order.id, product_order_from_db[0])

        customer.delete_from_db()
        order.delete_from_db()

        

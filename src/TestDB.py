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

    	# Create payment_type
    	payment_type = PaymentType()

    	# Insert customer and get ID
    	customer.id = customer.save()

    	# Assign customer's id to the new payment_type
    	payment_type.customer_id = customer.id

    	# Save the new payment type to db (with customer_id)
    	payment_type.id = payment_type.save()

    	# Returns tuple
    	payment_type_from_db = payment_type.get_row()

    	# PK
    	self.assertIn(payment_type.id, payment_type_from_db)
    	# Rest of properties
    	self.assertIn(payment_type.account_label, payment_type_from_db)
    	self.assertIn(payment_type.account_type, payment_type_from_db)
    	self.assertIn(payment_type.account_number, payment_type_from_db)
    	self.assertIn(payment_type.customer_id, payment_type_from_db)


    	customer.delete_from_db()
    	payment_type.delete_from_db()

    	

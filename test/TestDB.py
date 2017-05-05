import unittest
import sys; sys.path.append('../')
import faker

class TestDatabaseInteractions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.faker = faker.Faker()

        customer_values = list(faker.first_name(), faker.first_name(), faker.last_name(), 
            faker.street_address(), faker.city(), faker.state(), faker.zipcode(), 
            faker.phone_number(), faker.date())
    

    def test_save_customer(self):
        customer_id = save_to_db("customer", customer_values)

        # Assert that every property for local customer equals properties of database customer
        self.assertIsNotNone(customer_id)

        # Removes customer data from db
        flush_table("customer")


    def test_save_product(self):
        customer_id = save_to_db("customer", customer_values)
        product_values = list(faker.word(), faker.text(), faker.random_int(), customer_id, 
            faker.random_int())

        product_id = save_to_db("product", product_values)

        # Assert that every property for local product equals properties of database product
        self.assertIsNotNone(product_id)

        # Removes customer and product data from db
        flush_table("customer")
        flush_table("product")


    def test_save_payment_type(self):
        # Insert customer and get ID
        customer_id = customer.save_to_db()

        # Create payment_type
        payment_type_values = list(faker.word(), faker.credit_card_provider(), 
            faker.credit_card_number(), customer_id)

        payment_type_id = save_to_db("paymenttype", payment_type_values)

        self.assertIsNotNone(payment_type_id)

        # Removes customer and payment_type data from db
        flush_table("customer")
        flush_table("paymenttype")
        







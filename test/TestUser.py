import unittest

import sys; sys.path.append('../')

class TestUser(unittest.TestCase):

	@classmethod
    def setUpClass(self):
        self.user = User()
        self.user.active_customer = Customer()
        self.user.active_customer.id = 1
        self.user.active_order = Order()
        self.user.active_order.id = 1

    def test_create_customer(self):
    	self.user.active_customer = self.user.create_customer()

    	self.assertIsNotNone(self.user.active_customer.id)

    def test_create_payment_type(self):
    	payment_type = self.user.create_payment_type()

    	self.assertIsNotNone(payment_type.id)
    	self.assertEqual(payment_type.customer_id, self.user.active_customer.id)

    def test_create_order(self):
    	self.user.active_order = self.user.create_order()
    	
    	self.assertIsNotNone(self.user.active_order.id)
    	self.assertEqual(self.user.active_order.customer_id, self.user.active_customer.id)

    def test_get_all_customers(self):
    	customer = self.user.create_customer()
    	secondary_customer = self.user.create_customer()
    	customer_list = self.user.get_all_customers()


    	self.assertIsIn(customer.date_created, customer_list[0])
    	self.assertIsIn(secondary_customer.date_created, customer_list[1])
    	self.assertEqual(len(customer_list), 2)

    def test_get_all_products(self):
    	product_list = self.user.get_all_products()

    	self.assertEqual(len(product_list), 10)





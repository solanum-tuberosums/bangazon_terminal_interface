import unittest
import sys; sys.path.append('../')
import faker

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.faker = faker.Faker()
        faker = self.faker

    def test_save_customer(self):
        customer = Customer()
        customer.first_name = faker.first_name()
        customer.last_name = faker.last_name()
        customer.date_created = faker.date()
        user = User()
        customer = user.save(customer)
        customer_from_db = user.get_customer_from_db(customer)
        self.assertEqual(customer.date_created, customer_from_db.date_created)



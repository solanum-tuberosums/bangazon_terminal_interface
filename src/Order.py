import faker

faker = faker.Faker()

class Order:
    def __init__(self, customer_id):
        self.payment_type_id = None
        self.date_begun = faker.date()
        self.customer_id = customer_id
        self.date_paid = None
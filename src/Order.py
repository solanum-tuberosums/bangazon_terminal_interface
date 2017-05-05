import faker

faker = faker.Faker()

class Order():
    def __init__(self, customer_id):
    self.payment_type_id = None
    self.order_date = faker.date()
    self.customer_id = customer_id
import faker

faker = faker.Faker()

class Product:
    def __init__(self, customer_id):
        self.title = faker.word()
        self.description = faker.text()
        self.product_type = 1
        self.customer_id = customer_id
        self.price = faker.random_int()
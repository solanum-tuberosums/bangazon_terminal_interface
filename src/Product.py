import faker

faker = faker.Faker()

class Product():
    def __init__(self, customer_id):
        self.title = faker.word()
        self.description = faker.text()
        self.product_type = 1
        self.customer_id = customer_id

    def __str__(self):
        return "Title: {}, Description: {}, Product Type: {}, Customer ID: {}".format(self.title, self.description, self.product_type, self.customer_id)

product = Product(1)
print(product)
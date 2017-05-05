import faker

faker = faker.Faker()

class Customer:
    def __init__(self):
        self.first_name = faker.first_name()
        self.middle_name = faker.first_name()
        self.last_name = faker.last_name()
        self.street_address = faker.street_address()
        self.city = faker.city()
        self.state = faker.state()
        self.postal_code = faker.zipcode()
        self.phone_number = faker.phone_number()
        self.date_created = faker.date()
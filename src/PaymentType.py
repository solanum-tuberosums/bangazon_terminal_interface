class PaymentType():
    def __init__(self, customer_id):
        self.account_label = faker.word()
        self.account_type = faker.credit_card_provider()
        self.account_number = faker.credit_card_number()
        self.customer_id = customer_id
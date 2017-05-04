class Order():
    def __init__(self, customer_id):
    self.payment_type_id = None
    self.order_date = factory.Faker('date')
    self.customer_id = customer_id
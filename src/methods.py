"""
bangazon module the contains all the methods for interacting with the sql
database: "db.sqlite3"

---Methods---
get_all_from_table
complete_order
get_active_customer_order
flush_table
save_to_db
get_order_total
get_popular_products
"""

import sqlite3


def get_all_from_table(table_name, customer_id=None):
    """
    This method gets all data from one of three tables in the sql database,
    depending on the table_name passed in as an argument: paymenttype,
    customer, or product.

    ---Arguments---
    table_name(string):     This argument represents the database table from
                            which we pull the data with the SELECT * statement.

    customer_id(integer):   This argument represents the id of the customer
                            whose data we want to pull from the database. It
                            can be null.

    ---Return Value---
    selection(list):        A list of tuples that contains all values from the
                            selected table

    Author: Zak Spence, Blaise Roberts
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        if customer_id:
            sql =   ''' SELECT * FROM paymenttype
                        WHERE paymenttype.customer_id = {}
                    '''.format(str(customer_id))
            selection = [row for row in c.execute(sql)]
            conn.commit()
            return selection
        else:
            ordering = ' '
            if table_name.lower() == 'customer':
                ordering = 'last_name'
            elif table_name.lower() == 'product':
                ordering = 'id'
            elif table_name.lower() == 'producttype':
                ordering = 'id'
            sql =   "SELECT * FROM {} ORDER BY {}".format(table_name, ordering)
            selection = [row for row in c.execute(sql)]

            conn.commit()
            return selection


def complete_order(order_id, pmt_type_id):
    """
    This method changes the state of an order to completed by updating two
    fields in the appropriate row of the CustomerOrder table. It updates the
    payment_type_id to correspond to the payment used by the customer, and it
    updates the date_paid to the current date and time.

    ---Arguments---
    order_id(integer):      The SQL id of the order we wish to change.

    pmt_type_id(integer):   The SQL id of the payment type that the customer
                            used.

    ---Return Value---
    NONE

    Author: Zak Spence
    """
    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql =   ''' UPDATE CustomerOrder
                    SET
                    payment_type_id = {1}, date_paid = datetime('now')
                    WHERE id == {0}
                '''.format(order_id, pmt_type_id)
        c.execute(sql)
        conn.commit()


def get_active_customer_order(customer_id):
    """
    This method returns the most recently created order for a customer.

    ---Arguments---
    customer_id(integer):   This argument represents the id of the customer
                            whose data we want to pull from the database.

    ---Return Value---
    selection[0](tuple):    A tuple that contains all the data for the queried
                            order

    Author: Zak Spence
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql =   ''' SELECT o.id, o.payment_type_id, o.date_begun,
                        o.customer_id, o.date_paid
                    FROM CustomerOrder o
                    INNER JOIN (
                        SELECT customer_id, max(date_begun) as MaxDate
                        FROM CustomerOrder
                        WHERE customer_id == {0}
                     ) mco
                    ON o.customer_id == mco.customer_id
                    AND o.date_begun == mco.MaxDate
                    AND date_paid == 'None'

                '''.format(customer_id)
        selection = [row for row in c.execute(sql)]
        conn.commit()

        if len(selection) == 0:
            return None
        else:
            return selection[0]


def flush_table(table_name):
    """
    This method flushes all data from the table selected in the method
    invocation. It is used only in testing.

    ---Arguments---
    table_name(string):     This represents the name of the table whose data we
                            flush.

    ---Return Value---
    NONE

    Author: Zak Spence
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql =   ''' DELETE FROM {}
                '''.format(table_name)
        c.execute(sql)
        conn.commit()


def save_to_db(table, values):
    """
    This method saves data passed in during the method invocation to a table
    in a database, which is defined during the method invocation.

    ---Arguments---
    table(string):      This represents the name of the table to which we save
                        data.

    values(list):       This list contains the relevant data passed in through
                        the command-line interface via main.py.

    ---Return Value---
    pk(integer):        The primary key of the data inserted into the table

    Author: Jeremy Bakker
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        valuesList = 'NULL'
        for val in values:
            valuesList = valuesList + ', "' + str(val) + '"'
        sql =   ''' INSERT INTO {} VALUES ({})
                '''.format(table, valuesList)
        c.execute(sql)
        conn.commit()
        pk = c.lastrowid
        return pk




def get_order_total(order_id):
    """
    This method returns the total price for a particular order.

    ---Arguments---
    order_id(integer):      This represents the primary key of the order whose
                            prices we sum.

    ---Return Value---
    order_total(integer):   The total price of an order

    Author: Jeremy Bakker, Will Sims
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql =   ''' SELECT SUM(p.price)
                    FROM ProductOrder po
                    LEFT JOIN Product p
                    ON po.product_id = p.id
                    WHERE po.order_id = {}
                '''.format(order_id)
        c.execute(sql)
        conn.commit()
        order_total = c.fetchall()[0][0]    # Get(and convert to float) the
                                            # first index of the first index of
                                            # the tuple returned from the query
        return order_total


def get_popular_products():
    """
    This method will return the data we need to populate our table that
    displays the popular products.

    ---Arguments---
    None

    ---Return Value---
    selection(list):        A list of tuples that contain our data for the
                            popularity table.

    Author: Blaise Roberts, Jessica Younker
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql =   ''' SELECT p.title as Product, COUNT(po.id) as NumTimesOrdered,
                        COUNT(distinct o.customer_id)
                        NumberOfCustomersOrdered, (p.price * COUNT(po.id))
                        as Revenue
                    FROM customerorder o, productorder po, product p
                    WHERE o.id = po.order_id
                    AND p.id = po.product_id
                    AND o.date_paid != 'None'
                    GROUP BY po.product_id
                    ORDER BY NumTimesOrdered desc limit 5
                '''
        c.execute(sql)
        return c.fetchall()


def build_db():
    
    
    """
    This method will build the db.sqlite3 file

    ---Arguments---
    None

    ---Return Value---
    None

    Author: Blaise Roberts, Will Sims
    """

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql_customer =      ''' CREATE TABLE Customer(
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                first_name      VARCHAR(20) NOT NULL,
                                middle_name     VARCHAR(20),
                                last_name       VARCHAR(30) NOT NULL,
                                street_address  VARCHAR(40),
                                city            VARCHAR(20),
                                home_state      CHAR(2),
                                postal_code     CHAR(5),
                                phone_number    VARCHAR(15),
                                date_created    DATE NOT NULL)
                            '''
        sql_payment_type =  ''' CREATE TABLE PaymentType(
                                id              INTEGER NOT NULL PRIMARY KEY
                                                    AUTOINCREMENT,
                                account_label   VARCHAR(20),
                                account_type    VARCHAR(20),
                                account_number  VARCHAR(20) NOT NULL,
                                customer_id     INTEGER NOT NULL,
                                FOREIGN KEY     (customer_id)
                                                REFERENCES Customer(id)
                                                ON DELETE CASCADE)
                            '''
        sql_product_type =  ''' CREATE TABLE ProductType(
                                id              INTEGER NOT NULL PRIMARY KEY
                                                    AUTOINCREMENT,
                                label           VARCHAR(20))
                            '''
        sql_product =       ''' CREATE TABLE Product(
                                id              INTEGER NOT NULL PRIMARY KEY
                                                    AUTOINCREMENT,
                                price           REAL NOT NULL,
                                title           VARCHAR(20) NOT NULL,
                                description     VARCHAR(20),
                                product_type_id INTEGER NOT NULL,
                                customer_id     INTEGER NOT NULL,
                                FOREIGN KEY     (product_type_id)
                                                REFERENCES ProductType(id)
                                                ON DELETE CASCADE,
                                FOREIGN KEY     (customer_id)
                                                REFERENCES Customer(id)
                                                ON DELETE CASCADE)
                            '''
        sql_customer_order ='''CREATE TABLE CustomerOrder(
                                id              INTEGER NOT NULL PRIMARY KEY
                                                    AUTOINCREMENT,
                                payment_type_id INTEGER,
                                date_begun      DATE NOT NULL,
                                customer_id     INTEGER NOT NULL,
                                date_paid       DATE CHECK  (date_begun <=
                                                            date_paid),
                                FOREIGN KEY     (customer_id)
                                                REFERENCES Customer(id)
                                                ON DELETE CASCADE)
                            '''
        sql_product_order = ''' CREATE TABLE ProductOrder(
                                id              INTEGER NOT NULL PRIMARY KEY
                                                    AUTOINCREMENT,
                                product_id      INTEGER NOT NULL,
                                order_id        INTEGER NOT NULL,
                                FOREIGN KEY     (product_id)
                                                REFERENCES Product(id)
                                                ON DELETE CASCADE,
                                FOREIGN KEY     (order_id)
                                                REFERENCES CustomerOrder(id)
                                                ON DELETE CASCADE)
                            '''
        customer_one_sql =  ''' INSERT INTO Customer
                                    VALUES  (NULL, 'Jeremy', 'Will', 'Smith',
                                            '500 Interstate Blvd S.',
                                            'Nashville', 'TN', '37201',
                                            '615-888-5555', '05-09-2017')
                            '''
        customer_two_sql =  ''' INSERT INTO Customer
                                    VALUES(NULL, 'Blaise', 'Zak', 'Williams',
                                            '500 Interstate Blvd S.',
                                            'Nashville', 'TN', '37201',
                                            '615-888-5555', '05-09-2017')
                            '''
        customer_three_sql =''' INSERT INTO Customer
                                    VALUES(NULL, 'Jessica', 'Z.', 'Michaels',
                                            '500 Interstate Blvd S.',
                                            'Nashville', 'TN', '37201',
                                            '615-888-5555', '05-09-2017')
                            '''
        product_type_one_sql =  ''' INSERT INTO ProductType
                                        VALUES(NULL, 'Round Toys')
                                '''
        product_type_two_sql =  ''' INSERT INTO ProductType
                                        VALUES(NULL, 'Angular Toys')
                                '''
        product_one_sql =   '''     INSERT INTO Product
                                        VALUES (NULL, 19.99, "Red Ball",
                                            "Bouncy", 1, 1)
                            '''
        product_two_sql =   '''     INSERT INTO Product
                                       VALUES (NULL, 29.99, "Ford Truck",
                                            "F-150", 1, 2);
                            '''
        product_three_sql = '''     INSERT INTO Product
                                        VALUES (NULL, 9.99, "AA Batteries",
                                            "Fully-Charged", 1, 3);
                            '''
        product_four_sql =  '''     INSERT INTO Product
                                        VALUES (NULL, 5.99, "Green Ball",
                                            "Squishy", 1, 1);
                            '''
        product_five_sql =  '''     INSERT INTO Product
                                        VALUES (NULL, 2.99, "White Out",
                                            "Fix Mistakes", 1, 2);
                            '''
        product_six_sql =   '''     INSERT INTO Product
                                        VALUES (NULL, 999.99, "Diamonds",
                                            "Girl's Best Friend", 1, 3);
                            '''
        product_seven_sql = '''     INSERT INTO Product
                                        VALUES (NULL, 39.99, "USB Drive",
                                            "1TB", 1, 1);
                            '''
        product_eight_sql = '''     INSERT INTO Product
                                        VALUES (NULL, 7.99, "Blocks",
                                            "Hard", 2, 1);
                            '''
        product_nine_sql =  '''     INSERT INTO Product
                                        VALUES (NULL, 15.99, "Water Bottle",
                                            "Aluminum", 2, 2);
                            '''
        product_ten_sql =   '''     INSERT INTO Product
                                        VALUES (NULL, 32.99, "Power Strip",
                                            "Surge Protector", 2, 3);
                            '''
        try:
            c.execute(sql_customer)
            c.execute(sql_payment_type)
            c.execute(sql_product_type)
            c.execute(sql_product)
            c.execute(sql_customer_order)
            c.execute(sql_product_order)
            c.execute(customer_one_sql)
            c.execute(customer_two_sql)
            c.execute(customer_three_sql)
            c.execute(product_type_one_sql)
            c.execute(product_type_two_sql)
            c.execute(product_one_sql)
            c.execute(product_two_sql)
            c.execute(product_three_sql)
            c.execute(product_four_sql)
            c.execute(product_five_sql)
            c.execute(product_six_sql)
            c.execute(product_seven_sql)
            c.execute(product_eight_sql)
            c.execute(product_nine_sql)
            c.execute(product_ten_sql)
            conn.commit()
        except sqlite3.OperationalError:
            pass



def get_active_customer_order_details(table_name, order_id=None):

    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        if order_id:
            sql =   ''' SELECT * FROM productorder po, product p
                        WHERE po.product_id = p.id
                        AND po.order_id = {}
                    '''.format(str(order_id))
            selection = [row for row in c.execute(sql)]
            conn.commit()
            return selection
        else:
            ordering = ' '
            if table_name.lower() == 'customer':
                ordering = 'last_name'
            elif table_name.lower() == 'product':
                ordering = 'id'
            elif table_name.lower() == 'producttype':
                ordering = 'id'
            sql =   "SELECT * FROM {} ORDER BY {}".format(table_name, ordering)
            selection = [row for row in c.execute(sql)]

            conn.commit()
            return selection


def complete_order(order_id, pmt_type_id):
    """
    This method changes the state of an order to completed by updating two
    fields in the appropriate row of the CustomerOrder table. It updates the
    payment_type_id to correspond to the payment used by the customer, and it
    updates the date_paid to the current date and time.

    ---Arguments---
    order_id(integer):      The SQL id of the order we wish to change.

    pmt_type_id(integer):   The SQL id of the payment type that the customer
                            used.

    ---Return Value---
    NONE

    Author: Zak Spence
    """
    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql =   ''' UPDATE CustomerOrder
                    SET
                    payment_type_id = {1}, date_paid = datetime('now')
                    WHERE id == {0}
                '''.format(order_id, pmt_type_id)
        c.execute(sql)
        conn.commit()
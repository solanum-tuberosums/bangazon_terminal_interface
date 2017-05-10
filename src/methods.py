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
    depending on the table_name passed in as an argument: paymenttype, customer,
    or product.

    ---Arguments---
    table_name(string):     This argument represents the database table from 
                            which we pull the data with the SELECT * statement.

    customer_id(integer):    This argument represents the id of the customer 
                            whose data we want to pull from the database. It can
                            be null.

    ---Return Value---
    selection(list):        A list of tuples that contains all values from the 
                            selected table 

    Author: Zak Spence, Blaise Roberts
    """

    db = 'db.sqlite3'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if customer_id:
        sql =   ''' SELECT * FROM paymenttype 
                    WHERE paymenttype.customer_id = {}
                '''.format(str(customer_id))
        selection = [row for row in c.execute(sql)]
        conn.commit()
        conn.close()
        return selection
    else:
        ordering = ' '
        if table_name.lower() == 'customer':
            ordering = 'last_name'
        elif table_name.lower() == 'product':
            ordering = 'id'
        sql =   ''' SELECT * FROM {} ORDER BY {}
                '''.format(table_name, ordering)
        selection = [row for row in c.execute(sql)]
        conn.commit()
        conn.close()
        return selection


def complete_order(order_id, pmt_type_id):
    return (1, 3, '2016-01-21', 5, '2017-01-01')


def get_active_customer_order(customer_id):
    """
    This method returns the most recently created order for a customer. 

    ---Arguments---
    customer_id(integer):    This argument represents the id of the customer 
                            whose data we want to pull from the database.

    ---Return Value---
    selection[0](tuple):    A tuple that contains all the data for the queried
                            order

    Author: Zak Spence
    """

    db='db.sqlite3'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql =   ''' SELECT o.id, o.customer_id, o.date_begun, o.date_paid
                FROM CustomerOrder o
                INNER JOIN (
                    SELECT customer_id, max(date_begun) as MaxDate
                    FROM CustomerOrder
                    WHERE customer_id == {0}
                 ) mco
                ON o.customer_id == mco.customer_id
                AND o.date_begun == mco.MaxDate
            '''.format(customer_id)
    selection = [row for row in c.execute(sql)]
    conn.commit()
    conn.close()
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

    db='db.sqlite3'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql =   ''' DELETE FROM {}
            '''.format(table_name)
    c.execute(sql)
    conn.commit()
    conn.close()


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

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    valuesList = 'NULL'
    for val in values:
        valuesList = valuesList + ', "' + str(val) + '"'
    sql =   ''' INSERT INTO {} VALUES ({})
            '''.format(table, valuesList)
    c.execute(sql)
    conn.commit()
    pk = c.lastrowid
    c.close()
    return pk


def get_order_total(order_id):
    """
    This method returns the total price for a particular order.

    ---Arguments---
    order_id(integer):  This represents the primary key of the order whose 
                        prices we sum.

    ---Return Value---
    order_total(integer):   The total price of an order

    Author: Jeremy Bakker, Will Sims
    """
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sql =   ''' SELECT SUM(p.price) 
                FROM ProductOrder po 
                LEFT JOIN Product p 
                ON po.product_id = p.id 
                WHERE po.order_id = {}
            '''.format(order_id)
    c.execute(sql)
    conn.commit()
    order_total = c.fetchall()[0][0]    # Get(and convert to float) the first 
                                        # index of the first index of the tuple 
                                        # returned from the query
    c.close()
    return order_total


def get_popular_products():
    return [('AA Batteries', 100, 20, 990.90),('Diapers', 50, 10, 640.95), ('Case Crackling Cola', 40, 30, 270.96)]


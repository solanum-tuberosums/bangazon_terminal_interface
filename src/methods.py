import sqlite3


def get_all_from_table(table_name, customer_id=None):
    db = 'db.sqlite3'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if customer_id:
        command = 'SELECT * FROM paymenttype where paymenttype.customer_id = {}'.format(str(customer_id))
        selection = [row for row in c.execute(command)]
        conn.commit()
        conn.close()
        return selection
    else:
        ordering = ' '
        if table_name.lower() == 'customer':
            ordering = 'last_name'
        elif table_name.lower() == 'product':
            ordering = 'id'
        command = 'SELECT * FROM {} ORDER BY {}'.format(table_name, ordering)
        selection = [row for row in c.execute(command)]
        conn.commit()
        conn.close()
        return selection


def complete_order(order_id=None, pmt_type_id=None, db='db.sqlite3'):

    with sqlite3.connect(db) as conn:
        c = conn.cursor()

        update_order = '''
                     UPDATE CustomerOrder
                     SET payment_type_id = {1}, date_paid = GETDATE()
                     WHERE order_id == {0}
                  '''.format(order_id, pmt_type_id)
        c.execute(update_order)
        conn.commit()

def get_active_customer_order(customer_id):
    db='db.sqlite3'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    command = '''SELECT o.id, o.customer_id, o.date_begun, o.date_paid
                 FROM CustomerOrder o
                 INNER JOIN (
                    SELECT customer_id, max(date_begun) as MaxDate
                    FROM CustomerOrder
                    WHERE customer_id == {0}
                 ) mco
                 ON o.customer_id == mco.customer_id
                 AND o.date_begun == mco.MaxDate
                 '''.format(customer_id)
    selection = [row for row in c.execute(command)]
    conn.commit()
    conn.close()
    return selection[0]

def flush_table(table_name=None, db='db.sqlite3'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    command = "DELETE FROM {}".format(table_name)
    c.execute(command)
    conn.commit()
    conn.close()

def save_to_db(table, values):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    valuesList = 'NULL'
    for val in values:
        valuesList = valuesList + ', "' + str(val) + '"'
    sql = 'INSERT INTO {} VALUES ({})'.format(table, valuesList)
    c.execute(sql)
    conn.commit()
    pk = c.lastrowid
    c.close()
    return pk

def get_order_total(order_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    sql = "SELECT SUM(p.price) FROM ProductOrder po LEFT JOIN Product p ON po.product_id = p.id WHERE po.order_id = {}".format(order_id)
    c.execute(sql)
    conn.commit()

    # Get (and convert to float) the first index of the first index of the tuple returned from the query
    order_total = c.fetchall()[0][0]

    c.close()
    return order_total

def get_popular_products():
    return [('AA Batteries', 100, 20, 990.90),('Diapers', 50, 10, 640.95), ('Case Crackling Cola', 40, 30, 270.96)]


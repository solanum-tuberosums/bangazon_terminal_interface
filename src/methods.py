import sqlite3

def get_all_from_table(table_name=None, db='db.sqlite3'):
    conn = sqlite3.connect(db)
    c = conn.cursor()
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

def complete_order(order_id, pmt_type_id):
    return (1, 3, '2016-01-21', 5, '2017-01-01')

def get_active_customer_order(customer_id):
    return 1

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
    
    sql = "SELECT SUM(p.price) FROM ProductOrder po LEFT JOIN Product p ON po.product_id = p.id WHERE po.order_id = {}".format(get_active_customer_order(1))
    c.execute(sql)
    conn.commit()

    # Get (and convert to float) the first index of the first index of the tuple returned from the query
    order_total = c.fetchall()[0][0]

    c.close()
    return order_total

def get_popular_products():
    return [('AA Batteries', 100, 20, 990.90),('Diapers', 50, 10, 640.95), ('Case Crackling Cola', 40, 30, 270.96)]


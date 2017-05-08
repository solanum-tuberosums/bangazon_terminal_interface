import sqlite3

def get_all_from_table(table_name):
    return [(1, 1),(2,'j','b'), (3, 2)]

def complete_order(order_id, pmt_type_id):
    return (1, 3,'2016-01-21', 5, '2017-01-01')
    
def get_active_customer_order(customer_id):
    return 1

def flush_table(table_name):
    pass

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




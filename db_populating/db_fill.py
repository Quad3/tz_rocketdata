import sqlite3
from string import ascii_uppercase
from random import choice, randint, random
import datetime
import pathlib

CUR_DIR = pathlib.Path(__file__).parent.resolve()

DEBUG = False
NAMES = CUR_DIR / 'names.txt'
ADDRESSES = CUR_DIR / 'addresses.txt'
EMAILS = CUR_DIR / 'emails.txt'
PRODUCTS = CUR_DIR / 'raw_products.txt'
PRODUCERS = CUR_DIR / 'producers.txt'

# cur.executemany should be better
def db_exec(conn, inserts, to):
    cur = conn.cursor()
    print(f'### EXECUTE INSERT to {to} ###')
    for i in inserts:
        if DEBUG:
            print(i)
        cur.execute(i)
    conn.commit()

    print(f'### {len(inserts)} INSERTIONS to {to} COMPLETE ###')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    
    return conn

def insert_employees(producer_count):
    inserts = []
    with open(NAMES, 'r') as names:
        for fullname in names:
            inserts.append(f'INSERT INTO api_employee (first_name, last_name, producer_id) VALUES ({fullname[:-1]}, {randint(1, producer_count)});')
    
    return inserts

def insert_products():
    inserts = []
    with open(PRODUCTS, 'r') as products:
        for product in products:
            model = generate_model()
            release_date = generate_random_date(days=600)
            inserts.append(f'INSERT INTO api_product (name, model, release_date) VALUES ("{product[:-1]}", "{model}", "{release_date}");')

    return inserts

def insert_producers():
    inserts = []
    with open(PRODUCERS, 'r') as producers, open(ADDRESSES, 'r') as addresses, open(EMAILS, 'r') as emails:
        global_level = 0
        max_provider_id = 0
        producer_level_mapping = {}
        created_at = str(datetime.date.today())
        i = 0
        for producer, address, email in zip(producers, addresses, emails):
            if producer[0] == '#':
                global_level += 1
                max_provider_id = i
                continue
            debt = 0
            provider_id = 'NULL'
            level = global_level
            if global_level > 0:
                debt = randint(5000, 15000) + round(random(), 2)
                provider_id = randint(1, max_provider_id)
                level = producer_level_mapping[provider_id] + 1

            producer_level_mapping[i + 1] = level
            inserts.append(f'INSERT INTO api_address (country, city, street, house_number) VALUES {address[:-1]};')
            inserts.append(f'INSERT INTO api_contact (email, address_id) VALUES ({email[:-1]}, {i + 1});')
            inserts.append('INSERT INTO api_producer (name, level, debt, created_at, contact_id, provider_id) VALUES'\
                f'("{producer[:-1]}", {level}, {debt}, "{created_at}", {i + 1}, {provider_id});')
            i += 1

    return inserts

def insert_producer_product(producer_count, product_count):
    inserts = []
    for i in range(product_count):
        inserts.append('INSERT INTO api_producer_products (producer_id, product_id) VALUES'\
            f'({randint(1, producer_count)}, {i + 1});')

    return inserts

def generate_model():
    model = ''
    for i in range(randint(3, 4)):
        model += choice(ascii_uppercase)
    
    return model

def generate_random_date(days):
    """From today back to n days"""
    return str(datetime.date.today() - datetime.timedelta(days=days) * random())

def count_table(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT() FROM {table_name}")
    return cur.fetchone()[0]

def main():
    database = 'db.sqlite3'
    conn = create_connection(database)
    with conn:
        db_exec(conn, insert_products(), 'products')
        db_exec(conn, insert_producers(), 'producers, addr, contact')
        # db_exec(conn, insert_employees(count_table(conn, 'api_producer')), 'employees') # last
        db_exec(conn, insert_producer_product(
            count_table(conn, 'api_producer'),
            count_table(conn, 'api_product')), 'producer-product table')

if __name__ == '__main__':
    main()

import random
import logging
from faker import Faker


fake = Faker()


def populate_source_data(cursor, num_records=100):
    """

    :return:
    """
    records_to_insert = []
    for _ in range(num_records):
        action_figure_name = fake.random_element(
            elements=("Luke Skywalker", "Darth Vader", "Obi-Wan Kenobi", "Yoda", "Leia Organa"))
        quantity = random.randint(1, 10)
        price = round(random.uniform(5.0, 30.0), 2)
        date_of_purchase = fake.date_between(start_date='-2y', end_date='today')
        email = fake.email()
        sales_rep = fake.email(domain="swafco.com")
        promo_code = fake.random_element(elements=("radio", "tv", "online", "store"))

        # Append each record as a tuple
        records_to_insert.append((action_figure_name, quantity, price, date_of_purchase, email, sales_rep, promo_code))

    try:
        cursor.executemany('''
        INSERT INTO source (action_figure_name, quantity, price, date_of_purchase, email, sales_rep, promo_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', records_to_insert)
        logging.info(f"Successfully inserted {num_records} records into the database.")
    except Exception as e:
        logging.error(f"Failed to insert records: {e}")
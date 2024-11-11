import logging
import asyncio
import os

import psycopg2
import pandas as pd
from psycopg2.extras import execute_batch

from .swapi_client import fetch_swapi_character_data, add_film_details, add_homeworld_names
from .generate_source_data import populate_source_data


async def transform_data(source_df, swapi_data):
    """
    Transform source data by enriching it with SWAPI data and compute aggregates.

    :param source_df:
    :param swapi_data:
    :return:
    """
    try:
        characters = [
            {'name': person['name'], 'films': person['films'], 'homeworld': person['homeworld']}
            for person in swapi_data if 'films' in person and 'homeworld' in person
        ]

        character_names = [char['name'] for char in characters]
        source_df = source_df[source_df['action_figure_name'].isin(character_names)]
        source_df['revenue'] = source_df['quantity'] * source_df['price']

        character_df = pd.DataFrame(characters)
        character_df, _ = await asyncio.gather(
            add_homeworld_names(character_df),
            add_film_details(character_df)
        )

        merged_df = pd.merge(source_df, character_df, left_on='action_figure_name', right_on='name')
        merged_df['date_of_purchase'] = pd.to_datetime(merged_df['date_of_purchase'], errors='coerce')

        # Create summary table
        summary_df = merged_df.groupby('action_figure_name').agg(
            total_quantity_sold=('quantity', 'sum'),
            total_revenue_generated=('price', lambda x: (x * merged_df['quantity']).sum()),
            last_date_of_purchase=('date_of_purchase', 'max'),
            most_sold_year=('date_of_purchase', lambda x: x.dt.year.mode().max()),
            total_purchase_orders=('quantity', 'count'),
            number_of_films=('films', lambda x: len(x.iloc[0])),
            earliest_debut_date=('film_dates', lambda x: min(x.iloc[0])),
            last_appearance_date=('film_dates', lambda x: max(x.iloc[0])),
            homeworld=('homeworld_name', 'first')
        ).reset_index()

        return summary_df

    except Exception as e:
        logging.error(f"An error occurred during data transformation: {e}")
        return pd.DataFrame()


async def load_data_to_dw(merged_data):
    """

    :param merged_data:
    :return:
    """
    try:
        with psycopg2.connect('postgres://user:password@localhost:5433/dw') as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO action_figures_summary (
                    action_figure_name, total_quantity_sold, total_revenue_generated,
                    last_date_of_purchase, most_sold_year, total_purchase_orders,
                    number_of_films, earliest_debut_date, last_appearance_date, homeworld
                ) VALUES (
                    %(action_figure_name)s, %(total_quantity_sold)s, %(total_revenue_generated)s,
                    %(last_date_of_purchase)s, %(most_sold_year)s, %(total_purchase_orders)s,
                    %(number_of_films)s, %(earliest_debut_date)s, %(last_appearance_date)s, %(homeworld)s
                )
                """
                execute_batch(cursor, query, merged_data.to_dict('records'))
            conn.commit()
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logging.info("Data loading complete.")


async def extract_source_data():
    """

    :return:
    """
    try:
        with psycopg2.connect('postgres://user:password@localhost:5432/source') as conn:
            with conn.cursor() as cursor:
                populate_source_data(cursor)
                cursor.execute("SELECT action_figure_name, quantity, price, date_of_purchase FROM source")
                source_data = cursor.fetchall()
                source_column_headers = [desc[0] for desc in cursor.description]
                source_df = pd.DataFrame(source_data, columns=source_column_headers)
        return source_df
    except Exception as e:
        logging.error(f"Error: {e}")
        return pd.DataFrame()


async def run_etl():
    """

    :return:
    """
    logging.info("Starting ETL process")
    try:
        source_df = await extract_source_data()
        logging.info("Data extraction complete")

        swapi_data = await fetch_swapi_character_data()
        logging.info("Data fetching from SWAPI complete")

        merged_data = await transform_data(source_df, swapi_data)
        logging.info("Data transformation complete")

        await load_data_to_dw(merged_data)
        logging.info("Data loading into DW complete")

    except Exception as e:
        logging.error(f"ETL process failed: {e}")

    finally:
        logging.info("ETL process finished")

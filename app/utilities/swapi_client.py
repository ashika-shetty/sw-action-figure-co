import requests
import asyncio
import httpx
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)

TIMEOUT = httpx.Timeout(10.0, read=None)


async def fetch_swapi_character_data():
    """
    Fetch all character data from the SWAPI.

    :return: List of character data dictionaries.
    """
    url = "https://swapi.dev/api/people/"
    swapi_character_data = []
    while url:
        response = requests.get(url)
        data = response.json()
        swapi_character_data.extend(data['results'])
        url = data['next']  # Get the next page URL
    return swapi_character_data


async def get_film_details_async(film_urls: list) -> list:
    """
    Fetch film details asynchronously from given URLs.

    :param film_urls: List of URLs to fetch film details from.
    :return: List of film release dates.
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        responses = await asyncio.gather(*(client.get(url) for url in film_urls))
        film_dates = []
        for response in responses:
            if response.status_code == 200:
                try:
                    film_data = response.json()
                    film_dates.append(film_data['release_date'])
                except ValueError:
                    print(f"Failed to decode JSON from response: {response.text}")
            else:
                print(f"Request failed with status {response.status_code}: {response.text}")
        return film_dates


async def add_film_details(character_df):
    """
    Add film details to character DataFrame.

    :param character_df: DataFrame containing character data with a 'films' column.
    :return: DataFrame with added film dates.
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        character_df['film_dates'] = await asyncio.gather(
            *(get_film_details_async(films) for films in character_df['films'])
        )
    return character_df


async def get_homeworld_name(homeworld_url: str, client) -> str:
    """
    Fetch homeworld name from the URL.

    :param homeworld_url: URL to fetch homeworld name from.
    :param client: httpx.AsyncClient instance.
    :return: Homeworld name or None if an error occurs.
    """
    response = await client.get(homeworld_url)
    if response.status_code == 200:
        try:
            return response.json()['name']
        except ValueError:
            print(f"Failed to decode JSON from response: {response.text}")
    else:
        print(f"Request failed with status {response.status_code}: {response.text}")
    return None


async def add_homeworld_names(character_df):
    """
    Add homeworld names to character DataFrame.

    :param character_df: DataFrame to enhance with homeworld names.
    :return: Enhanced DataFrame.
    """
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        character_df['homeworld_name'] = await asyncio.gather(
            *(get_homeworld_name(url, client) for url in character_df['homeworld'])
        )
    return character_df
import sqlite3
from math import radians, cos, sin, asin, sqrt


def distance(lat1, lat2, lon1, lon2):
    """
    Calculate the straight-line distance between two coordinates using the Haversine formula.

    Args:
    - lat1, lat2: Latitude of the first and second points in degrees.
    - lon1, lon2: Longitude of the first and second points in degrees.

    Returns:
    The distance between the two points in kilometers.
    """
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def create_table():
    """
    Create the SQLite database table for storing city coordinates if it doesn't exist.
    """
    conn = sqlite3.connect('city_coordinates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cities
                 (city TEXT PRIMARY KEY, latitude REAL, longitude REAL)''')
    conn.commit()
    conn.close()


def get_city_coordinates(city):
    """
    Retrieve the coordinates of a city from the database.

    Args:
    - city: The name of the city.

    Returns:
    A tuple containing the latitude and longitude of the city, or None if the city is not found.
    """
    conn = sqlite3.connect('city_coordinates.db')
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM cities WHERE city=?", (city,))
    row = c.fetchone()
    conn.close()
    return row


def add_city_coordinates(city, latitude, longitude):
    """
    Add new city coordinates to the database.

    Args:
    - city: The name of the city.
    - latitude: The latitude of the city in degrees.
    - longitude: The longitude of the city in degrees.
    """
    conn = sqlite3.connect('city_coordinates.db')
    c = conn.cursor()
    c.execute("INSERT INTO cities (city, latitude, longitude) VALUES (?, ?, ?)", (city, latitude, longitude))
    conn.commit()
    conn.close()


def calculate_distance():
    """
    Calculate the straight-line distance between two cities based on user input.
    """
    create_table()
    city1 = input("Enter the first city: ")
    city2 = input("Enter the second city: ")

    city1_coords = get_city_coordinates(city1)
    if not city1_coords:
        latitude1 = float(input(f"Enter latitude for {city1}: "))
        longitude1 = float(input(f"Enter longitude for {city1}: "))
        add_city_coordinates(city1, latitude1, longitude1)
        city1_coords = (latitude1, longitude1)
    else:
        latitude1, longitude1 = city1_coords

    city2_coords = get_city_coordinates(city2)
    if not city2_coords:
        latitude2 = float(input(f"Enter latitude for {city2}: "))
        longitude2 = float(input(f"Enter longitude for {city2}: "))
        add_city_coordinates(city2, latitude2, longitude2)
        city2_coords = (latitude2, longitude2)
    else:
        latitude2, longitude2 = city2_coords

    dist = distance(latitude1, latitude2, longitude1, longitude2)
    print(f"The straight-line distance between {city1} and {city2} is {dist:.2f} kilometers.")


if __name__ == "__main__":
    calculate_distance()
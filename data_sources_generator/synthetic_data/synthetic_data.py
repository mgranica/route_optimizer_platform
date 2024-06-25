from faker import Faker
from typing import Dict
import random
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
from geopy.geocoders import Nominatim
import argparse
import os
import uuid


ROOT_PATH = os.path.dirname(__file__)
STATIC_DATA = "static_data"
POPULATION = "city_population.json"
RESULTS = "results"
CLIENT = "client_data.json"
ADDRESS = "address_data.json"
SHAPE_FILE = "Distritos.shp"


class GeneratorMixIn:
    
    @staticmethod
    def generate_id() -> str:
        """
        Generate a unique ID.

        :return: A unique ID string prefixed with 'cus-'.
        """
        return f"cus-{str(uuid.uuid4())}"
    
    def save_dict(self, filepath: str, data: Dict) -> None:
        """
        Save a dictionary to a JSON file specified by the output path.

        :param filename: Path to the output file where the dictionary will be saved.
        :param data: The dictionary to save.
        :raises IOError: If there is an error saving the file.
        """
        try:
            with open(filepath, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Dictionary saved to {filepath}")
        except IOError as e:
            print(f"Error occurred while saving dictionary: {e}")

    

class ClientDataGenerator(GeneratorMixIn):
    def __init__(self,):
        self.fake = Faker('es_ES')
    
    def generate_status(self):
        return random.choices(["active", "unactive", "suspended"], weights=[0.85, 0.1, 0.05])[0]
    
    def generate_email(self, first_name, last_name):
        # Helper function to clean names
        def clean_name(name):
            return name.replace(' ', '.').lower()
        providers = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com']
        provider = random.choice(providers)
        email = f"{clean_name(first_name)}.{clean_name(last_name)}@{provider}"
        return email
    
    def generate_gender(self):
        return self.fake.random_element(['Male', 'Female'])
    
    def generate_first_name(self, gender):
        if gender == "Male":
            return self.fake.first_name_male()
        elif gender == "Female":
            return self.fake.first_name_female()

    def generate_client_data(self, filename, num_clients):
        client_list = []
        for _ in range(num_clients):
            # neighborhood = self.generate_neighborhood()
            gender = self.generate_gender()
            first_name = self.generate_first_name(gender)
            last_name = self.fake.last_name()
            email = self.generate_email(first_name, last_name)
            status = self.generate_status()

            client = {
                'client_id': self.generate_id(),
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone_number': self.fake.phone_number(),
                'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
                'gender': gender,
                'occupation': self.fake.job(),
                'created_at': self.fake.date_this_decade(before_today=True, after_today=False).strftime("%Y-%m-%d"),
                'updated_at': self.fake.date_time_between(start_date='-1y', end_date='now').strftime("%Y-%m-%d"),
                'status': status, 
            }
            client_list.append(client)
        self.save_dict(filename, client_list)
        return client_list


class AddressDataGenerator(GeneratorMixIn):
    def __init__(self, clients, shapefile, city_population, city) -> None:
        self.client = clients
        self.num_addresses = 3
        self.df_district = self.load_shape_data(shapefile)
        self.city_data = self.load_static_data(city_population, city)
        self.client_id_list = self.generate_client_id_list()
        self.geolocator = Nominatim(user_agent="geo_reverse")
    
    def load_shape_data(self, shapefile, target_crs = "EPSG:4326"):
        df = gpd.read_file(shapefile).set_index("NOMBRE")
        return df.to_crs(target_crs)
    
    def load_static_data(self, filename, city):
        with open(filename, 'r') as file:
            city_population = json.load(file)
        return self.weight_population(city_population[city])
    
    def weight_population(self, city_data):
        total_population = sum(city_data["population"].values())
        city_data["population"] = {
            key:value/total_population for key, value in city_data["population"].items()
        }
        return city_data
        
    def generate_neighborhood(self):
        neighborhood_data = self.city_data.get("population", {})
        # Sample a neighborhood based on the probability distribution
        neighborhood = random.choices(list(neighborhood_data.keys()), weights=list(neighborhood_data.values()))[0]
        return neighborhood
    
    def generate_client_id_list(self):
        return [
            id 
            for client in self.client 
            for id in [client['client_id']] * (np.random.randint(self.num_addresses)+1)
        ]
    
    def generate_points_within_polygon(self, neighborhood):
        polygon = self.df_district.loc[neighborhood, "geometry"]
        minx, miny, maxx, maxy = polygon.bounds
        while True:
            x = np.random.uniform(minx, maxx)
            y = np.random.uniform(miny, maxy)
            point = Point(x, y)
            if polygon.contains(point):
                # return LAT &  LON
                return y, x
            
    def generate_address(self, point):
        # get address from coordinates
        raw = self.geolocator.reverse(point, timeout=3).raw  # Reverse geocoding with latitude and longitude
        address = raw["address"]
        return {
            "road": address.get("road", ""), 
            "house_number": address.get("house_number", ""), 
            "suburb": address.get("suburb", ""),
            "city_district": address.get("city_district", ""),
            "state": address.get("state", ""), 
            "postcode": address.get("postcode", ""),
            "country": address.get("country", ""),
            "lat": raw.get("lat", ""),
            "lon": raw.get("lon", ""),
        }

    
    def generate_address_data(self, filename):
        address_list = []
        for client_id in self.client_id_list:
            neighborhood = self.generate_neighborhood()
            point = self.generate_points_within_polygon(neighborhood)
            address = self.generate_address(point)
            address_data = {
                'client_id': client_id,
                'address_id': self.generate_id(),
                'neighborhood': neighborhood,
                'coordinates': point,
                "road": address.get("road"), 
                "house_number": address.get("house_number"), 
                "suburb": address.get("suburb"),
                "city_district": address.get("city_district"),
                "state": address.get("state"), 
                "postcode": address.get("postcode"),
                "country": address.get("country"),
                "lat": address.get("lat"),
                "lon": address.get("lon"),
            }
            address_list.append(address_data)
        self.save_dict(filename, address_list)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic client data and geolocate it.")
    parser.add_argument('--num_clients', type=int, default=20, help='Number of clients to generate')
    parser.add_argument('--city', type=str, default='Madrid', help='City name')
    parser.add_argument('--filename', type=str, default='clients_geo.csv', help='Input filename for geo-located clients dataframe')
    
    args = parser.parse_args()
    
    city_population = os.path.join(ROOT_PATH, STATIC_DATA, POPULATION)
    shapefile = os.path.join(ROOT_PATH, STATIC_DATA, SHAPE_FILE)
    client = os.path.join(ROOT_PATH, RESULTS, CLIENT)
    address = os.path.join(ROOT_PATH, RESULTS, ADDRESS)
    
    client_generator = ClientDataGenerator()
    clients = client_generator.generate_client_data(client, args.num_clients)
    address_generator = AddressDataGenerator(clients, shapefile, city_population, args.city)
    address_generator.generate_address_data(address)


if __name__ == "__main__":
    main()
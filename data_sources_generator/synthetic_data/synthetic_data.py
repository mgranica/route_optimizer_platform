from faker import Faker
import random
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
from geopy.geocoders import Nominatim
import argparse
import os


ROOT_PATH = os.path.dirname(__file__)
STATIC_DATA = "static_data"
POPULATION = "city_population.json"
RESULTS = "results"
CLIENT_DATA = "client_data.json"
SHAPE_FILE = "Distritos.shp"

class ClientDataGenerator:
    def __init__(self, filename, city, output):
        self.fake = Faker('es_ES')
        self.city = city
        self.city_data = self.load_static_data(filename)
        self.output = output

    def load_static_data(self, filename):
        with open(filename, 'r') as file:
            static_data = json.load(file)
        return self.weight_population(static_data[self.city])
    
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

    def generate_client_data(self, num_clients):
        clients = []
        for _ in range(num_clients):
            neighborhood = self.generate_neighborhood()
            gender = self.generate_gender()
            first_name = self.generate_first_name(gender)
            last_name = self.fake.last_name()
            email = self.generate_email(first_name, last_name)
            status = self.generate_status()

            client = {
                'client_id': str(self.fake.random_number(digits=12)),
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone_number': self.fake.phone_number(),
                'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d"),
                'gender': gender,
                'occupation': self.fake.job(),
                'neighborhood': neighborhood,
                'created_at': self.fake.date_this_decade(before_today=True, after_today=False).strftime("%Y-%m-%d"),
                'updated_at': self.fake.date_time_between(start_date='-1y', end_date='now').strftime("%Y-%m-%d"),
                'status': status, 
            }
            clients.append(client)
        self.save_dict(clients)
        return clients
    
    def save_dict(self, dict):
        try:
            # Save the dictionary as JSON
            with open(self.output, "w") as json_file:
                json.dump(dict, json_file)
            print(f"Dictionary saved to {self.output}")
        except IOError as e:
            print(f"Error occurred while saving dictionary: {e}")
                

class ClientDataReverseGeolocator:
    def __init__(self, clients, shapefile, filename) -> None:
        self.df_clients = pd.DataFrame(clients).sort_values(by="neighborhood", ignore_index=True)
        self.df_district = self.load_shape_data(shapefile)
        self.filename = filename
        self.geolocator = Nominatim(user_agent="geo_reverse")       
        
    def load_shape_data(self, shapefile, target_crs = "EPSG:4326"):
        df = gpd.read_file(shapefile)
        return df.to_crs(target_crs)
    
    @staticmethod
    def generate_points_within_polygon(polygon, num_points):
        minx, miny, maxx, maxy = polygon.bounds
        points = []
        while len(points) < num_points:
            x = np.random.uniform(minx, maxx)
            y = np.random.uniform(miny, maxy)
            point = Point(x, y)
            if polygon.contains(point):
                points.append((y, x))
        return points
    
    def generate_address(self, point):
        # get address from coordinates
        raw = self.geolocator.reverse(point, timeout=10).raw  # Reverse geocoding with latitude and longitude
        address = raw["address"]
        return (
            address.get("road", ""), 
            address.get("house_number", ""), 
            address.get("suburb", ""),
            address.get("city_district", ""),
            address.get("state", ""), 
            address.get("postcode", ""),
            address.get("country", ""),
            raw.get("lat", ""),
            raw.get("lon", ""),
        )
    
    def generate_weighted_dataframe(self):
        self.df_weight = (
            self.df_clients
            .groupby("neighborhood", as_index=False)
            .agg({"client_id": "count"})
            .rename(columns={"neighborhood": "NOMBRE", "client_id": "num_clientes"})
            .merge(self.df_district, on=["NOMBRE"])
        )
    
    def generate_points_dataframe(self):
        points_columns = [
            "NOMBRE", "num_clientes", "COD_DIS_TX", "points", #"geometry",
        ]
        self.df_points =(
            self.df_weight
            .assign(
                points= lambda df: df.apply(
                    lambda x: self.generate_points_within_polygon(x["geometry"], x["num_clientes"]), axis=1
                )
            )
            .explode("points")
            .reset_index(drop=True)
            [points_columns]
        )
        
    def generate_address_dataframe(self):
        address_columns = [
            "road",  
            "house_number",  
            "suburb",
            "city_district",
            "state",  
            "postcode", 
            "country",
            "lat",
            "lon"
        ]

        df_address = (
            self.df_points
            .apply(
                lambda x: self.generate_address(x["points"]), axis=1, result_type="expand"
            )
            .set_axis(address_columns, axis=1)
            .assign(
                city_district = lambda df: df["city_district"].str.replace("-", " - "),
                district_name = lambda df: np.where(
                    df["city_district"] == "",
                    df["suburb"],
                    df["city_district"],
                ),
                address = lambda df: df["road"].astype(str) + df["house_number"]
            )
            .drop(columns=["suburb", "city_district", "road", "house_number"])
        )
        self.df_geolocation = pd.concat([self.df_points, df_address], axis=1)
    
    def generate_client_geo_dataframe(self):
        client_geolocation_columns = [
            "client_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "gender",
            "occupation",
            "address",
            "neighborhood",
            "district_name",# to corroborate geolocation API functionality
            "state",
            "postcode",
            "country",
            "created_at",
            "updated_at",
            "status",
            "points",
            "lat",
            "lon",   
        ]
        self.df_client_geolocation = pd.concat(
            [self.df_clients, self.df_geolocation], axis=1
        )[client_geolocation_columns]
        self.df_client_geolocation.to_csv(self.filename, index=False)
        
    def generate_reverse_geo_dataframe(self):
        self.generate_weighted_dataframe()
        self.generate_points_dataframe()
        self.generate_address_dataframe()
        self.generate_client_geo_dataframe()


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic client data and geolocate it.")
    parser.add_argument('--num_clients', type=int, default=20, help='Number of clients to generate')
    parser.add_argument('--city', type=str, default='Madrid', help='City name')
    parser.add_argument('--filename', type=str, default='clients_geo.csv', help='Input filename for geo-located clients dataframe')
    
    args = parser.parse_args()
    
    city_population = os.path.join(ROOT_PATH, STATIC_DATA, POPULATION)
    shapefile = os.path.join(ROOT_PATH, STATIC_DATA, SHAPE_FILE)
    client_data = os.path.join(ROOT_PATH, RESULTS, CLIENT_DATA)
    filename = os.path.join(ROOT_PATH, RESULTS, args.filename)
    
    generator = ClientDataGenerator(city_population, args.city, client_data)
    clients = generator.generate_client_data(args.num_clients)
    geolocator = ClientDataReverseGeolocator(clients, shapefile, filename)
    geolocator.generate_reverse_geo_dataframe()


if __name__ == "__main__":
    main()
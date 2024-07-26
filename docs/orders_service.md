# Order Service

## Overview

The Order Simulation Service is designed to generate simulated order data by processing input from three main data tables: Customers, Addresses, and Products. The service utilizes AWS Kinesis to implement a producer-consumer structure that streams the simulated order events. These streams can then be consumed by various downstream applications for analysis, monitoring, and further processing.


##  Data Tables Schema

### Customers Table
The Customers table contains information about the clients. Each record includes personal details and metadata about the client.

Schema:

```
{
    "client_id": "cus-5855b54f-2e4f-44e2-83ee-67006cce78ce",
    "first_name": "Kike",
    "last_name": "Rios",
    "email": "kike.rios@hotmail.com",
    "phone_number": "+34882004486",
    "date_of_birth": "1940-10-12",
    "gender": "Male",
    "occupation": "Reparador de bicicletas",
    "created_at": "2022-06-28",
    "updated_at": "2023-10-21",
    "status": "active"
}
```

### Addresses Table

The Addresses table stores address information associated with clients. Each record includes detailed location data, including coordinates.

Schema:

```
{
    "client_id": "cus-7d70c702-01ed-4619-a211-ad59e51371b1",
    "address_id": "cus-9de25694-d4b2-4c73-a81f-7b82cee16f7e",
    "neighborhood": "Fuencarral - El Pardo",
    "coordinates": [
        40.616026405147196,
        -3.630901451761291
    ],
    "road": "Calle Abedul",
    "house_number": "",
    "suburb": "Ciudalcampo",
    "city_district": "Fuencarral-El Pardo",
    "state": "Comunidad de Madrid",
    "postcode": "28707",
    "country": "España",
    "lat": "40.616839",
    "lon": "-3.6257757"
}
```

### Orders Stream


```
{
    'eventId': 'ev-b2543515-c6f2-45f2-8853-a090f83ea6ca', 
    'eventType': 'ORDER_CREATED', 
    'eventTimestamp': '2024-06-10 16:08:24', 
    'orderId': 'ord-8cb158b4-2aed-4e4f-b600-929a0ed63d1c', 
    'orderDetails': {
        'customerId': 'cus-fd8690ab-598b-4c38-901a-ab66775f93c5', 
        'orderDate': '2024-06-10 16:07:32', 
        'items': [
            {
                'itemId': '111e2222-e33b-44d3-a456-426614174333', 
                'productName': 'armario', 
                'quantity': 1, 
                'price': 699.99, 
                'weight': 23.5
            }, 
            {
                'itemId': '222e3333-e44b-55d3-a456-426614174444', 
                'productName': 'silla', 
                'quantity': 2, 
                'price': 49.99, 
                'weight': 15.6
            }
        ], 
        'totalAmount': 799.97, 
        'totalWeight': 54.7, 
        'status': 'PENDING', 
        'destinationAddress': {
            'address_id': 'cus-bb86c5df-937a-468d-947f-73f3080b4bad', 
            'neighborhood': 'Carabanchel', 
            'coordinates': [40.38355845858851, -3.732050010120695], 
            'road': 'Calle del Avefría', 
            'house_number': '38', 
            'suburb': 'Carabanchel', 
            'city_district': '', 
            'state': 'Comunidad de Madrid', 
            'postcode': '28025', 
            'country': 'España', 
            'lat': 40.38357925415039, 
            'lon': -3.7320752143859863
        }, 
        'paymentDetails': {
            'paymentMethod': '', 
            'paymentStatus': '', 
            'transactionId': ''
        }
    }
}
```

# TODO

> set of tasks to complete the implementation of the microservice

1. Stream implementation
    1.1 Producer
    1.2 Consumer

2. Migration to a python code

3. 

# To be Considered

- <input type="checkbox" disabled checked /> Add historical orders
- <input type="checkbox" disabled /> Implement medallion architecture
- <input type="checkbox" disabled /> build metastore data

## Task Status

| Task           | Time required | Assigned to   | Current Status | Finished | 
|----------------|---------------|---------------|----------------|-----------|
| Calendar Cache | > 5 hours  |  | in progress | :white_check_mark
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 


* https://quix.io/blog/kafka-kinesis-comparison
* https://www.softkraft.co/aws-kinesis-vs-kafka-comparison/
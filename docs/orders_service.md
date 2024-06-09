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


# Synthetic Data Generator

## Overview
This script generates synthetic client and address data, using the `Faker` library for client information and geospatial libraries for address data. The data can be used for testing and development purposes, particularly for systems that require client and geolocation data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation
To use this script, you'll need Python 3.x and several Python libraries. It is recommended to use `pipenv` for managing dependencies and virtual environments.

### Step 1: Install Pipenv
If you don't have `pipenv` installed, you can install it using pip:

```bash
pip install pipenv
```

### Step 2: Set Up the Environment
Navigate to the project directory and install the required packages using `pipenv`:

```bash
pipenv install
```

This will create a virtual environment and install all dependencies listed in the `Pipfile`.

### Step 3: Activate the Virtual Environment
Activate the virtual environment:

```bash
pipenv shell
```

## Usage
To run the script and generate synthetic data, use the following command:

```bash
python synthetic_data_generator.py --num_clients <number_of_clients> --city <city_name> --filename <output_filename>
```

### Arguments
- `--num_clients`: (Optional) The number of client records to generate. Default is 20.
- `--city`: (Optional) The city name for generating address data. Default is 'Madrid'.
- `--filename`: (Optional) The output filename for the geo-located clients dataframe. Default is 'clients_geo.csv'.

## File Structure
The project directory should have the following structure:

```
synthetic_data_generator/
│
├── static_data/
│   ├── city_population.json       # Population data for cities
│   └── Distritos.shp              # Shapefile for city districts
│
├── results/
│   ├── client_data.json           # Generated client data
│   └── address_data.json          # Generated address data
│
├── synthetic_data_generator.py    # Main script file
└── README.md                      # This README file
```

## Configuration
- **Static Data**: The script uses static data files for city populations and shapefiles for district boundaries. Ensure these files are placed correctly in the `static_data` directory.
- **Output Data**: Generated data will be saved in the `results` directory. The filenames for client and address data are specified within the script.

## Examples
Generate 50 clients for the city of Barcelona and save the output to `barcelona_clients.csv`:

```bash
python synthetic_data_generator.py --num_clients 50 --city Barcelona --filename barcelona_clients.csv
```

## Dependencies
The dependencies are managed through `pipenv` and listed in the `Pipfile`.

- [Faker](https://github.com/joke2k/faker)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [GeoPandas](https://geopandas.org/)
- [Shapely](https://shapely.readthedocs.io/)
- [Geopy](https://geopy.readthedocs.io/)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [UUID](https://docs.python.org/3/library/uuid.html)
- [JSON](https://docs.python.org/3/library/json.html)
- [OS](https://docs.python.org/3/library/os.html)

## Contributing
Contributions are welcome! Please create a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License.

---

### Pipfile

Additionally, include a `Pipfile` for managing the dependencies with `pipenv`:

```toml
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
Faker = "*"
pandas = "*"
numpy = "*"
geopandas = "*"
shapely = "*"
geopy = "*"
argparse = "*"

[requires]
python_version = "3.x"
```

Feel free to adjust the `python_version` according to your specific Python version.
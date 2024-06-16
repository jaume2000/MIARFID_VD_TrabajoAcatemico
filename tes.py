import json

# Cargar el archivo GeoJSON
geojson_path = './mnt/data/countries.geo.json'

with open(geojson_path, 'r') as file:
    geojson_data = json.load(file)

# Inspeccionar las propiedades de la primera característica
print(geojson_data['features'][0]['properties'])

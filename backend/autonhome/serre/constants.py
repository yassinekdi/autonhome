measures_metadata = {
    'temperature': {'label': 'Température',
                    'unit': '°C'},
    'humidity': {'label': 'Humidité',
                    'unit': '%'},
    'tds': {'label': 'TDS',
                    'unit': 'ppm'},
    "luminosity" : {'label': 'Luminosité',
                    'unit': 'lux'},                   
    'pH': {'label': 'pH',
                    'unit': ''},
}
SECTIONS_CHOICE = (
        ('AIR', 'AIR'),
        ('EAU', 'EAU'),
        ('POT1','POT1'),
        ('POT2','POT2'),
    )
SENSOR_TYPE_CHOICES = (
        ('Temperature', 'Temperature'),
        ('Humidity', 'Humidity'),
        ('Luminosity', 'Luminosity'),
        ('Dissolved Solids', 'Dissolved Solids'),
        ('pH', 'pH'),
        # Add other sensor types if necessary
    )
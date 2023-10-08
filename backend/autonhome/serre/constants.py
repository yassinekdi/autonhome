measures_metadata = {
    'temperature': {'label': 'Température',
                    'unit': '°C'},
    'humidity': {'label': 'Humidité',
                    'unit': '%'},
    'tds': {'label': 'TDS',
                    'unit': 'ppm'},
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
        # Add other sensor types if necessary
    )
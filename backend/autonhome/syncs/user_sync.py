import os
import json
from dotenv import dotenv_values
from pathlib import Path

class UserSync:
    def __init__(self, user_dir, sensors_dir):
        self.user_dir = user_dir
        self.sensors_dir = sensors_dir
        self.env = dotenv_values()
        self.user_id = int(user_dir.split('/')[-1])

    def sync(self):
        # copy sensor files
        for sensor in os.listdir(self.sensors_dir):
            sensor_path = os.path.join(self.sensors_dir, sensor)
            if os.path.isdir(sensor_path):
                os.makedirs(os.path.join(self.user_dir, sensor), exist_ok=True)
                for file in os.listdir(sensor_path):
                    if file.endswith('.ino'):
                        self._copy_and_update_file(os.path.join(sensor_path, file))

    def _copy_and_update_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # update values
        for i, line in enumerate(lines):
            if line.startswith('const char* WIFI_SSID'):
                lines[i] = f'const char* WIFI_SSID = "{self.env["WIFI_SSID"]}";\n'
            elif line.startswith('const char* WIFI_PASSWORD'):
                lines[i] = f'const char* WIFI_PASSWORD = "{self.env["WIFI_PASSWORD"]}";\n'
            elif line.startswith('String FIREBASE_HOST'):
                lines[i] = f'String FIREBASE_HOST = "{self.env["FIREBASE_HOST"]}";\n'
            elif line.startswith('String FIREBASE_AUTH'):
                lines[i] = f'String FIREBASE_AUTH = "{self.env["FIREBASE_AUTH"]}";\n'
            elif line.startswith('String UserId'):
                lines[i] = f'String UserId = "{self.user_id}";\n'

        # write updated file to new location
        with open(os.path.join(self.user_dir, Path(file_path).relative_to(self.sensors_dir)), 'w') as f:
            f.writelines(lines)


    
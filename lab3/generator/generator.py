import json
import random
import time

import requests

with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())
    message_count = config["message_count"]

url = "http://aggregator/aggregate"

for _ in range(message_count):
    message = random.randint(1, 100)
    requests.post(url, json={"number": message})
    time.sleep(0.1)

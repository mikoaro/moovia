from kafka import KafkaProducer
import json
import datetime
import uuid
import time

# READ COORDINATES FROM GEOJSON
input_file = open('./data/bus3.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

# GENERATE UUID
def generate_uuid():
    return uuid.uuid4()

# KAFKA PRODUCER
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}
data['busline'] = '00003'
data['key'] = data['busline'] + '_' + str(generate_uuid())

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.datetime.now(datetime.timezone.utc))
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data) 
        print(message)
        producer.send('testBusdata', message.encode('ascii')) 
        time.sleep(1)

        # if bus reaches last coordinate, start from beginning
        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)

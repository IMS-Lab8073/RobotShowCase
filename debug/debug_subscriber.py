import paho.mqtt.subscribe as subscribe
import json

def print_msg(client, userdata, message):
    try:
        recieve_data_dict = json.loads(message.payload)
        print(recieve_data_dict)
        print("Location id : " + str(recieve_data_dict["location_id"]))
        print()
    except Exception as e:
        print(e)

while True:
    subscribe.callback(print_msg, "toUnit/Robotdata", hostname="localhost")

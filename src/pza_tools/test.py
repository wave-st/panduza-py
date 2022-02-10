import time
import json
import paho.mqtt.client as mqtt


DEFAULT_CFG_PATH='/etc/panduza/sysfs.json'


DEFAULT_CFG = {
    'broker': {
        'address': "localhost"
    }
}


RUNN = True

if __name__ == '__main__':

    cfg = DEFAULT_CFG

    # # Opening JSON file
    # f = open(DEFAULT_CFG_PATH)
    
    # # returns JSON object as
    # # a dictionary
    # data = json.load(f)
    
    # # Iterating through the json
    # print(data)
    
    # # Closing file
    # f.close()

    def _on_message(client, userdata, msg):
        print(f"Connected with result code {msg.payload}")
        # client.loop_stop(force=True)

        global RUNN
        RUNN = False
        

    client = mqtt.Client()
    client.on_message = _on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("pza/all/interfaces")


    client.publish('pza/all/cmd/scan', "do", qos=0, retain=False)
    print(f"send to a/b")
    
    
    while RUNN:
        client.loop()


    # loop_stop(force=False)


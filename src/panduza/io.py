import json
from .core import Core
import json
import logging


# Module logger
mog = logging.getLogger("pza.pipe")


class Io:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None) -> None:
        """
        """
        self.client, self.baseTopic = Core.GetClientAndBaseTopic(alias)
        
    ###########################################################################
    ###########################################################################

    def writeDirection(self, direction, ack=0):
        """
        @param ack : if 0 do not wait for ack, else block until ack recieved or ack timeout
        """

        # def _on_message(client, userdata, msg):
        #     print(f"Connected with result code {msg.payload}")
            # client.loop_stop(force=True)

        # global RUNN
        # RUNN = False
        
        # self.client.on_message = _on_message
        # client.connect("localhost", 1883, 60)


        payload = json.dumps({ "direction": direction })
        self.client.publish(self.baseTopic + "/cmds/direction/set", payload, qos=0, retain=False)


        # client.publish('pza/all/cmd/scan', "do", qos=0, retain=False)
        # print(f"send to a/b")
        
        
        # while RUNN:
        #     client.loop()

        # # Prepare url & payload
        # url = self.url + '/direction'
        # payload = { "direction": direction }
        # # Debug
        # mog.debug("writeDirection [%s] to [%s]", json.dumps(payload), url)

        # # Send request
        # r = requests.put( url, json=payload )
        # mog.debug("response %s", r)

        # # Manage errors
        # if(r.status_code != 200):
        #     raise Exception("write direction failure [" + repr(r) + "]")
        

    ###########################################################################
    ###########################################################################

    def readDirection(self):
        """
        """
        # r = requests.get(self.url + '/direction')

        # # Manage http errors
        # if(r.status_code != 200):
        #     raise Exception("read direction failure [" + repr(r) + "]")

        # # Manage payload errors
        # body = r.json()
        # if "direction" not in body:
        #     raise Exception("response has no 'direction'")

        # return body["direction"]
        pass

    ###########################################################################
    ###########################################################################

    def writeValue(self, value):
        """
        """
        
        payload = json.dumps({ "value": value })
        self.client.publish(self.baseTopic + "/cmds/value/set", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################
    
    def readValue(self):
        """
        """        
        self.client.subscribe(self.baseTopic + "/atts/value")

        def _on_message(client, userdata, msg):
            # print(f"Connected with result code {msg.payload}")
            global CONTEXT
            CONTEXT = { "alive":False, "payload": msg.payload }

        self.client.on_message = _on_message

        global CONTEXT
        CONTEXT = { "alive":True, "payload": None }
        while CONTEXT["alive"]:
            self.client.loop()

        self.client.unsubscribe(self.baseTopic + "/atts/value")

        obj = json.loads( CONTEXT["payload"] )
        # print()
        return obj["value"]


    ###########################################################################
    ###########################################################################
    

import json
from .core import Core
import json
import logging
import base64
from .interface import PzaInterface


class SpiSlave(PzaInterface):
    """
    """

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None):
        """ Constructor
        """
        super().__init__(alias)

        self.pending_data = []

        self.client.subscribe(self.baseTopic + "/atts/data")

    ###########################################################################
    ###########################################################################

    def has_pending_data(self):
        """ Return the number of pending data
        """
        return len(self.pending_data)

    ###########################################################################
    ###########################################################################

    def pop_data(self):
        """
        """
        if len(self.pending_data) <= 0:
            return None
        return self.pending_data.pop(0)

    ###########################################################################
    ###########################################################################

    def push_response(self, data):
        """
        """
        payload = json.dumps({
            "data": base64.b64encode(data).decode('ascii')
        })
        self.client.publish(self.baseTopic + "/cmds/responses/push", payload, qos=0, retain=False)


    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        """
        """
        #
        super()._on_mqtt_message(client, userdata, msg)

        print("sub class _on_mqtt_message  slave !!", "\n")
        
        # 
        if msg.topic.endswith('/atts/data'):
            print(f"pok {msg.payload} \n")
        
            request = self.payload_to_dict(msg.payload)
            data = base64.b64decode(request["data"])
            
            self.pending_data.append(data)



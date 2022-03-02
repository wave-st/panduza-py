import json
import base64
import logging
from .core import Core
from .interface import PzaInterface


class TwiMaster(PzaInterface):
    """
    """

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None):
        """ Constructor
        """
        super().__init__(alias)

        # self.pending_data = []

        # self.client.subscribe(self.baseTopic + "/atts/data")

    # ###########################################################################
    # ###########################################################################

    # def has_pending_data(self):
    #     """ Return the number of pending data
    #     """
    #     return len(self.pending_data)

    # ###########################################################################
    # ###########################################################################

    # def pop_data(self):
    #     """
    #     """
    #     if len(self.pending_data) <= 0:
    #         return None
    #     return self.pending_data.pop(0)

    ###########################################################################
    ###########################################################################
    
    def write(self, data):
        """
        """
        payload = json.dumps({
            "data": base64.b64encode(data).decode('ascii')
        })
        self.client.publish(self.baseTopic + "/cmds/data/write", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################
    
    def read(self, size):
        """
        """
        payload = json.dumps({
            "size": size
        })
        self.client.publish(self.baseTopic + "/cmds/data/read", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################
    
    def writeRead(self, data):
        """
        """
        payload = json.dumps({
            "data": base64.b64encode(data).decode('ascii')
        })
        self.client.publish(self.baseTopic + "/cmds/data/writeRead", payload, qos=0, retain=False)

    # ###########################################################################
    # ###########################################################################

    # def _on_mqtt_message(self, client, userdata, msg):
    #     """
    #     """
    #     #
    #     super()._on_mqtt_message(client, userdata, msg)
        
        
    #     # 
    #     if msg.topic.endswith('/atts/data'):
    #         request = self.payload_to_dict(msg.payload)
    #         data = base64.b64decode(request["data"])
            
    #         self.pending_data.append(data)

    # ###########################################################################
    # ###########################################################################


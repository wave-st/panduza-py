import json
from .core import Core
import json
import logging
import base64



class SpiSlave:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None) -> None:
        """Constructor
        """
        self.client, self.baseTopic = Core.GetClientAndBaseTopic(alias)

        
        # self.client.subscribe(self.baseTopic + "/atts/value")

        # def _on_message(client, userdata, msg):
        #     # print(f"Connected with result code {msg.payload}")
        #     global CONTEXT
        #     CONTEXT = { "alive":False, "payload": msg.payload }

        # self.client.on_message = _on_message



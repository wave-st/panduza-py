import json
from .core import Core
import json
import logging
import base64



class SpiMaster:

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


    ###########################################################################
    ###########################################################################
    
    def transfer(self, out_buffer, in_request):
        """
        """
        
        
        payload = json.dumps({
            "in_request": in_request,
            "out_buffer": base64.b64encode(out_buffer).decode('ascii')
        })
        # self.client.publish(self.baseTopic + "/cmds/value/set", payload, qos=0, retain=False)

        pass

    ###########################################################################
    ###########################################################################
    

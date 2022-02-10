import json
from .core import Core
import json
import logging

# Module logger
mog = logging.getLogger("pza.pipe")

class Can:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None) -> None:
        """
        """
        self.client, self.baseTopic = Core.GetClientAndBaseTopic(alias)

    ###########################################################################
    ###########################################################################
    
    def write(self, id, payload):
        """
        """
        jsonFrame = {}
        jsonFrame['type'] = 'msg'
        jsonFrame['id'] = id
        jsonFrame['length'] = len(payload)
        jsonFrame['payload'] = []
        for element in payload:
            jsonFrame['payload'].append(element)
        
        mog.debug("Can write > %s (%s)", self.baseTopic + "/cmds/msg", json.dumps(jsonFrame))
        self.client.publish(self.baseTopic + "/cmds/msg", json.dumps(jsonFrame), qos=0, retain=False)

    ###########################################################################
    ###########################################################################

    def read(self):
        """
        """
        print("read!!")

    ###########################################################################
    ###########################################################################

    def read_loop(self, on_data):
        """
        """
        def _on_message(client, userdata, msg):
            on_data(msg.payload)

        self.client.on_message = _on_message
        self.client.subscribe(self.baseTopic + "/atts/msg")
        self.client.loop_start()

    ###########################################################################
    ###########################################################################

    def read_loop_stop(self):
        """
        """
        self.client.loop_stop()

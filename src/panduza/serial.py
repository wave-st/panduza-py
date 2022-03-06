import json
from .core import Core
import json
import logging

# Module logger
mog = logging.getLogger("pza.pipe")

class Serial:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None) -> None:
        """
        """
        self.client, self.base_topic = Core.GetClientAndBaseTopic(alias)

    ###########################################################################
    ###########################################################################
    
    def write(self, data):
        """
        """
        mog.debug("Serial write > %s (%s)", self.base_topic + "/cmds/data/send", data)
        self.client.publish(self.base_topic + "/cmds/data/send", data, qos=0, retain=False)

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
        self.client.subscribe(self.base_topic + "/atts/data")
        self.client.loop_start()

    ###########################################################################
    ###########################################################################

    def read_loop_stop(self):
        """
        """
        self.client.loop_stop()




        
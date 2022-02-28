import json
from .core import Core
import json
import logging
import base64



class SpiSlave:
    """
    """

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None):
        """ Constructor
        """
        super().__init__(alias)

        self.client.subscribe(self.baseTopic + "/atts/data")


    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        """
        """
        super()._on_mqtt_message(client, userdata, msg)

        print("sub class _on_mqtt_message  slave !!")

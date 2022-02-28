import json
import base64
import logging
from .core import Core
from .interface import PzaInterface


class SpiMaster(PzaInterface):
    """
    """

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None):
        """ Constructor
        """
        super().__init__(alias)

    ###########################################################################
    ###########################################################################
    
    def transfer(self, out_buffer, in_request):
        """
        """
        payload = json.dumps({
            "in_request": in_request,
            "out_buffer": base64.b64encode(out_buffer).decode('ascii')
        })
        self.client.publish(self.baseTopic + "/cmds/data/transfer", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################


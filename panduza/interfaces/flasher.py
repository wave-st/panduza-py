from panduza.core.interface import Interface
from ..core import Core
import json
import logging
import os
import base64

# Module logger
mog = logging.getLogger("pza.pipe")

class Flasher(Interface):

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None, url=None, port=None, b_topic=None, pza_client=None):
        """
        """
        # self.base_topic = Core.BaseTopicFromAlias(alias)
        # self.client.subscribe(self.base_topic + "/atts/#")
        # self.client.message_callback_add(self.base_topic + "/atts/result", self.__flashResult)
        super().__init__(alias, url, port, b_topic, pza_client)


    ###########################################################################
    ###########################################################################     
   

    def __flashResult():
        print("result!")


    def flash(self, address, binpath):
        binfile = open(binpath, 'rb')
        contents = binfile.read()

        payload = {
            "addr" : address,
            "filename" : os.path.basename(binpath),
            "bin" : base64.standard_b64encode(contents).decode("ascii")
        }
        cmd = self.base_topic + "/flasher_test/cmds/flasher"
        print(cmd)
        self.client.publish(cmd, json.dumps(payload))

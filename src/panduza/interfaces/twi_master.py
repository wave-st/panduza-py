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
    
    def __init__(self, alias=None, b_addr=None, b_port=None, b_topic=None):
        """ Constructor
        """
        super().__init__(alias, b_addr, b_port, b_topic)

        self.pending_data = []

        self.client.subscribe(self.base_topic + "/atts/data")

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
    
    def write(self, data, addr, addr_10b=False, no_stop=False):
        """
        """
        # Prepare the payload
        payload_dict = {
            "data": base64.b64encode(data).decode('ascii'),
            "addr": addr
        }
        if addr_10b:
            payload_dict["addr_10b"] = addr_10b
        if no_stop:
            payload_dict["no_stop"] = no_stop

        payload = json.dumps(payload_dict)
            
        self.client.publish(self.base_topic + "/cmds/data/write", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################
    
    def read(self, size):
        """
        """
        payload = json.dumps({
            "size": size
        })
        self.client.publish(self.base_topic + "/cmds/data/read", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################
    
    def writeRead(self, addr, w_data, r_size, addr_10b=False, no_stop=False):
        """Send a twi WriteRead request

        Args:
            addr (int): twi address of the device
            w_data (bytes): data that must be written first
            r_size (int): number of byte that must be read after the write operation
        """
        payload = json.dumps({
            "addr": addr,
            "size": r_size,
            "data": base64.b64encode(w_data).decode('ascii')
        })
        self.client.publish(self.base_topic + "/cmds/data/writeRead", payload, qos=0, retain=False)

    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        """_summary_

        Args:
            client (_type_): _description_
            userdata (_type_): _description_
            msg (_type_): _description_
        """
        #
        super()._on_mqtt_message(client, userdata, msg)
                
        # 
        if msg.topic.endswith('/atts/data'):
            request = self.payload_to_dict(msg.payload)
            data = base64.b64decode(request["data"])
            
            self.pending_data.append(data)



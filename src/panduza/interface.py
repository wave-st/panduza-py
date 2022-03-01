import time
import json
from .core import Core

class PzaInterface:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None):
        """ Constructor
        """
        self.HBM = { "alive": False, "enabled": False, "heartbeat": 0 }
        self.client, self.baseTopic = Core.GetClientAndBaseTopic(alias)

        self.client.on_message = self._on_mqtt_message
        self.client.loop_start()

    ###########################################################################
    ###########################################################################

    def payload_to_dict(self, payload):
        """ To parse json payload
        """
        return json.loads(payload.decode("utf-8"))

    ###########################################################################
    ###########################################################################

    def payload_to_int(self, payload):
        """
        """
        return int(payload.decode("utf-8"))

    ###########################################################################
    ###########################################################################

    def payload_to_str(self, payload):
        """
        """
        return payload.decode("utf-8")

    ###########################################################################
    ###########################################################################

    def enableHeartBeatMonitoring(self):
        """
        """
        self.client.subscribe(self.baseTopic + "/info")
        self.HBM = { "alive": False, "enabled": True, "heartbeat": time.time() }

    ###########################################################################
    ###########################################################################

    def disableHeartBeatMonitoring(self):
        self.client.unsubscribe(self.baseTopic + "/info")
        self.HBM = { "enabled": False }

    ###########################################################################
    ###########################################################################

    def isAlive(self):
        """
        """
        if not self.HBM["enabled"]:
            raise Exception("watchdog not enabled on the interface")
        
        t0 = time.time()
        while (time.time() - t0 < 3) and not self.HBM["alive"]:
            pass

        return self.HBM["alive"]

    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        # print("!!!", msg.topic)

        if self.HBM["enabled"] and msg.topic.endswith('/info'):
            # print("info !!!  ", time.time(), "\n")
            elapsed = time.time() - self.HBM["heartbeat"]
            self.HBM["heartbeat"] = time.time()

            if elapsed > 5 and self.HBM["alive"]:
                self.HBM["alive"] = False
            elif not self.HBM["alive"]:
                self.HBM["alive"] = True



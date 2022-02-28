import time
from .core import Core

class PzaInterface:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None):
        """ Constructor
        """
        self.watchdog = { "alive": False, "enabled": False, "heartbeat": 0 }
        self.client, self.baseTopic = Core.GetClientAndBaseTopic(alias)

        self.client.on_message = self._on_mqtt_message
        self.client.loop_start()

    ###########################################################################
    ###########################################################################

    def enableWatchdog(self):
        """
        """
        self.client.subscribe(self.baseTopic + "/info")
        self.watchdog = { "alive": False, "enabled": True, "heartbeat": time.time() }

    ###########################################################################
    ###########################################################################

    def disableWatchdog(self):
        self.client.unsubscribe(self.baseTopic + "/info")
        self.watchdog = { "enabled": False }

    ###########################################################################
    ###########################################################################

    def isAlive(self):
        """
        """
        if not self.watchdog["enabled"]:
            raise Exception("watchdog not enabled on the interface")
        
        t0 = time.time()
        while (time.time() - t0 < 3) and not self.watchdog["alive"]:
            pass

        return self.watchdog["alive"]

    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        print("!!!", msg.topic)

        if self.watchdog["enabled"] and msg.topic.endswith('/info'):
            # print("info !!!  ", time.time(), "\n")
            elapsed = time.time() - self.watchdog["heartbeat"]
            self.watchdog["heartbeat"] = time.time()

            if elapsed > 5 and self.watchdog["alive"]:
                self.watchdog["alive"] = False
            elif not self.watchdog["alive"]:
                self.watchdog["alive"] = True




import time
import json
import paho.mqtt.client as mqtt

from .core import Core
from .heartbeat import HeartBeatMonitoring

class Interface:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None, b_addr=None, b_port=None, b_topic=None):
        """ Constructor
        """
        #
        if alias:
            self.client, self.base_topic = Core.GetClientAndBaseTopic(alias)
        else:
            self.base_topic = b_topic
            self.client = mqtt.Client()
            self.client.connect(b_addr, b_port)

        #
        self.heart_beat_monitoring = HeartBeatMonitoring(self.client, self.base_topic)
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
        print("enableHeartBeatMonitoring ::: DEPRECATED !!!!!!!!!")
        # self.client.subscribe(self.base_topic + "/info")
        # self.HBM = { "alive": False, "enabled": True, "heartbeat": time.time() }

    ###########################################################################
    ###########################################################################

    def disableHeartBeatMonitoring(self):
        print("disableHeartBeatMonitoring ::: DEPRECATED !!!!!!!!!")
        # self.client.unsubscribe(self.base_topic + "/info")
        # self.HBM = { "enabled": False }

    ###########################################################################
    ###########################################################################

    def isAlive(self):
        """
        """
        if not self.heart_beat_monitoring.enabled:
            raise Exception("watchdog not enabled on the interface")
        
        t0 = time.time()
        while (time.time() - t0 < 3) and not self.heart_beat_monitoring.alive:
            pass

        return self.heart_beat_monitoring.alive

    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        # print("!!!", msg.topic)

        if msg.topic.endswith('/info'):
            self.heart_beat_monitoring.update()


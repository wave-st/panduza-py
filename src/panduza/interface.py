import time
import json
from .core import Core
import paho.mqtt.client as mqtt


class HeartBeatMonitoring:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, client, base_topic):
        self.client = client
        self.base_topic = base_topic
        self.alive = False
        self.enabled = False
        self.heartbeat = 0
        self.observers = []

    def enable(self):
        self.client.subscribe(self.base_topic + "/info")
        self.alive = False
        self.enabled = True
        self.heartbeat = time.time()

    def disable(self):
        self.client.unsubscribe(self.base_topic + "/info")
        self.enabled = False

    def update(self):
        if self.enabled:
            # print("info !!!  ", time.time(), "\n")
            
            elapsed = time.time() - self.heartbeat
            self.heartbeat = time.time()

            old_state = self.alive
            if elapsed > 5 and self.alive:
                self.alive = False
            elif not self.alive:
                self.alive = True

            # Notify observers
            if old_state != self.alive:
                for obs in self.observers:
                    obs(self.alive)

    def add_observer(self, cb):
        self.observers.append(cb)
    
    def rem_observer(self, cb):
        self.observers.remove(cb)
        

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class PzaInterface:

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


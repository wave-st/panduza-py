"""
┌────────────────────────┐
│ Simple API for Panduza │
└────────────────────────┘

 Florian Dupeyron
 February 2022
"""

from abc import ABC, abstractmethod

import logging
import queue
import threading
import traceback

import json
import paho.mqtt.client as mqtt

from typing      import Optional, Callable, Set
from dataclasses import dataclass, field

from .core import Core

# ┌────────────────────────────────────────┐
# │ Utilities                              │
# └────────────────────────────────────────┘

def _pza_path_join(*args):
    return "/".join(args)

# ┌────────────────────────────────────────┐
# │ Panduza connection                     │
# └────────────────────────────────────────┘

class Client:
    

    def __init__(self, alias=None, url=None, port=None):

        if alias:
            # load from alias
            pass
        
        else:
            # create client
            pass


        self.log = logging.getLogger(f"Panduza {url}:{port}")
        self.log.info("Init panduza connection")

        self.url                           = url
        self.port                          = port
        self.is_connected                  = False

        # Init MQTT client instance
        self.client                        = mqtt.Client()
        self.client.on_message             = self.__on_message
        self.client.on_connect             = self.__on_connect
        self.client.on_disconnect          = self.__on_disconnect

        # Listeners
        self._listeners                    = dict()
        self._listeners_lock               = threading.RLock()




    # ┌────────────────────────────────────────┐
    # │ Message callback                       │
    # └────────────────────────────────────────┘

    def __on_message(self, client, userdata, message):
        self.log.debug(f"Received MQTT message on topic '{message.topic}' with QOS {message.qos}")

        with self._listeners_lock:
            if message.topic in self._listeners:
                # Call all listener's callbacks
                for callback in self._listeners[message.topic]:
                    callback(message.payload)


    # ┌────────────────────────────────────────┐
    # │ Connect / Disconnect                   │
    # └────────────────────────────────────────┘

    def connect(self):
        self.log.debug("Connect to broker")

        self.client.connect(self.url, self.port)
        self.client.loop_start()


    def disconnect(self):
        self.log.debug("Disconnect from broker")
        self.client.disconnect()
        self.client.loop_stop()

    def __on_connect(self, client, userdata, flags, rc):
        self.is_connected = True

    def __on_disconnect(self, client, userdata, rc):
        self.is_connected = False

    # ┌────────────────────────────────────────┐
    # │ Publish wrapper                        │
    # └────────────────────────────────────────┘

    def publish(self, topic, payload: bytes, qos=0):
        self.log.debug(f"Publish to topic {topic} with QOS={qos}: {payload}")
        self.client.publish(topic, payload, qos=qos, retain=False)


    def publish_json(self, topic, req: dict, qos=0):
        self.publish(
            topic    = topic,
            payload  = json.dumps(req).encode("utf-8"),
            qos      = qos
        )


    # ┌────────────────────────────────────────┐
    # │ Register/Unregister listener           │
    # └────────────────────────────────────────┘
    
    def subscribe(self, topic: str, callback):
        """
        Registers the listener, returns the queue instance
        """

        self.log.debug(f"Register listener for topic '{topic}'")
        with self._listeners_lock:
            # Create set if not existing for topic
            if not topic in self._listeners:
                self._listeners[topic] = set()
                self.client.subscribe(topic)

            # Check that callback is not already registered, and register
            if callback in self._listeners[topic]:
                raise ValueError(f"callback {callback} already registered for topic {topic}")

            else:
                self._listeners[topic].add(callback)


    def unsubscribe(self, topic: str, callback = None):
        """
        Unsuscribe listener from topic. if callback is None, unregister all listeners
        """

        self.log.debug(f"Unregister listener for topic '{topic}'")

        with self._listeners_lock:
            if topic in self._listeners:
                if callback is None:
                    for listener in self._listeners:
                        # Send none value to callback to unlock listener
                        try:
                            listener(None)
                        except:
                            self.log.error(traceback.format_exc())

                    # Remove set from dict (hardcore mode)
                    self.client.unsubscribe(topic)
                    del self._listeners[topic]

                else:
                    if not (callback in self._listeners[topic]):
                        raise ValueError(f"callback {callback} not registered for topic {topic}")
                    else:
                        # Send none value to callback to unlock listener
                        try:
                            callback(None)
                        except:
                            self.log.error(traceback.format_exc())

                        self._listeners[topic].discard(callback)

                        # If set is empty, remove from dict
                        if not self._listeners[topic]:
                            self.client.unsubscribe(topic)
                            del self._listeners[topic]


    # ┌────────────────────────────────────────┐
    # │ Handy stuff                            │
    # └────────────────────────────────────────┘

    #def retained_atts_get(self, topic: str, timeout=5):
    #    """
    #    Supposes atts last message have the retained flag
    #    Returns the raw payload
    #    """

    #    self.log.debug(f"Retrieve atts from topic {topic}")

    #    v    = None
    #    q    = queue.Queue()
    #    clbk = lambda payload: q.put(payload)

    #    # Subscribe to atts topic
    #    self.subscribe(topic, clbk)

    #    # Wait for value
    #    payload = q.get(timeout=timeout)

    #    # Unsubscribe from topic
    #    self.unsubscribe(topic, clbk)

    #    # Return value
    #    return payload



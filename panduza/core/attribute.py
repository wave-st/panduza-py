import os
import json
import logging
import threading

from abc import ABC, abstractmethod
from typing      import Optional, Callable, Set
from dataclasses import dataclass, field

from .client import Client

@dataclass
class Attribute:
    client: Client
    base_topic: str
    name: str

    payload_parser: Callable[[bytes],  any] = field(repr=False, hash=False, compare=False, default=lambda v:v)
    payload_factory: Callable[[bytes], any] = field(repr=False, hash=False, compare=False, default=lambda v:json.dumps(v).encode("utf-8"))

    def __post_init__(self):
        self._topic_atts_get = os.path.join(self.base_topic, "atts", self.name       )
        self._topic_cmds_set = os.path.join(self.base_topic, "cmds", self.name, "set")


    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self):
        pass


###############################################################################
###############################################################################

@dataclass
class Attribute_JSON(Attribute):
    __value: any = None

    def __post_init__(self):
        super().__post_init__()

        self.__trigger = threading.Event()
        self.__log     = logging.getLogger(f"PZA {self.name} attribute for {self.base_topic}")

        # Subscribe to topic
        self.client.subscribe(self._topic_atts_get, callback=self.__update)


    def __del__(self):
        # Unsubscribe from topic
        # self.client.unsubscribe(self._topic_atts_get, callback=self.__update)
        pass

    # ┌────────────────────────────────────────┐
    # │ Update callback                        │
    # └────────────────────────────────────────┘

    def __update(self, payload):
        self.__log.debug("Received new value")

        if payload is None:
            self.__value = None
        else:
            self.__value = self.payload_parser(payload)
            self.__trigger.set()
    

    # ┌────────────────────────────────────────┐
    # │ Trigger control                        │
    # └────────────────────────────────────────┘
    
    # def trigger_arm(self):
    #     self.__trigger.clear()

    # def trigger_wait(self, timeout=5):
    #     if not self.__trigger.wait(timeout=timeout):
    #         raise RuntimeError(f"Timeout waiting for trigger for attribute {self.name} on {self.base_topic}")


    # ┌────────────────────────────────────────┐
    # │ Set/get                                │
    # └────────────────────────────────────────┘

    def get(self):
        return self.__value

    def set(self, v, ensure=False):
        # if ensure:
        #     self.trigger_arm()

        self.client.publish(self._topic_cmds_set, self.payload_factory(v))

        # if ensure:
        #     self.trigger_wait(timeout=5)

        #     if self.__value != v:
        #         raise RuntimeError(f"Attribute {self.name} for {self.base_topic}: cannot set to {v}, got {self.__value}")



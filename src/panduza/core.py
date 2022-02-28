import time
import json
import paho.mqtt.client as mqtt

class Core:
    """ Core class
    """

    # Store mqtt clients
    Clients = {}

    # Store aliases
    Aliases = {}

    # Store connections data
    Connections = {}

    ###########################################################################
    ###########################################################################

    def LoadAliases(connections=None, filepath=None):
        """ Load aliases from connections or json file with connections

        Args:
            connections (dict, optional): Connections as declared as dict
                {
                    "connection_1": {
                        "url": "localhost",
                        "port": 1883,
                        "interfaces": {
                            "foo1": "/topic/to/foo1",
                            "foo2": "/topic/to/foo2",
                        }
                    },
                    "connection_2": {
                        "url": "broker.online",
                        "port": 1883,
                        "interfaces": {
                            "foo3": "/topic/to/foo3",
                            "foo4": "/topic/to/foo4",
                        }
                    }
                }
                Defaults to Null.
            
            filepath (string, optional): File containing json connections declaration. Defaults to Null.
        """
        # Load connections
        if connections:
            Core.__LoadAliasesFromDict(connections)
        elif filepath:
            with open(filepath) as f:
                data = json.load(f)
                Core.__LoadAliasesFromDict(data)

        # # Reset clients
        # Core.__ResetClients()

    ###########################################################################
    ###########################################################################

    def __LoadAliasesFromDict(connections):
        """ Load aliases from a connections dict
        """
        for co in connections:
            # Load connection
            Core.Connections[co] = {
                "url": connections[co]["url"],
                "port": connections[co]["port"]
            }

            # Load aliases
            for it in connections[co]["interfaces"]:
                Core.Aliases[it] = {
                    "co": co,
                    "base_topic": connections[co]["interfaces"][it]
                }

    # ###########################################################################
    # ###########################################################################

    # def __ResetClients():
    #     """ Create mqtt clients from connections data
    #     """
    #     for co in Core.Connections:
    #         # Create the client
    #         client = mqtt.Client(userdata=co)
    #         client.on_message = Core.__on_message
    #         client.connect(Core.Connections[co]["url"], Core.Connections[co]["port"])
    #         client.loop_start()

    #         # Store the client
    #         Core.Clients[co] = {}
    #         Core.Clients[co]["obj"] = client
    #         Core.Clients[co]["interfaces"] = {}

    # ###########################################################################
    # ###########################################################################

    # def __on_message(client, userdata, msg):
    #     print("Connected with result code {msg.payload}", "\n")

    #     co = userdata
    #     print(userdata, "\n")
    #     for it in Core.Clients[co]["interfaces"]:
    #         it.on_mqtt_message(msg)

    ###########################################################################
    ###########################################################################

    def GetClient(alias):
        """
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")
        co = Core.Aliases[alias]["co"]

        # Get data from the connection
        if co not in Core.Connections.keys():
            raise Exception("Connection [" + co + "] not defined")

        # Create the client
        client = mqtt.Client(userdata=co)
        client.connect(Core.Connections[co]["url"], Core.Connections[co]["port"])

        # Get the client
        return client

    ###########################################################################
    ###########################################################################

    def GetBaseTopic(alias):
        """
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")

        return Core.Aliases[alias]["base_topic"]

    ###########################################################################
    ###########################################################################

    def GetClientAndBaseTopic(alias):
        """
        """
        return (Core.GetClient(alias), Core.GetBaseTopic(alias))




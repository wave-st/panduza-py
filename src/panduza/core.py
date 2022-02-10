import time
import json
import paho.mqtt.client as mqtt

class Core:
    """ Core class
    """

    Connections = {}

    Aliases = {}

    ###########################################################################
    ###########################################################################

    def LoadAliases(connections):
        """ Load connections
            @param connections
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

        # print(Core.Connections)
        # print(Core.Aliases)


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

        # Generate the new client
        client = mqtt.Client()
        client.connect(Core.Connections[co]["url"], Core.Connections[co]["port"])
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

    # ###########################################################################
    # ###########################################################################

    # def ScanInterfaces(co="*", timeout=2, filters=None):
    #     """
    #     """
    #     # Initialize scan infos
    #     scan_infos = []

    #     # Get the connections that must be scanned
    #     conns={}
    #     if "*" == co:
    #         conns = Core.Connections
    #     else:
    #         conns = {}
    #         conns[co] = Core.Connections[co]

    #     # For each connections scan and store panduza interfaces        
    #     for co in conns:
            
    #         def _on_message(client, userdata, msg):
    #             info = json.loads(msg.payload)

    #             append_flag = True
    #             if filters:
    #                 if info['type'] not in filters:
    #                     append_flag = False

    #             if append_flag:
    #                 scan_infos.append({
    #                     'topic': msg.topic[:-5], 'info': info
    #                 })

    #         client = mqtt.Client()
    #         client.on_message = _on_message
    #         client.connect(conns[co]['url'], conns[co]['port'], 60)
    #         client.subscribe("pza/+/+/+/info")

    #         t_end = time.time() + timeout
    #         while time.time() < t_end:
    #             client.loop()


    #     return scan_infos
        


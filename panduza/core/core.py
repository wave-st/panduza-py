import json

class Core:
    """Core object to share configuration data
    """

    # Store aliases
    Aliases = {}

    # Store connections data
    Connections = {}

    ###########################################################################
    ###########################################################################

    def LoadAliases(connections=None, filepath=None):
        """Load aliases from connections or json file with connections

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

    ###########################################################################
    ###########################################################################

    def __LoadAliasesFromDict(connections):
        """Load aliases from a connections dict
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

    ###########################################################################
    ###########################################################################

    def BrokerInfoFromBrokerAlias(alias):
        """Return the broker data from alias

        Args:
            alias (str): Broker alias

        Raises:
            Exception: raise if connection alias not loaded

        Returns:
            str, int: url, port
        """
        # Get data from the connection
        if alias not in Core.Connections.keys():
            raise Exception("Connection [" + alias + "] not defined")

        # Get the client
        return Core.Connections[alias]["url"], Core.Connections[alias]["port"]

    ###########################################################################
    ###########################################################################

    def BrokerInfoFromInterfaceAlias(alias):
        """
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")
        co = Core.Aliases[alias]["co"]

        # Get data from the connection
        if co not in Core.Connections.keys():
            raise Exception("Connection [" + co + "] not defined")

        # Get the client
        return Core.Connections[co]["url"], Core.Connections[co]["port"]

    ###########################################################################
    ###########################################################################

    def BaseTopicFromAlias(alias):
        """
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")

        return Core.Aliases[alias]["base_topic"]

    ###########################################################################
    ###########################################################################



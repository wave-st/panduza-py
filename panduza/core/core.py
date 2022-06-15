import json
import logging

# Create the logger for core events
CoreLog = logging.getLogger(f"pza.core")

# ┌────────────────────────────────────────┐
# │ AliasError                             │
# └────────────────────────────────────────┘

class AliasError(Exception):
    """Error that is raised when a error occurs on the alias management
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

# ┌────────────────────────────────────────┐
# │ Core                                   │
# └────────────────────────────────────────┘

class Core:
    """Core object to share configuration data
    """

    # Store aliases
    Aliases = {}

    # Store connections data
    Connections = {}

    ###########################################################################
    ###########################################################################

    def LoadAliases(connections=None, json_filepath=None):
        """Load aliases from connections OR json file with connections

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
            
            json_filepath (string, optional): File containing json connections declaration. Defaults to Null.
        """
        if connections:
            Core.__LoadAliasesFromDict(connections)
        elif json_filepath:
            Core.__LoadAliasesFromFile(json_filepath)

    ###########################################################################
    ###########################################################################

    def __LoadAliasesFromFile(json_filepath):
        """Load aliases from a json file
        """
        try:
            CoreLog.info(f"Load aliases from file : {json_filepath}")
            with open(json_filepath) as f:
                data = json.load(f)
                Core.__LoadAliasesFromDict(data)
        except json.decoder.JSONDecodeError as e:
            raise AliasError("File content is not json well formated")

    ###########################################################################
    ###########################################################################

    def __LoadAliasesFromDict(connections):
        """Load aliases from a connections dict
        """
        # Go through connections and sort them into internal attributes
        CoreLog.info(f"Load aliases from dict : {connections}")
        for co in connections:

            # Load connection
            CoreLog.info(f"   Load connection : {co}")
            Core.Connections[co] = {
                "url": connections[co]["url"],
                "port": connections[co]["port"]
            }

            # Load aliases
            for it in connections[co]["interfaces"]:
                CoreLog.info(f"      Load interface : {it}")
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
        """Return the broker information to reach reach the interface from its alias
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
        """Return the base topic of the interface from its alias
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")

        return Core.Aliases[alias]["base_topic"]

    ###########################################################################
    ###########################################################################


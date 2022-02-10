import os
import json
import appdirs
import argparse
import traceback

from pza_scan import Scanner
from pza_dio import DioController

appname = "panduza"
appauthor = "PanduzaTeam"
dirs = appdirs.AppDirs(appname, appauthor)



parser = argparse.ArgumentParser(description='Tools')
parser.add_argument('commands', nargs='+', default=[])
args = parser.parse_args()



# broker add show remove
# alias

if args.commands[0] == "broker":

    if args.commands[1] == "add":

        filepath = os.path.join(dirs.user_data_dir, "config.json")

        data={}
        try:
            with open(filepath, 'r') as f:
                content_= f.read()
                data = json.loads(content_)
                # print(data)
        except:
            pass
            
        if "brokers" not in data:
            data["brokers"] = {}

        name = args.commands[2]
        url  = args.commands[3]
        data["brokers"][name] = url

        os.makedirs(dirs.user_data_dir, exist_ok=True)

        f = open(filepath, "w+")
        f.write( json.dumps(data, indent=1) )
        f.close()

        print(">>>", filepath)
    
    if args.commands[1] == "show":

        filepath = os.path.join(dirs.user_data_dir, "config.json")
        data={}
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except:
            traceback.print_exc()
            
        if "brokers" not in data:
            data["brokers"] = {}

        print(data["brokers"])


elif args.commands[0] == "scan":

    filepath = os.path.join(dirs.user_data_dir, "config.json")

    data={}
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except:
        traceback.print_exc()
            
        
    if "brokers" not in data:
        data["brokers"] = {}

    scanner = Scanner()

    # For each connections scan and store panduza interfaces        
    for broker_name in data["brokers"]:
        scanner.load_broker(broker_name, data["brokers"][broker_name])

    try:
        scanner.run()
    except KeyboardInterrupt:
        scanner.stop()
        scanner.switchForm(None)
        


elif args.commands[0] == "dio":

    filepath = os.path.join(dirs.user_data_dir, "config.json")

    data={}
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except:
        traceback.print_exc()
            
        
    if "brokers" not in data:
        data["brokers"] = {}

    dio_controller = DioController()

    # For each connections scan and store panduza interfaces        
    for broker_name in data["brokers"]:
        dio_controller.load_broker(broker_name, data["brokers"][broker_name])

    try:
        dio_controller.run()
    except KeyboardInterrupt:
        dio_controller.stop()
        dio_controller.switchForm(None)



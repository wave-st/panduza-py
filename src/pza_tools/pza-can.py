#!/usr/bin/python3

import time
import logging
import argparse
import json

from pipe import Can, Core

###############################################################################
###############################################################################

def scan_and_let_user_select():
    """
    """
    print("SCAN in progress...")
    Core.LoadConnections({
        "c1": {
            "url": url,
            "port": port,
        },
    })
    scan_results = Core.ScanInterfaces()

    i = 0
    for s in scan_results:
        print("-- ", i, " :", s)
        i+=1

    index = input('Select interface\n')
    index = int(index)
    print(scan_results[index])

    return scan_results[index]['topic']

###############################################################################
###############################################################################

def display_data(url, port, topic):
    """
    """
    Core.LoadConnections({
        "c1": {
            "url": url,
            "port": port,
        },
    })
    Core.LoadAliases({
        "canBus": {
            "co": "c1",
            "base_topic": topic
        }
    })

    s = Can(alias="canBus")

    def _on_data(data):
        msg = json.loads(data)
        print(f"{hex(msg['canId'])[2:].zfill(3).upper()} [{msg['length']}] {' '.join(str(hex(x)[2:].zfill(2).upper()) for x in msg['payload'])}")

    s.read_loop(_on_data)

    while True:
        time.sleep(0.2)

###############################################################################
###############################################################################

def generate_data(url, port, topic):
    """
    """
    Core.LoadConnections({
        "c1": {
            "url": url,
            "port": port,
        },
    })
    Core.LoadAliases({
        "canBus": {
            "co": "c1",
            "base_topic": topic
        }
    })

    s = Can(alias="canBus")

    while True:
        s.write(0xAA, [1,2])
        time.sleep(0.1)

###############################################################################
###############################################################################

if __name__ == '__main__':
    # Manage arguments
    parser = argparse.ArgumentParser(description='Tool to perform a scan on panduza interfaces')
    parser.add_argument('-u', '--url', dest='url', help='URL of the broker')
    parser.add_argument('-p', '--port', dest='port', help='Port mqtt of the broker')
    parser.add_argument('-t', '--topic', dest='topic', help='Base topic of the serial port')
    parser.add_argument('-l', '--log', dest='enable_logs', action='store_true', help='start the logs')
    parser.add_argument('-d', '--display', dest='enable_display', action='store_true', help='display incomming serial data')
    parser.add_argument('-g', '--generate', dest='enable_generate', action='store_true', help='generate serial data')
    args = parser.parse_args()

    #
    if args.enable_logs:
        logging.basicConfig(level=logging.DEBUG)


    # Parse URL
    url = 'localhost'
    if args.url:
        url = args.url
        print("URL: ", args.url)

    # Parse PORT
    port = 1883
    if args.port:
        port = args.port
        print("port: ", args.port)

    # Topic
    topic = ""
    if args.topic:
        topic = args.topic
    if not args.topic:
        print("No interface topic selected")
        topic = scan_and_let_user_select()


    if args.enable_generate:
        generate_data(url, port, topic)

    if args.enable_display:
        display_data(url, port, topic)

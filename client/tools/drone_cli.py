#!/usr/bin/env python3

# CLI for interacting with drone.
from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import sys
import time
import json
import asyncio

from drone_client.drone_client import DroneClient
from auvsi_suas.client.client import AsyncClient
from auvsi_suas.proto.interop_api_pb2 import Telemetry
from google.protobuf import json_format
from mavlink_proxy import MavlinkProxy
from upload_odlcs import upload_odlcs

logger = logging.getLogger(__name__)

async def load_mission(args, client):
    interop_client = AsyncClient(args.interop_url,
                     args.interop_username,
                     args.interop_password)

    await client.load_mission(args.mission_id, interop_client)

def sendMission(args, client):
    interop_client = AsyncClient(args.interop_url,
                     args.interop_username,
                     args.interop_password)
    mission = interop_client.get_mission(args.mission_id).result()
    mission_json = json_format.MessageToJson(mission)
    mission_dictionary = json.loads(mission_json)
    print(mission_dictionary)

async def mission(client):
    await client.mission()
    return

def main():
        # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')

    # Parse command line args.
    parser = argparse.ArgumentParser(description='AUVSI SUAS Drone CLI.')
    parser.add_argument(
        '--url', required=True, help='URL for drone.')

    subparsers = parser.add_subparsers(help='Sub-command help.')

    subparser = subparsers.add_parser('mission', help='Send Mission.')
    subparser.set_defaults(func=mission)
    
    subparser = subparsers.add_parser('load_mission', help='Loads Mission.')
    subparser.set_defaults(func=load_mission)
    subparser.add_argument(
              '--mission_id',
              type=int,
              required=True,
              help='ID of the mission to get.')
    subparser.add_argument(
              '--interop_url',
              required=True,
              help='url for interop server')
    subparser.add_argument(
              '--interop_username',
              required=True,
              help='username for interop server')
    subparser.add_argument(
              '--interop_password',
              required=True,
              help='password for interop server')          
    
    args = parser.parse_args()

    #create client and send commands
    client = DroneClient(args.url)
    asyncio.run(args.func(client))

if __name__ == '__main__':
    main()
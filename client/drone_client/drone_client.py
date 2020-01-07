"""Core drone client module

This module provides a Python interface to the drone using mavsdk.
"""
import asyncio
import json

from auvsi_suas.client.exceptions import InteropError
from auvsi_suas.proto import interop_api_pb2
from concurrent.futures import ThreadPoolExecutor
from google.protobuf import json_format
from auvsi_suas.client.client import AsyncClient
from mavsdk import System
from mavsdk import (MissionItem)

class DroneClient():
    def __init__(self, args):
        self.drone = System()
        self.url = args.url

    async def connect(self):
        drone = System()
        await drone.connect(system_address=self.url)

    async def mission(self):
        drone = System()
        await drone.connect(system_address=self.url)

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered with UUID: {state.uuid}")
                break

        asyncio.ensure_future(self.print_mission_progress(drone))
        termination_task = asyncio.ensure_future(self.observe_is_in_air(drone))

        mission_items = []
        mission_items.append(MissionItem(47.398039859999997,
                                        8.5455725400000002,
                                        25,
                                        10,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan')))
        mission_items.append(MissionItem(47.398036222362471,
                                        8.5450146439425509,
                                        25,
                                        10,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan')))
        mission_items.append(MissionItem(47.397825620791885,
                                        8.5450092830163271,
                                        25,
                                        10,
                                        True,
                                        float('nan'),
                                        float('nan'),
                                        MissionItem.CameraAction.NONE,
                                        float('nan'),
                                        float('nan')))

        await drone.mission.set_return_to_launch_after_mission(True)

        print("-- Uploading mission")
        await drone.mission.upload_mission(mission_items)

        print("-- Arming")
        await drone.action.arm()

        print("-- Starting mission")
        await drone.mission.start_mission()

        await termination_task


    async def print_mission_progress(self, drone):
        async for mission_progress in drone.mission.mission_progress():
            print(f"Mission progress: "
                f"{mission_progress.current_item_index}/"
                f"{mission_progress.mission_count}")


    async def observe_is_in_air(self, drone):
        """ Monitors whether the drone is flying or not and
        returns after landing """

        was_in_air = False

        async for is_in_air in drone.telemetry.in_air():
            if is_in_air:
                was_in_air = is_in_air

            if was_in_air and not is_in_air:
                await asyncio.get_event_loop().shutdown_asyncgens()
                return

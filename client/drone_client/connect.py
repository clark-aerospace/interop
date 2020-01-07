#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk import (MissionItem)


async def connect(url):
    drone = System()
    await drone.connect(system_address=url)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
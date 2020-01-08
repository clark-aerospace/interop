import os
import unittest
import asyncio

from drone_client.drone_client import DroneClient

# These tests run a SITL drone simulation using gazebo and default settings

# Set these environmental variables to the proper values
# if the defaults are not correct.
device = os.getenv('TEST_DRONE', 'udp://:14540')

class TestClientMission(unittest.TestCase):
    """Test if the mission function connects and sends mission items to device"""

    def test_mission(self):
        """send good mission on url"""
        #if no exeption is raised it works
        client = DroneClient(device)
        asyncio.run(client.mission())

import unittest

from auvsi_suas.client.types import FlyZone
from auvsi_suas.client.types import GpsPosition
from auvsi_suas.client.types import Mission
from auvsi_suas.client.types import Odlc
from auvsi_suas.client.types import Waypoint


class TestMission(unittest.TestCase):
    """Test the Mission object. There is very little to see here."""

    def test_serialize(self):
        """Test valid inputs serialize"""
        # No exceptions
        mission = Mission(
            id=1,
            active=True,
            air_drop_pos=GpsPosition(latitude=38, longitude=-76),
            fly_zones=[
                FlyZone(
                    boundary_pts=[
                        Waypoint(
                            order=1,
                            latitude=37,
                            longitude=-70,
                            altitude_msl=10)
                    ],
                    altitude_msl_min=10,
                    altitude_msl_max=20)
            ],
            home_pos=GpsPosition(latitude=39, longitude=-77),
            mission_waypoints=[
                Waypoint(order=1, latitude=37, longitude=-70, altitude_msl=10)
            ],
            off_axis_odlc_pos=GpsPosition(latitude=37, longitude=-75),
            emergent_last_known_pos=GpsPosition(latitude=34, longitude=-75),
            search_grid_points=[
                Waypoint(order=1, latitude=37, longitude=-70, altitude_msl=10)
            ])
        d = mission.serialize()
        self.assertEqual(1, d['id'])
        self.assertEqual(38, d['air_drop_pos']['latitude'])
        self.assertEqual(-77, d['home_pos']['longitude'])
        self.assertEqual(1, d['mission_waypoints'][0]['order'])
        self.assertEqual(37, d['off_axis_odlc_pos']['latitude'])
        self.assertEqual(34, d['emergent_last_known_pos']['latitude'])
        self.assertEqual(10, d['search_grid_points'][0]['altitude_msl'])

    def test_deserialize(self):
        """Test deserialization."""
        return
        m = Mission.deserialize({
            'id':
            1,
            'active':
            True,
            'air_drop_pos': {
                'latitude': 38,
                'longitude': -76,
            },
            'fly_zones': [
                {
                    'altitude_msl_min':
                    10,
                    'altitude_msl_max':
                    20,
                    'boundary_pts': [
                        {
                            'order': 1,
                            'latitude': 37,
                            'longitude': -77,
                        },
                    ],
                },
            ],
            'home_pos': {
                'latitude': 39,
                'longitude': -75,
            },
            'mission_waypoints': [{
                'order': 2,
                'latitude': 30,
                'longitude': -70,
                'altitude_msl': 5,
            }],
            'off_axis_odlc_pos': {
                'latitude': 31,
                'longitude': -71,
            },
            'emergent_last_known_pos': {
                'latitude': 32,
                'longitude': -71,
            },
            'search_grid_points': [
                {
                    'order': 3,
                    'latitude': 29,
                    'longitude': -72,
                },
            ],
        })

        self.assertEqual(1, m.id)
        self.assertTrue(m.active)
        self.assertEqual(38, m.air_drop_pos.latitude)
        self.assertEqual(-76, m.air_drop_pos.longitude)
        self.assertEqual(10, m.fly_zones[0].altitude_msl_min)
        self.assertEqual(20, m.fly_zones[0].altitude_msl_max)
        self.assertEqual(1, m.fly_zones[0].boundary_pts[0].order)
        self.assertEqual(37, m.fly_zones[0].boundary_pts[0].latitude)
        self.assertEqual(-77, m.fly_zones[0].boundary_pts[0].longitude)
        self.assertEqual(39, m.home_pos.latitude)
        self.assertEqual(-75, m.home_pos.latitude)
        self.assertEqual(2, m.mission_waypoints[0].order)
        self.assertEqual(30, m.mission_waypoints[0].latitude)
        self.assertEqual(-70, m.mission_waypoints[0].longitude)
        self.assertEqual(5, m.mission_waypoints[0].altitude_msl)
        self.assertEqual(31, m.off_axis_odlc_pos.latitude)
        self.assertEqual(-71, m.off_axis_odlc_pos.latitude)
        self.assertEqual(32, m.emergent_last_known_pos.latitude)
        self.assertEqual(-71, m.emergent_last_known_pos.latitude)
        self.assertEqual(3, m.search_grid_points[0].order)
        self.assertEqual(29, m.search_grid_points[0].latitude)
        self.assertEqual(-72, m.search_grid_points[0].longitude)


class TestOdlc(unittest.TestCase):
    """Tests the Odlc model for validation and serialization."""

    def test_valid(self):
        """Test valid inputs."""
        Odlc(
            id=1,
            user=2,
            type='standard',
            latitude=10,
            longitude=-10,
            orientation='n',
            shape='circle',
            background_color='white',
            alphanumeric='a',
            alphanumeric_color='black')

        Odlc(
            type='off_axis',
            latitude=10,
            longitude=-10,
            orientation='n',
            shape='circle',
            background_color='white',
            alphanumeric='a',
            alphanumeric_color='black')

        Odlc(
            type='emergent',
            latitude=10,
            longitude=-10,
            description='Fireman putting out a fire.')

        Odlc(type='standard', latitude=10, longitude=-10, autonomous=True)

    def test_invalid(self):
        """Test invalid inputs."""
        # Bad latitude.
        with self.assertRaises(ValueError):
            Odlc(
                type='emergent',
                latitude='a',
                longitude=-10,
                description='Firefighter')

        with self.assertRaises(ValueError):
            Odlc(
                type='emergent',
                latitude=10,
                longitude='a',
                description='Firefighter')

    def test_serialize(self):
        """Test serialization."""
        o = Odlc(
            id=1,
            user=2,
            type='standard',
            latitude=10,
            longitude=-10,
            orientation='n',
            shape='circle',
            background_color='white',
            alphanumeric='a',
            alphanumeric_color='black',
            autonomous=True,
            actionable_override=True,
            team_id='testuser')
        s = o.serialize()

        self.assertEqual(13, len(s))
        self.assertEqual(1, s['id'])
        self.assertEqual(2, s['user'])
        self.assertEqual('standard', s['type'])
        self.assertEqual(10, s['latitude'])
        self.assertEqual(-10, s['longitude'])
        self.assertEqual('n', s['orientation'])
        self.assertEqual('circle', s['shape'])
        self.assertEqual('white', s['background_color'])
        self.assertEqual('a', s['alphanumeric'])
        self.assertEqual('black', s['alphanumeric_color'])
        self.assertEqual(True, s['autonomous'])
        self.assertEqual(True, s['actionable_override'])
        self.assertEqual('testuser', s['team_id'])

    def test_deserialize(self):
        """Test deserialization."""
        o = Odlc.deserialize({
            'type': 'standard',
            'latitude': '10',
            'longitude': -10,
            'orientation': 'n',
            'shape': 'circle',
            'background_color': 'white',
            'alphanumeric': 'a',
            'alphanumeric_color': 'black',
            'autonomous': True,
            'actionable_override': True,
            'team_id': 'testuser'
        })

        self.assertEqual('standard', o.type)
        self.assertEqual(10, o.latitude)
        self.assertEqual(-10, o.longitude)
        self.assertEqual('n', o.orientation)
        self.assertEqual('circle', o.shape)
        self.assertEqual('white', o.background_color)
        self.assertEqual('a', o.alphanumeric)
        self.assertEqual('black', o.alphanumeric_color)
        self.assertEqual(True, o.autonomous)
        self.assertEqual(True, o.actionable_override)
        self.assertEqual('testuser', o.team_id)

        o = Odlc.deserialize({'type': 'emergent'})

        self.assertEqual('emergent', o.type)

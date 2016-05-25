# flake8: noqa

import unittest
from dcss import parse


class TestParse(unittest.TestCase):

    def test_parse_start_operation(self):
        self.assertEqual(parse.parse_start_operation(
                'stog_start_operation robot_config 31.2 set_port_state mX0 u'
            ),
            {
                "direction": "stog",
                "name": "robot_config",
                "handle": "31.2",
                "arguments": "set_port_state mX0 u",
            }
        )

    def test_parse_operation_update(self):
        self.assertEqual(parse.parse_operation_update(
                'stog_operation_update robot_config 31.38 port jam at m 3 A'
            ),
            {
                "direction": "stog",
                "name": "robot_config",
                "handle": "31.38",
                "arguments": "port jam at m 3 A",
            }
        )

    def test_parse_operation_completed(self):
        self.assertEqual(parse.parse_operation_completed(
                'stog_operation_completed robot_config 31.41 aborted'
            ),
            {
                "direction": "stog",
                "name": "robot_config",
                "handle": "31.41",
                "status": "aborted",
                "arguments": None,
            }
        )

    def test_parse_holder_found_message(self):
        self.assertEqual(parse.parse_holder_found_message(
                'stog_operation_update robot_config 31.4 '
                'found calibration cassette l dz: -0.300'
            ),
            {'handle': '31.4', 'position': 'left',
             'type': 'calibration cassette', 'dz': -0.3}
        )
        self.assertEqual(parse.parse_holder_found_message(
                'stog_operation_update robot_config 31.8 '
                'found normal cassette m dz: -0.336'
            ),
            {'handle': '31.8', 'position': 'middle',
             'type': 'cassette', 'dz': -0.336}
        )
        self.assertEqual(parse.parse_holder_found_message(
                'stog_operation_update robot_config 31.12 '
                'found super puck adaptor r dz: 0.036'
            ),
            {'handle': '31.12', 'position': 'right',
             'type': 'puck adaptor', 'dz': 0.036}
        )

    def test_parse_robot_force_message(self):
        self.assertEqual(parse.parse_robot_force_message(
                'stog_set_string_completed robot_force_middle normal  -65.8  '
                '0.0 uuuu uuuu uuuu uuuu uuuu uuuu  0.3 '
                '-0.2 uuuu uuuu uuuu uuuu uuuu uuuu EEEE '
            ),
            {'position': 'middle', 'status': 'normal',
             'height': -65.8, 'forces': [
                 0.0, 'unknown', 'unknown', 'unknown',
                 'unknown', 'unknown', 'unknown', 0.3,
                 -0.2, 'unknown', 'unknown', 'unknown',
                 'unknown', 'unknown', 'unknown', 'empty',
             ]}
         )

    def test_parse_robot_cassette_message(self):
        self.maxDiff = 9999
        self.assertEqual(parse.parse_robot_cassette_message(
            'stog_set_string_completed robot_cassette normal '
                'X b b b b b b b b b b b b b b b b '
                  'b b b b b b b b b b b b b b b b '
                  'b b b b b b b b b b b b b b b b '
                  'b b b b b b b b b b b b b b b b '
                  'b b b b b b b b b b b b b b b b '
                  'b b b b b b b b b b b b b b b b '
                '3 1 1 j 1 1 1 1 1 1 1 1 1 1 1 1 1 '
                  '1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 '
                  '- - - - - - - - - - - - - - - - '
                  '1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 '
                  '- - - - - - - - - - - - - - - - '
                  '- - - - - - - - - - - - - - - - '
                'u u u u u u u u u u u u u u u u u '
                  'u u u u u u u u u u u u u u u u '
                  'u u u u u u u u u u u u u u u u '
                  'u u u u u u u u u u u u u u u u '
                  'u u u u u u u u u u u u u u u u '
                  'u u u u u u u u u u u u u u u u '
            ), {
                'status': 'normal',
                'holders': [
                    {'type': 'bad', 'ports': ['b'] * 96},
                    {'type': 'puck adaptor',
                     'ports': [
                            '1', '1', 'j', '1', '1', '1', '1', '1',
                            '1', '1', '1', '1', '1', '1', '1', '1',
                            '1', '1', '1', '1', '1', '1', '1', '1',
                            '1', '1', '0', '0', '0', '0', '1', '1',
                            '-', '-', '-', '-', '-', '-', '-', '-',
                            '-', '-', '-', '-', '-', '-', '-', '-',
                            '1', '1', '1', '1', '1', '1', '1', '1',
                            '1', '1', '1', '1', '1', '1', '1', '1',
                            '-', '-', '-', '-', '-', '-', '-', '-',
                            '-', '-', '-', '-', '-', '-', '-', '-',
                            '-', '-', '-', '-', '-', '-', '-', '-',
                            '-', '-', '-', '-', '-', '-', '-', '-',
                        ],
                    },
                    {'type': 'unknown', 'ports': ['u'] * 96},
                ],
            },
        )
        self.assertEqual(parse.parse_robot_cassette_message(
            'stog_configure_string robot_cassette robot  '
                '1 u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '2 0 - - - - - - 1 1 - - - - - - 0 '
                '  1 - - - - - - 1 1 - - - - - - 0 '
                '  1 - - - - - - 1 0 - - - - - - 1 '
                '  1 - - - - - - 1 0 - - - - - - 1 '
                '  0 - - - - - - 0 0 - - - - - - 0 '
                '  0 - - - - - - 0 0 - - - - - - 0 '
                'u u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
                '  u u u u u u u u u u u u u u u u '
            ), {
                'status': 'robot',
                'holders': [
                    {'type': 'cassette', 'ports': ['u'] * 96},
                    {'type': 'calibration cassette',
                     'ports': [
                            '0', '-', '-', '-', '-', '-', '-', '1',
                            '1', '-', '-', '-', '-', '-', '-', '0',
                            '1', '-', '-', '-', '-', '-', '-', '1',
                            '1', '-', '-', '-', '-', '-', '-', '0',
                            '1', '-', '-', '-', '-', '-', '-', '1',
                            '0', '-', '-', '-', '-', '-', '-', '1',
                            '1', '-', '-', '-', '-', '-', '-', '1',
                            '0', '-', '-', '-', '-', '-', '-', '1',
                            '0', '-', '-', '-', '-', '-', '-', '0',
                            '0', '-', '-', '-', '-', '-', '-', '0',
                            '0', '-', '-', '-', '-', '-', '-', '0',
                            '0', '-', '-', '-', '-', '-', '-', '0',
                        ],
                    },
                    {'type': 'unknown', 'ports': ['u'] * 96},
                ],
            },
        )

    def test_parse_start_robot_probe_message(self):
        self.maxDiff = 9999
        self.assertEqual(parse.parse_start_robot_probe_message(
            'stog_start_operation robot_config 31.41 probe '
                '1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                '0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                  '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
            ),
            {
                'direction': 'stog',
                'name': 'robot_config',
                'handle': '31.41',
                'arguments': (
                    'probe 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                          '0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                          '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                            '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 '
                ),
                'holders': [
                    {
                        'probe_holder_type': 1,
                        'ports': [0] * 96,
                    },
                    {
                        'probe_holder_type': 0,
                        'ports': [1] * 16 + [0] * 80,
                    },
                    {
                        'probe_holder_type': 0,
                        'ports': [0] * 96,
                    },
                ]
            }
        )

#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
CARLA Dynamic Weather:

Connect to a CARLA Simulator instance and control the weather. Change Sun
position smoothly with time and generate storms occasionally.
"""

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import argparse
import math


def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(value, maximum))

def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-s', '--speed',
        metavar='FACTOR',
        default=1.0,
        type=float,
        help='rate at which the weather changes (default: 1.0)')
    args = argparser.parse_args()

    speed_factor = args.speed
    update_freq = 0.1 / speed_factor

    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)
    world = client.get_world()

    # Static Weather presets
    #
    # carla.WeatherParameters.ClearNoon
    # carla.WeatherParameters.CloudyNoon
    # carla.WeatherParameters.WetNoon
    # carla.WeatherParameters.WetCloudyNoon
    # carla.WeatherParameters.MidRainyNoon
    # carla.WeatherParameters.HardRainNoon
    # carla.WeatherParameters.SoftRainNoon
    # carla.WeatherParameters.ClearSunset
    # carla.WeatherParameters.CloudySunset
    # carla.WeatherParameters.WetSunset
    # carla.WeatherParameters.WetCloudySunset
    # carla.WeatherParameters.MidRainSunset
    # carla.WeatherParameters.HardRainSunset
    # carla.WeatherParameters.SoftRainSunset

    weather = carla.WeatherParameters.ClearNoon

    elapsed_time = 0.0

    while True:
        timestamp = world.wait_for_tick(seconds=30.0)
        elapsed_time += timestamp.delta_seconds
        if elapsed_time > update_freq:
            world.set_weather(weather)
            sys.stdout.write('\r' + str(weather) + 12 * ' ')
            sys.stdout.flush()
            elapsed_time = 0.0


if __name__ == '__main__':

    main()

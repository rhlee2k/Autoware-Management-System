#!/usr/bin/env python
# coding: utf-8

import json
import Geohash
from numpy import array as np_array


class Waypoint(object):
    GEOHASH_PRECISION = 15

    def __init__(self):
        self.__waypoints = {}

    def load(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            self.set_waypoints(data["waypoints"])
        return True

    def connect_to_redis(self, _host, _port, _dbname):
        return self

    def set_waypoints(self, waypoints):
        self.__waypoints = dict(map(
            lambda x: (x[0], {
                "waypoint_id": x[1]["waypointID"],
                "geohash": Geohash.encode(
                    float(x[1]["lat"]), float(x[1]["lng"]), precision=Waypoint.GEOHASH_PRECISION),
                "position": np_array([x[1]["x"], x[1]["y"], x[1]["z"]]),
                "yaw": x[1]["yaw"]
            }),
            waypoints.items()))

    def get_waypoint_ids(self):
        return list(self.__waypoints.keys())

    def get_latlng(self, waypoint_id):
        return Geohash.decode(self.__waypoints[waypoint_id]["geohash"])

    def get_geohash(self, waypoint_id):
        return self.__waypoints[waypoint_id]["geohash"]

    def get_position(self, waypoint_id):
        return self.__waypoints[waypoint_id]["position"]

    def get_xyz(self, waypoint_id):
        return self.__waypoints[waypoint_id]["position"].data[:]

    def get_yaw(self, waypoint_id):
        return self.__waypoints[waypoint_id]["yaw"]

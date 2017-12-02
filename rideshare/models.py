""" All models for rideshare service """
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import hashlib
import time
# from django.db import models

class Driver(object):
    """ A Driver object in rideshare service.
    NOT A Django Model.
     """
    def __init__(self, vehicle_name, vehicle_number, **kwargs):
        """
        vehicle_name: vehicle company and model name
        vehicle_number: vehicle unique number
        **kwargs: all driver related info
        """
        self.info = kwargs
        self.vehicle_name = vehicle_name
        self.vehicle_number = vehicle_number

    def serialize(self):
        """
        Serializes an object to json format
        """
        response = dict()
        for key, value in self.__dict__.items():
            try:
                assert isinstance(value) == str
                response[key] = value
            except AssertionError:
                raise AttributeError("key:{} not serializable".format(key))
       
        return response


class Ride(object):
    """ A Ride object to represent a ride in rideshare service. """
    def __init__(self, uid, driver, seats, seats_available):
        if uid is None:
            self.uid = hashlib.sha256(str(time.time())).hexdigest()
        self.uid = uid
        self.driver = driver
        self.seats = seats
        self.seats_available = seats_available
        self.riders = []

    def add_rider(self, rider_id):
        """
        Adds a new rider to a ride
        """
        if self.seats_available < self.seats:
            self.riders.append(rider_id)
            return True
        return False
    
    def serialize(self):
        """
        Serializes an object to json format
        """
        response = {
            'uid': self.uid,
            'driver': self.driver.serialize(),
            'seats': self.seats,
            'seats_available': self.seats_available,
            'riders': self.riders}
        try:
            return json.dumps(response)
        except AttributeError:
            raise Exception("serialization error")

    @staticmethod
    def get_ride(uid):
        """
        looks up the ride by the uid
        """
        pass

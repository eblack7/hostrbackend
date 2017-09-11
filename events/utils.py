# All Uitlities will be in this .py file

#imports
from django.core import serializers
import json
from users.models import User
from datetime import datetime
#CONSTANTS
DATE_FORMATTER = "%Y-%m-%d %H:%M:%S +0000"

class EventSerializer():
    @staticmethod
    def serialize(event=None):
        if event is None:
            return None

        if hasattr(event, '__iter__') is False:
            #its a single object
            output = dict()
            output['id'] = event.pk
            output['event_name'] = str(event.event_name)
            output['hoster'] = json.loads(serializers.serialize("json", [User.objects.get(pk=event.hoster)])[1:-1])
            output['from_timestamp'] = datetime.strftime(event.from_timestamp, DATE_FORMATTER)
            output['to_timestamp'] = datetime.strftime(event.to_timestamp, DATE_FORMATTER)
            output['price'] = float(event.price)
            output['currency'] = str(event.currency)
            output['address'] = str(event.address)
            output['attending'] = int(event.attending)
            output['latitude'] = float(event.latitude)
            output['longitude'] = float(event.longitude)
            output['is_private'] = event.is_private
            output['event_image_url'] = str(event.event_image_url)
            output['created_at'] = datetime.strftime(event.created_at, DATE_FORMATTER)
            return json.dumps(output)

        output_list = []
        events = event
        del event
        for event in events:
            output = dict()
            output['id'] = event.pk
            output['event_name'] = str(event.event_name)
            output['hoster'] = json.loads(serializers.serialize("json", [User.objects.get(pk=event.hoster.id)])[1:-1])
            output['from_timestamp'] = datetime.strftime(event.from_timestamp, DATE_FORMATTER)
            output['to_timestamp'] = datetime.strftime(event.to_timestamp, DATE_FORMATTER)
            output['price'] = float(event.price)
            output['currency'] = str(event.currency)
            output['address'] = str(event.address)
            output['attending'] = int(event.attending)
            output['latitude'] = float(event.latitude)
            output['longitude'] = float(event.longitude)
            output['is_private'] = event.is_private
            output['event_image_url'] = str(event.event_image_url)
            output['created_at'] = datetime.strftime(event.create_at, DATE_FORMATTER)
            output_list.append(output)
        return json.dumps(output_list)

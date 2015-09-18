from django.forms import widgets
from rest_framework import serializers
from sensortag.models import SensorTag, SensorData

class SensorTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SensorTag
        fields = ('mac_address',
                  'slug',
                  'description')

class SensorTagDetailSerializer(serializers.ModelSerializer):
    sensortags = SensorTagSerializer(many=True, read_only=True)
    class Meta:
        model = SensorData
        fields = ('sensortags',
                  'time_recorded',
                  'ir_temp',
                  'ambient_temp',
                  'humidity',
                  'lux',)
    
class SensorDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SensorData
        fields = ('time_recorded',
                  'ir_temp',
                  'ambient_temp',
                  'humidity',
                  'lux',)
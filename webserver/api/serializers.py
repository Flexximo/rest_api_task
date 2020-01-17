from rest_framework import serializers
from .models import Car
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["car_id", "color", "manufacturer", "price", "year"] 

class ResponseSerializer(serializers.Serializer):
        status = serializers.CharField(max_length=36)
        info = serializers.CharField(max_length=64)
        created = serializers.DateTimeField()
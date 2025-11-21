from rest_framework import serializers
from .models import Geladinho


class GeladinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geladinho
        fields = '__all__'

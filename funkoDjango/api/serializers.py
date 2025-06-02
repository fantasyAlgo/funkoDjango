from rest_framework import serializers
from mainApp.models import FunkoPop

class FunkoPopSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunkoPop
        fields = "__all__"

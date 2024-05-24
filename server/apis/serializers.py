from rest_framework import serializers
from .models import users_collection

class UsersCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_collection
        fields = '__all__'


from rest_framework import serializers
from .models import Device, UsageSession, Accessory
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class AccessorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Accessory
    fields = '__all__'
    # read_only_fields = ('device',)

class DeviceSerializer(serializers.ModelSerializer):
    usage_sessions_today = serializers.SerializerMethodField()
    accessories = AccessorySerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Device
        fields = '__all__'

    def get_usage_sessions_today(self, obj):
        return obj.usage_sessions_today()

class UsageSessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = UsageSession
    fields = '__all__'
    read_only_fields = ('device',)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Device, UsageSession, Accessory
from .serializers import DeviceSerializer, UsageSessionSerializer, AccessorySerializer, UserSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the electronics-collector api home route!'}
    return Response(content)
  
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
  

class DeviceList(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = DeviceSerializer

  def get_queryset(self):
      # This ensures we only return cats belonging to the logged-in user
      user = self.request.user
      return Device.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created cat with the logged-in user
      serializer.save(user=self.request.user)

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = DeviceSerializer
  lookup_field = 'id'

  # add (override) the retrieve method below
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    # Get the list of toys not associated with this cat
    accessories_not_associated = Accessory.objects.exclude(id__in=instance.accessories.all())
    accessories_serializer = AccessorySerializer(accessories_not_associated, many=True)

    return Response({
        'device': serializer.data,
        'accessories_not_associated': accessories_serializer.data
    })
  
    def get_queryset(self):
      user = self.request.user
      return Device.objects.filter(user=user)
    
    def perform_update(self, serializer):
      device = self.get_object()
      if device.user != self.request.user:
          raise PermissionDenied({"message": "You do not have permission to edit this device."})
      serializer.save()

    def perform_destroy(self, instance):
      if instance.user != self.request.user:
          raise PermissionDenied({"message": "You do not have permission to delete this device."})
      instance.delete()

class UsageSessionListCreate(generics.ListCreateAPIView):
  serializer_class = UsageSessionSerializer

  def get_queryset(self):
    Device_id = self.kwargs['Device_id']
    return UsageSession.objects.filter(Device_id=Device_id)

  def perform_create(self, serializer):
    Device_id = self.kwargs['Device_id']
    Device = Device.objects.get(id=Device_id)
    serializer.save(Device=Device)

class UsageSessionDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = UsageSessionSerializer
  lookup_field = 'id'

  def get_queryset(self):
    device_id = self.kwargs['device_id']
    return UsageSession.objects.filter(device_id=device_id)
  
class AccessoryListCreate(generics.ListCreateAPIView):
  serializer_class = AccessorySerializer

  def get_queryset(self):
    Device_id = self.kwargs['Device_id']
    return Accessory.objects.filter(Device_id=Device_id)

  def perform_create(self, serializer):
    Device_id = self.kwargs['Device_id']
    Device = Device.objects.get(id=Device_id)
    serializer.save(Device=Device)

class AccessoryDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = AccessorySerializer
  lookup_field = 'id'

  def get_queryset(self):
    device_id = self.kwargs['device_id']
    return Accessory.objects.filter(device_id=device_id)
  
class AddAccessoryToDevice(APIView):
  def post(self, request, device_id, accessory_id):
    device = Device.objects.get(id=device_id)
    accessory = Accessory.objects.get(id=accessory_id)
    device.accessories.add(accessory)
    return Response({'message': f'Accessory {accessory.name} added to Device {device.name}'})
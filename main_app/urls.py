from django.urls import path
# import Home view from the views file
from .views import Home, DeviceList, DeviceDetail, UsageSessionListCreate, UsageSessionDetail, CreateUserView, LoginView, VerifyUserView, AccessoryListCreate, AccessoryDetail, AddAccessoryToDevice

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  path('devices/', DeviceList.as_view(), name='device-list'),
  path('devices/<int:id>/', DeviceDetail.as_view(), name='device-detail'),
	path('devices/<int:device_id>/usage/', UsageSessionListCreate.as_view(), name='feeding-list-create'),
	path('devices/<int:device_id>/usage/<int:id>/', UsageSessionDetail.as_view(), name='feeding-detail'),
  path('devices/<int:device_id>/add_accessory/<int:accessory_id>/', AddAccessoryToDevice.as_view(), name='add-accessory-to-device'),
  path('accessories/', AccessoryListCreate.as_view(), name='accessory-list-create'),
	path('accessories/<int:id>/', AccessoryDetail.as_view(), name='accessory-detail'),
]
from django.urls import path
from .views import Detection_Photo,Detection_Video,Detection_Thermal

urlpatterns = [
    path('detection_mask_photo/', Detection_Photo.as_view(), name = 'detection_photo'),
    path('detection_mask_video/', Detection_Video.as_view(), name = 'detection_video'),
    path('detection_mask_temp/', Detection_Thermal.as_view(), name = 'detection_mask_temp'),
]
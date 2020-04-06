from django.urls import path
from .views import ProfileList, ProfileDetail

urlpatterns = [
    path('v1/profiles', ProfileList.as_view(), name="profile_list"),
    path('v1/profile/<int:pk>', ProfileDetail.as_view(), name="profile_detail")
]
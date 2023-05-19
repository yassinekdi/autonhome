from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('sensors/', views.SensorList.as_view(), name='sensor_list'),
    path('sensors/<int:pk>/', views.SensorDetail.as_view(), name='sensor_detail'),
    path('measures/', views.MeasureList.as_view(), name='measure_list'),
    path('measures/<int:pk>/', views.MeasureDetail.as_view(), name='measure_detail'),
    path('events/', views.CalendarEventList.as_view(), name='event_list'),
    path('events/<int:pk>/', views.CalendarEventDetail.as_view(), name='event_detail'),
    # API Token Authentification
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # User authentification
    path('api/auth/', include('dj_rest_auth.urls')),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]

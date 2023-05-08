from django.urls import path
from . import views

urlpatterns = [
    path('sensors/', views.SensorList.as_view(), name='sensor_list'),
    path('sensors/<int:pk>/', views.SensorDetail.as_view(), name='sensor_detail'),
    path('measures/', views.MeasureList.as_view(), name='measure_list'),
    path('measures/<int:pk>/', views.MeasureDetail.as_view(), name='measure_detail'),
    path('events/', views.CalendarEventList.as_view(), name='event_list'),
    path('events/<int:pk>/', views.CalendarEventDetail.as_view(), name='event_detail'),
    # URLs d'authentification
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

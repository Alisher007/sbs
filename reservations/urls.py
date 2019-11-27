from django.urls import path
from reservations import views

app_name= 'reservation'
urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/list/', views.reservation_list2, name='list'),
    path('reservation/list/<str:date>/', views.reservation_list_date, name='list_date'),
    path('reservation/update/', views.reservation_update, name='update'),
    path('reservation/detail/', views.reservation_detail, name='detail'),
    path('reservation/delete/', views.reservation_delete, name='delete'),
]
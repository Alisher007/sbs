from django.urls import path
from customers import views

app_name= 'customers'
urlpatterns = [
    path('', views.customer_list, name='list'),
    path('add/', views.customer_add, name='add'),
    path('detail/', views.customer_detail, name='detail'),
    path('delete/<int:id>/', views.customer_delete, name='delete'),
]
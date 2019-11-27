from django.urls import path
from products import views

app_name= 'products'
urlpatterns = [
    path('', views.product_list, name='list'),
    path('add/', views.product_add, name='add'),
    path('detail/', views.product_detail, name='detail'),
    path('delete/<int:id>/', views.product_delete, name='delete'),
]
from django.urls import path
from rest_framework import routers

from apps.order import views

router = routers.SimpleRouter()

# router.register('<str:account>', views.OrderView)

urlpatterns = [path(r'<str:account_name>/', views.OrderView.as_view({'get': 'list', 'post': 'create'})),
    path(r'<str:account_name>/<int:pk>/', views.OrderView.as_view({'get': 'retrieve', 'delete': 'destroy'})), ]

urlpatterns += router.urls

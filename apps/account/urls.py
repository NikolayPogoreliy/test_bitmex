from rest_framework import routers

from apps.account import views

router = routers.SimpleRouter()

router.register('', views.AccountView)

urlpatterns = []

urlpatterns += router.urls

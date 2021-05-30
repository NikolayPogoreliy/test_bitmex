from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from apps.account.models import Account
from apps.account.serializers import AccountSerializer


class AccountView(viewsets.ModelViewSet):
    """
    Viewset for account management
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    debug_permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_permissions(self):
        if settings.get('DEBUG'):
            permission_classes = self.debug_permission_classes
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

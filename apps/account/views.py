from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.account.models import Account
from apps.account.serializers import AccountSerializer


class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)

# banking/views.py

from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    # @action(detail=True, methods=['get'])
    # def transactions(self, request, pk=None):
    #     account = self.get_object()
    #     transactions = account.transactions.all()
    #     serializer = TransactionSerializer(transactions, many=True)
    #     return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

# TODO stale byt odhlaseny po ukonceni sessionu
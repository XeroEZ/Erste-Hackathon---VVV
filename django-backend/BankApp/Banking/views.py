# banking/views.py
from rest_framework import viewsets
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        account = self.get_object()
        transactions = account.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
# TODO stale byt odhlaseny po ukonceni sessionu
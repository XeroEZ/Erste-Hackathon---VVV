<<<<<<< HEAD
# Banking/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

=======
# banking/views.py

from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
>>>>>>> fd9e7b8f571011a4d79ce3b6ece6b9a257f50c66
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

<<<<<<< HEAD
    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """Získaj všetky transakcie pre konkrétny účet."""
        account = self.get_object()
        transactions = account.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
=======

    # @action(detail=True, methods=['get'])
    # def transactions(self, request, pk=None):
    #     account = self.get_object()
    #     transactions = account.transactions.all()
    #     serializer = TransactionSerializer(transactions, many=True)
    #     return Response(serializer.data)
>>>>>>> fd9e7b8f571011a4d79ce3b6ece6b9a257f50c66


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
<<<<<<< HEAD
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
=======
    permission_classes = [permissions.IsAuthenticated]

# TODO stale byt odhlaseny po ukonceni sessionu
>>>>>>> fd9e7b8f571011a4d79ce3b6ece6b9a257f50c66

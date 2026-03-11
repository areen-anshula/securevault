from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Organization, CustomUser, Wallet, Transaction
from .serializers import OrganizationSerializer, CustomUserSerializer, WalletSerializer, TransactionSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(maker=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):

        tx = self.get_object()

        if tx.state != Transaction.Status.PENDING:
            return Response({"error": "Only pending transactions can be approved."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if tx.maker == request.user:
            return Response({"error": "You cannot approve your own transaction."}, 
                            status=status.HTTP_403_FORBIDDEN)

        if request.user.role not in ['CHECKER', 'ADMIN']:
            return Response({"error": "You do not have permission to approve transactions."}, 
                            status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic():
                wallet = tx.wallet
                
                if wallet.balance < tx.amount:
                    return Response({"error": "Insufficient funds in the wallet."}, 
                                    status=status.HTTP_400_BAD_REQUEST)

                wallet.balance -= tx.amount
                wallet.save()

                tx.state = Transaction.Status.APPROVED
                tx.checker = request.user
                tx.save()

            return Response({"message": "Transaction approved and funds deducted successfully."}, 
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "System error during transaction execution."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]    

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]    
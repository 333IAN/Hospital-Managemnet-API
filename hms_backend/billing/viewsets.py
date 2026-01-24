from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice, Payment, InvoiceItem, PaymentMode
from .serializers import InvoiceSerializer, PaymentSerializer, InvoiceItemSerializer, PaymentModeSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class=InvoiceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    def get_queryset(self):
        user=self.request.user
        if user.role=='PATIENT':
            return Invoice.objects.filter(patient__user=user)
        return Invoice.objects.all()
    
    @action(detail=True, methods=['post'], url_path= 'add-item')
    def add_item(self, request, pk=None):
        invoice=self.get_object()
        serializer=InvoiceItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invoice=invoice)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='pay')
    def record_payment(self, request, pk=None):
        invoice=self.get_object()
        serializer=PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invoice=invoice, recorded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PaymentModeViewSet(viewsets.ModelViewSet):
    queryset=PaymentMode.objects.all()
    serializer_class=PaymentModeSerializer
    permission_classes=[permissions.IsAuthenticated]



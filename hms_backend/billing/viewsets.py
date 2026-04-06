from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Invoice, Payment, InvoiceItem, PaymentMode
from .serializers import InvoiceSerializer, PaymentSerializer, InvoiceItemSerializer, PaymentModeSerializer
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from decimal import Decimal


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

    @action(detail=True, methods=['post'], url_path='record-payment')
    def record_payment(self, request, pk=None):
        invoice=self.get_object()
        amount_paid=request.data.get('amount')
        method=request.data.get('payment_method', 'Cash')



        if not amount_paid:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payment_obj=PaymentMode.objects.get(name=method)
            amount_decimal=Decimal(str(amount_paid))
            Payment.objects.create(
                invoice=invoice,
                amount=amount_decimal,
                payment_mode=payment_obj
            )

            invoice.update_totals()

            return Response({
                "message": "Payment recorded successfully",
                "current_paid": float(invoice.paid_amount),
                "remaining_balance": float(invoice.get_balance),
                "status": invoice.status
            }, status=status.HTTP_200_OK)
        
        except PaymentMode.DoesNotExist:
            return Response({'error': f"Payment mode '{method}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer=PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(invoice=invoice, recorded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='download-pdf')
    def download_pdf(self, request, pk=None):
        invoice=self.get_object()
        html_string=render_to_string('invoice_pdf.html', {'invoice': invoice})

        html=HTML(string=html_string)
        result=html.write_pdf()

        response=HttpResponse(content_type='application/pdf;')
        response['Content-Disposition']=f'inline; filename=invoice_{invoice.id}.pdf'
        response['Content-Transfer-Encoding']='binary'

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output=open(output.name, 'rb')
            response.write(output.read())
        return response
    
class PaymentModeViewSet(viewsets.ModelViewSet):
    queryset=PaymentMode.objects.all()
    serializer_class=PaymentModeSerializer
    permission_classes=[permissions.IsAuthenticated]



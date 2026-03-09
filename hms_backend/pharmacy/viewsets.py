from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

class MedicationViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['post'], url_path='restock')
    def restock(self, request, pk=None):
        medication = self.get_object()
        quantity = request.data.get('quantity')
        batch = request.data.get('batch_number', f"BAT-{timezone.now().strftime('%Y%m%d')}")
        expiry = request.data.get('expiry_date')

        if not quantity:
            return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

        PharmacyStock.objects.create(
            medication=medication,
            quantity=quantity,
            batch_number=batch,
            expiry_date=expiry
        )
        
        return Response({
            "status": "Stock replenished",
            "medication": medication.name,
            "added_quantity": quantity
        }, status=status.HTTP_201_CREATED)
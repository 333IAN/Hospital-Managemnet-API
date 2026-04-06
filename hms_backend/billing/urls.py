from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import InvoiceViewSet, PaymentModeViewSet

router=DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('payment-modes', PaymentModeViewSet, basename='payment-mode')

urlpatterns=[
    path('', include(router.urls)),
]

from django.shortcuts import render


from rest_framework import viewsets
from .models import (
    Customer, Product, Category, Quotation, QuotationItem, Invoice, InvoiceItem,
    CashSale, CashSaleItem, Receipt
)
from .serializers import (
    CustomerSerializer, ProductSerializer, CategorySerializer,
    QuotationSerializer, InvoiceSerializer, CashSaleSerializer, ReceiptSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class QuotationViewSet(viewsets.ModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class CashSaleViewSet(viewsets.ModelViewSet):
    queryset = CashSale.objects.all()
    serializer_class = CashSaleSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

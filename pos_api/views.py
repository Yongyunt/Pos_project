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
from rest_framework.decorators import action


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

    @action(detail=True, methods=['post'])
    def convert_to_receipt(self, request, pk=None):
        quotation = self.get_object()

        # เช็คว่ามี Receipt จากใบเสนอราคานี้ไปแล้วหรือยัง
        if hasattr(quotation, 'receipts') and quotation.receipts.exists():
            return Response({'detail': 'ใบเสนอราคานี้ถูกแปลงเป็นใบเสร็จแล้ว'}, status=status.HTTP_400_BAD_REQUEST)

        # สร้าง Receipt ใหม่
        receipt = Receipt.objects.create(
            quotation=quotation,
            customer=quotation.customer,
            receipt_date=timezone.now(),
            total_amount=quotation.total_amount,
            payment_method='cash',  # หรือให้ client ส่งมาก็ได้
        )

        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class CashSaleViewSet(viewsets.ModelViewSet):
    queryset = CashSale.objects.all()
    serializer_class = CashSaleSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

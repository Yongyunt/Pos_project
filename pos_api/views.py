from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Customer, Product, Category, Quotation, QuotationItem, Invoice, InvoiceItem,
    CashSale, CashSaleItem, Receipt, ReceiptItem
)
from .serializers import (
    CustomerSerializer, ProductSerializer, CategorySerializer,
    QuotationSerializer, InvoiceSerializer, CashSaleSerializer, ReceiptSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

@action(detail=True, methods=['post'])
def convert_to_receipt(self, request, pk=None):
    quotation = self.get_object()

    if quotation.customer is None:
        return Response({'detail': 'ใบเสนอราคานี้ยังไม่มีลูกค้า กรุณาเพิ่มลูกค้าก่อนแปลง'}, status=status.HTTP_400_BAD_REQUEST)

    # สร้าง Receipt
    receipt = Receipt.objects.create(
        quotation=quotation,
        customer=quotation.customer,
        receipt_date=timezone.now(),
        total_amount=quotation.total_amount,
        payment_method='cash',
    )

    # ดึงรายการสินค้าในใบเสนอราคา
    quotation_items = QuotationItem.objects.filter(quotation=quotation)

    # ก๊อปปี้ QuotationItem → ReceiptItem
    for item in quotation_items:
        ReceiptItem.objects.create(
            receipt=receipt,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )

    serializer = ReceiptSerializer(receipt)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

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

        if quotation.customer is None:
            return Response({'detail': 'ใบเสนอราคานี้ยังไม่มีลูกค้า กรุณาเพิ่มลูกค้าก่อนแปลง'}, status=status.HTTP_400_BAD_REQUEST)

        # สร้างใบเสร็จ
        receipt = Receipt.objects.create(
            quotation=quotation,
            customer=quotation.customer,
            receipt_date=timezone.now(),
            total_amount=quotation.total_amount,
            payment_method='cash',
        )

        # ดึงรายการจาก QuotationItem
        quotation_items = QuotationItem.objects.filter(quotation=quotation)

        # คัดลอก QuotationItem ไปเป็น ReceiptItem
        for item in quotation_items:
            ReceiptItem.objects.create(
                receipt=receipt,
                product=item.product,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit,
            )

        return Response({'detail': 'แปลงใบเสนอราคาเป็นใบเสร็จเรียบร้อยแล้ว'}, status=status.HTTP_201_CREATED)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class CashSaleViewSet(viewsets.ModelViewSet):
    queryset = CashSale.objects.all()
    serializer_class = CashSaleSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

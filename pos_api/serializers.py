from rest_framework import serializers
from .models import (
    Customer, Product, Category, Quotation, QuotationItem, Invoice, InvoiceItem,
    CashSale, CashSaleItem, Receipt
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id', 'quotation', 'product', 'quantity', 'price_per_unit', 'total_price']
        read_only_fields = ['total_price']

# เช็คว่า product มีอยู่ใน quotation item หรือไม่
    def validate(self, data):
        product = data.get('product')
        if product and not data.get('price_per_unit'):
            data['price_per_unit'] = product.price
        return data
    

class QuotationSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = QuotationItemSerializer(many=True)

    class Meta:
        model = Quotation
        fields = ['id', 'customer', 'quotation_date', 'total_amount', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        quotation = Quotation.objects.create(**validated_data)
        for item in items_data:
            QuotationItem.objects.create(quotation=quotation, **item)
        return quotation

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.customer = validated_data.get('customer', instance.customer)
        instance.quotation_date = validated_data.get('quotation_date', instance.quotation_date)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.save()

        # clear old items and recreate
        instance.items.all().delete()
        for item in items_data:
            QuotationItem.objects.create(quotation=instance, **item)

        return instance


class InvoiceItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'quantity', 'price_per_unit']


class InvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    quotation = serializers.PrimaryKeyRelatedField(queryset=Quotation.objects.all())
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'quotation', 'customer', 'invoice_date', 'total_amount', 'payment_status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.quotation = validated_data.get('quotation', instance.quotation)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.invoice_date = validated_data.get('invoice_date', instance.invoice_date)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.save()

        # clear old items and recreate
        instance.items.all().delete()
        for item in items_data:
            InvoiceItem.objects.create(invoice=instance, **item)

        return instance


class CashSaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CashSaleItem
        fields = ['id', 'product', 'quantity', 'price_per_unit']


class CashSaleSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = CashSaleItemSerializer(many=True)

    class Meta:
        model = CashSale
        fields = ['id', 'customer', 'cash_sale_date', 'total_amount', 'payment_method', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cash_sale = CashSale.objects.create(**validated_data)
        for item in items_data:
            CashSaleItem.objects.create(cash_sale=cash_sale, **item)
        return cash_sale

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.customer = validated_data.get('customer', instance.customer)
        instance.cash_sale_date = validated_data.get('cash_sale_date', instance.cash_sale_date)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.save()

        # clear old items and recreate
        instance.items.all().delete()
        for item in items_data:
            CashSaleItem.objects.create(cash_sale=instance, **item)

        return instance


class ReceiptSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Receipt
        fields = ['id', 'invoice', 'customer', 'receipt_date', 'total_amount', 'payment_method']

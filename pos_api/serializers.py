from rest_framework import serializers
from .models import (
    Customer, Product, Category, Quotation, QuotationItem, Invoice, InvoiceItem,
    CashSale, CashSaleItem, Receipt
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'


class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id', 'quotation', 'product', 'quantity', 'price_per_unit', 'total_price']
        read_only_fields = ['total_price']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity', 0)

        # เช็คราคา default จาก product
        if product and not data.get('price_per_unit'):
            data['price_per_unit'] = product.price

        # เช็คว่า quantity ต้องมากกว่า 0
        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than 0"})

        return data

    def create(self, validated_data):
        validated_data['total_price'] = validated_data['quantity'] * validated_data['price_per_unit']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price_per_unit = validated_data.get('price_per_unit', instance.price_per_unit)
        instance.total_price = instance.quantity * instance.price_per_unit
        instance.save()
        return instance
    

class QuotationSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = QuotationItemSerializer(many=True)

    class Meta:
        model = Quotation
        fields = ['id', 'customer', 'quotation_date', 'total_amount', 'created_at', 'updated_at', 'items']
        read_only_fields = ['total_amount']  # ❗️แนะนำให้เป็น read_only

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        quotation = Quotation.objects.create(**validated_data)

        total_amount = 0
        for item_data in items_data:
            item = QuotationItem.objects.create(quotation=quotation, **item_data)
            total_amount += item.total_price

        quotation.total_amount = total_amount
        quotation.save()
        return quotation

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.customer = validated_data.get('customer', instance.customer)
        instance.quotation_date = validated_data.get('quotation_date', instance.quotation_date)
        instance.save()

        # clear old items and recreate
        instance.items.all().delete()

        total_amount = 0
        for item_data in items_data:
            item = QuotationItem.objects.create(quotation=instance, **item_data)
            total_amount += item.total_price

        instance.total_amount = total_amount
        instance.save()
        return instance


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'product', 'quantity', 'price_per_unit', 'total_price']
        read_only_fields = ['total_price']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity', 0)

        if product and not data.get('price_per_unit'):
            data['price_per_unit'] = product.price

        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than 0"})

        return data

    def create(self, validated_data):
        validated_data['total_price'] = validated_data['quantity'] * validated_data['price_per_unit']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price_per_unit = validated_data.get('price_per_unit', instance.price_per_unit)
        instance.total_price = instance.quantity * instance.price_per_unit
        instance.save()
        return instance


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
    class Meta:
        model = CashSaleItem
        fields = ['id', 'cash_sale', 'product', 'quantity', 'price_per_unit', 'total_price']
        read_only_fields = ['total_price']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity', 0)

        # ถ้าไม่ส่ง price_per_unit → ใช้ราคาจาก product อัตโนมัติ
        if product and not data.get('price_per_unit'):
            data['price_per_unit'] = product.price

        # quantity ต้อง > 0
        if quantity <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than 0"})

        return data

    def create(self, validated_data):
        validated_data['total_price'] = validated_data['quantity'] * validated_data['price_per_unit']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price_per_unit = validated_data.get('price_per_unit', instance.price_per_unit)
        instance.total_price = instance.quantity * instance.price_per_unit
        instance.save()
        return instance


class CashSaleSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = CashSaleItemSerializer(many=True)

    class Meta:
        model = CashSale
        fields = ['id', 'customer', 'cash_sale_date', 'total_amount', 'payment_method', 'items']
        read_only_fields = ['total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cash_sale = CashSale.objects.create(**validated_data)

        total_amount = 0
        for item in items_data:
            item_obj = CashSaleItem.objects.create(cash_sale=cash_sale, **item)
            total_amount += item_obj.total_price

        cash_sale.total_amount = total_amount
        cash_sale.save()
        return cash_sale

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        instance.customer = validated_data.get('customer', instance.customer)
        instance.cash_sale_date = validated_data.get('cash_sale_date', instance.cash_sale_date)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.save()

        total_amount = 0
        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                item_obj = CashSaleItem.objects.create(cash_sale=instance, **item)
                total_amount += item_obj.total_price

            instance.total_amount = total_amount
            instance.save()

        return instance


class ReceiptSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Receipt
        fields = ['id', 'invoice', 'customer', 'receipt_date', 'total_amount', 'payment_method']

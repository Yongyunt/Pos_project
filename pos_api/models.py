from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Customer(models.Model):
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    line_id = models.CharField(max_length=255, blank=True, null=True)
    viber_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name_th)
    
    class Meta:
        ordering = ['id']


class CashSale(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('cash', _('เงินสด')),
        ('transfer', _('โอน')),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cash_sales', null=True, blank=True)
    cash_sale_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
    )

    @property
    def calculated_total_amount(self):
        return sum(item.total_price for item in self.items.all()) or 0

    def __str__(self):
        return f"{self.cash_sale_date} | {(self.customer.name_th if self.customer else 'ไม่มีลูกค้า')} | {self.calculated_total_amount}฿"


class CashSaleItem(models.Model):
    cash_sale = models.ForeignKey('CashSale', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        """คำนวณราคารวมของรายการนี้"""
        if self.quantity and self.price_per_unit:
            return self.quantity * self.price_per_unit
        return 0

    def clean(self):
        # ตรวจสอบว่าสินค้าในสต็อกเพียงพอ
        if self.quantity > self.product.stock_quantity:
            raise ValidationError('สินค้าในสต็อกไม่เพียงพอ')

    def save(self, *args, **kwargs):
        # ใส่ราคาต่อหน่วยอัตโนมัติถ้ายังไม่มี
        if not self.price_per_unit:
            self.price_per_unit = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} ราคาต่อหน่วย = {self.price_per_unit}฿"
        

class Quotation(models.Model):

    STATUS_CHOICES = [
        ('pending', 'รออนุมัติ'),
        ('approved', 'อนุมัติ'),
        ('Not approved', 'ไม่ได้รับการอนุมัติ'),
        ('converted', 'แปลงเป็นใบเสร็จรับเงิน'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending') 
    quotation_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่อัปเดต")

    def update_total_amount(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()

    def save(self, *args, **kwargs):
        creating_receipt = False
        if self.pk:  # ถ้าแก้ไข (ไม่ใช่สร้างใหม่)
            orig = Quotation.objects.get(pk=self.pk)
            if orig.status != 'converted' and self.status == 'converted':
                creating_receipt = True
        super().save(*args, **kwargs)

        if creating_receipt:
            # สร้างใบเสร็จ ถ้ายังไม่มี
            from .models import Receipt
            Receipt.objects.get_or_create(
                quotation=self,
                defaults={
                    'customer': self.customer,
                    'total_amount': self.total_amount,
                }
            )

    def __str__(self):
        return f"[{self.quotation_date}] ลูกค้า: {self.customer.name_th} | ยอดรวม: ฿{self.total_amount} | สถานะ: {self.status}"

    class Meta:
        ordering = ['id']

class Receipt(models.Model):
    PAYMENT_METHOD_CHOICES = [
    ('cash', _('เงินสด')),
    ('transfer', _('โอน')),
]
    
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='receipts', null=True, blank=True)
    quotation = models.ForeignKey('Quotation', on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='receipts', null=True, blank=True)
    receipt_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD_CHOICES)

    def calculate_total_amount(self):
        """คำนวณราคารวมจาก ReceiptItem ทั้งหมด"""
        total = sum(item.total_price for item in self.items.all())
        return total

    def save(self, *args, **kwargs):
        if self.quotation and not self.customer:
            self.customer = self.quotation.customer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_date} | {(self.customer.name_th if self.customer else 'ไม่มีลูกค้า')} | {self.total_amount} | {self.payment_method}"

    class Meta:
        ordering = ['id']

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    # parent_category = models.ForeignKey(
    #     'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories'
    # )

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)            # ราคาขาย
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)           # ราคาต้นทุน
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return f"{self.id} - {self.name}"
        # return "id: {} ขื่อสินค้า {} ราคาต่อหน่วย {} จำนวนคงคลัง {} หมวดหมู่สินค้า {}".format(self.id, self.name, self.unit_price, self.stock_quantity, self.category)

    class Meta:
        ordering = ['id']


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # ต้องมีจำนวนอย่างน้อย 1
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        """คำนวณราคารวมอัตโนมัติ"""
        return self.quantity * self.price_per_unit

    def clean(self):
        if self.quantity > self.product.stock_quantity:
            raise ValidationError('สินค้าในสต็อกไม่เพียงพอ')

    def save(self, *args, **kwargs):
        # ถ้ายังไม่มีราคา (หรืออยากให้ update ทุกครั้งที่เปลี่ยน product)
        if not self.price_per_unit:
            self.price_per_unit = self.product.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} ราคาต่อหน่วย = {self.price_per_unit}฿"

    
class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        qty = self.quantity or 0
        price = self.price_per_unit or 0
        return qty * price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.receipt.save()  # ให้ Receipt คำนวณยอดรวมใหม่

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.receipt.save()  # ให้ Receipt คำนวณยอดรวมใหม่

    def __str__(self):
        return f"{self.product.name} x{self.quantity} ราคาต่อหน่วย = {self.price_per_unit}฿"


class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('draft', _('แบบร่าง')),
        ('sent', _('ส่งแล้ว')),                   # ส่งใบแจ้งหนี้ให้ลูกค้าแล้ว
        ('partial', _('ชำระบางส่วน')),            # ลูกค้าจ่ายมาแล้วบางส่วน
        ('paid', _('ชำระแล้วทั้งหมด')),           # ลูกค้าชำระครบแล้ว
        ('shipped', _('จัดส่งแล้ว')),
        ('cancelled', _('ยกเลิก')),
        ('pending', _('รอดำเนินการ')),           # สถานะรอดำเนินการ
    ]

    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.invoice_date,self.id,self.customer,self.total_amount,self.status
    

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"









    

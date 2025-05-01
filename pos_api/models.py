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
        

class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', _('แบบร่าง')),
        ('sent', _('ส่งแล้ว')),
        ('pending', 'รออนุมัติ'),
        ('revised', _('ปรับแก้ไข')),
        ('approved', _('ลูกค้าอนุมัติ')),
        ('rejected', _('ลูกค้าปฏิเสธ')),
        ('cancelled', _('ยกเลิก')),
        ('converted', _('แปลงเป็นใบแจ้งหนี้')),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',  # ตั้งค่าสถานะเริ่มต้นเป็น 'pending'
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quotation_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่สร้าง"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("วันที่อัปเดต"))

    def __str__(self):
           return "วันที่ {} id: {} ชื่อลูกค้า {} ยอดรวม {} สภานะ {}".format(self.quotation_date, self.id, self.customer.name_th, self.total_amount, self.status)
        

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
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity} @ ฿{self.price_per_unit}"


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    # parent_category = models.ForeignKey(
    #     'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories'
    # )

    def __str__(self):
        return self.category_name


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


class CashSale(models.Model):
    PAYMENT_METHOD_CHOICES = [
    ('cash', _('เงินสด')),
    ('transfer', _('โอน')),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cash_sales')
    cash_sale_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return  self.cash_sale_date,self.id,self.customer,self.total_amount,self.payment_method
    
class CashSaleItem(models.Model):
    cash_sale = models.ForeignKey(CashSale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Receipt(models.Model):
    PAYMENT_METHOD_CHOICES = [
    ('cash', _('เงินสด')),
    ('transfer', _('โอน')),
]
    invoice = models.ForeignKey(Invoice, null=True, blank=True, on_delete=models.SET_NULL, related_name='receipts')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='receipts')
    receipt_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return {self.receipt_date,self.id,self.customer,self.total_amount,self.payment_method}
    

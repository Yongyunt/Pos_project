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


class Receipt(models.Model):
    PAYMENT_METHOD_CHOICES = [
    ('cash', _('เงินสด')),
    ('transfer', _('โอน')),
]
    
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='receipts', null=True, blank=True)
    quotation = models.ForeignKey('Quotation', on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    customer = models.ForeignKey('customer', on_delete=models.CASCADE, related_name='receipts')
    receipt_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.receipt_date} | {(self.customer.name_th if self.customer else 'ไม่มีลูกค้า')} | {self.total_amount} | {self.payment_method}"
        # return {self.receipt_date,self.id,self.customer,self.total_amount,self.payment_method}
    
class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
    
    class Meta:
        unique_together = ('receipt', 'product')


class Quotation(models.Model):
    STATUS_CHOICES = [
        ('sent', _('ส่งแล้ว')),
        ('pending', 'รออนุมัติ'),
        ('approved', _('ดำเนินการแล้ว')),
        ('Not approved', _('ไม่ได้รับการอนุมัติ')),
        ('converted', _('แปลงเป็นใบเสร็จรับเงิน')),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',  # ตั้งค่าสถานะเริ่มต้นเป็น 'pending'
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quotation_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่สร้าง"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("วันที่อัปเดต"))

    def save(self, *args, **kwargs):
        # ถ้า status เป็น approved → เปลี่ยนเป็น 'ดำเนินการแล้ว'
        if self.status == 'approved':
            self.status = 'ดำเนินการแล้ว'
        super().save(*args, **kwargs)

    def update_total_amount(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"[{self.quotation_date}] ลูกค้า: {self.customer.name_th} | ยอดรวม: ฿{self.total_amount} | สถานะ: {self.status}"

    class Meta:
        ordering = ['id'] 

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

    def save(self, *args, **kwargs):
        # ถ้ายังไม่มีราคา (หรืออยากให้ update ทุกครั้งที่เปลี่ยน product)
        if not self.price_per_unit:
            self.price_per_unit = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x{self.quantity} ราคาต่อหน่วย = {self.price_per_unit}฿"

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



    

from django.contrib import admin
from pos_api.models import Customer,Quotation,QuotationItem,Product,Category,CashSale,CashSaleItem,Receipt,ReceiptItem


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name_th','address','phone_number')
    search_fields = ('name_th',)

admin.site.register(Customer, CustomerAdmin)


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1

class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_date', 'id', 'customer', 'total_amount', 'status')
    search_fields = ('customer__name_th',)  # แก้ให้ตรง field
    list_filter = ('status',)
    list_editable = ('status',)
    inlines = [QuotationItemInline]
    readonly_fields = ['total_amount']


admin.site.register(Quotation, QuotationAdmin)
admin.site.register(QuotationItem)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price', 'stock_quantity', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

admin.site.register(Product, ProductAdmin)


# Inline สำหรับแสดง ReceiptItem ในหน้า Receipt
class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 1
    readonly_fields = ('total_price',)
    fields = ('product', 'quantity', 'price_per_unit', 'total_price',)

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'ราคารวม'

# Register Receipt พร้อม inline ReceiptItem
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id','receipt_date', 'customer', 'total_amount', 'payment_method')
    inlines = [ReceiptItemInline]
    search_fields = ('customer__name_th',)
    list_filter = ('payment_method',)
    list_editable = ('payment_method',)
    readonly_fields = ('total_amount',)

# (ถ้าอยากให้ ReceiptItem แก้ไขแยกเดี่ยวได้ด้วย)
@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'product', 'quantity', 'price_per_unit', 'total_price')
    search_fields = ('receipt__customer__name_th', 'product__name',)

    def total_price_display(self, obj):
        return obj.total_price
    total_price_display.short_description = 'ราคารวม'
    

class CashSaleItemInline(admin.TabularInline):
    model = CashSaleItem
    extra = 1
    readonly_fields = ('total_price_display',)
    fields = ('product', 'quantity', 'price_per_unit', 'total_price_display')

    def total_price_display(self, obj):
        if obj.pk:
            return f"{obj.total_price:.2f} ฿"
        return "-"
    total_price_display.short_description = 'ราคารวม'

@admin.register(CashSale)
class CashSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cash_sale_date', 'customer', 'calculated_total_amount_display', 'payment_method')
    inlines = [CashSaleItemInline]

    def calculated_total_amount_display(self, obj):
        return f"{obj.calculated_total_amount:.2f} ฿"
    calculated_total_amount_display.short_description = 'ยอดรวม'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)


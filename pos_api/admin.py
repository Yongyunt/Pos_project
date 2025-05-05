from django.contrib import admin
from pos_api.models import Customer,Quotation,QuotationItem,Product,Category,CashSale,Receipt

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name_th','address','phone_number')
    search_fields = ('name_th',)

admin.site.register(Customer, CustomerAdmin)


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1

class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_date','id', 'customer', 'total_amount' ,'status')
    search_fields = ('customer__name',)
    list_filter = ('status',)
    inlines = [QuotationItemInline]
    readonly_fields = ['total_amount']  # ให้แสดงยอดรวมแต่แก้ไขไม่ได้

    def get_changeform_initial_data(self, request):
        return {'status': 'pending'}  # ตั้งค่าเริ่มต้นเป็น pending
     

admin.site.register(Quotation, QuotationAdmin)
admin.site.register(QuotationItem)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price', 'stock_quantity', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Receipt)

admin.site.register(CashSale)
admin.site.register(Category)

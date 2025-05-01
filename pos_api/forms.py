# from django import forms
# from models import Product, Quotation, QuotationItem

# class QuotationItemForm(forms.ModelForm):
#     class Meta:
#         model = QuotationItem
#         fields = ['product', 'quantity']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['product'].widget.attrs.update({'class': 'select2-product'})

#     def clean(self):
#         cleaned_data = super().clean()
#         product = cleaned_data.get('product')
#         if product:
#             cleaned_data['unit_price'] = product.unit_price  # ดึงราคาจาก Product มาใส่
#         return cleaned_data
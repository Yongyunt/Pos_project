from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, CategoryViewSet, ProductViewSet, QuotationViewSet,
    InvoiceViewSet, CashSaleViewSet, ReceiptViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'cashsales', CashSaleViewSet)
router.register(r'receipts', ReceiptViewSet)

urlpatterns = router.urls
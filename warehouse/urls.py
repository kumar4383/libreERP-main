from django.conf.urls import include, url
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'service' , ServiceViewSet , base_name = 'service')
router.register(r'contact' , ContactViewSet , base_name = 'contact')
router.register(r'contract' , ContractViewSet , base_name = 'contract')
router.register(r'invoice' , InvoiceViewSet , base_name = 'invoice')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'downloadInvoice/$' , DownloadInvoice.as_view() ),
]

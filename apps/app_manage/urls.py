from django.urls import path
from apps.app_manage import certificate

urlpatterns = [
    path('certificate', certificate.certificate, name='certificate'),
    path('certificate/add', certificate.certificate_add, name='certificate_add'),
    path('certificate/edit/<int:certificate_id>/', certificate.certificate_edit, name='certificate_edit'),
    path('certificate/del', certificate.certificate_del, name='certificate_del'),
]
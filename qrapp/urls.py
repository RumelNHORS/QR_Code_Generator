# # qrapp/urls.py
# from django.urls import path
# from .views import generate_qr_code, qr_code_page

# urlpatterns = [
#     path('qr-code/', generate_qr_code, name='generate_qr_code'),
#     path('qr-code-page/', qr_code_page, name='qr_code_page'),
# ]


# qrapp/urls.py
from django.urls import path
from .views import download_qr_code, generate_qr_code

urlpatterns = [
    path('qr-code/', generate_qr_code, name='generate_qr_code'),
    path('download-qr-code/', download_qr_code, name='download_qr_code'),
]



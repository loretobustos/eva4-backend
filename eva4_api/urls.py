from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from proyects.api import WebpayIniciarPagoView, WebpayConfirmarPagoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/webpay/pagar/', WebpayIniciarPagoView.as_view(), name='webpay_pagar'),
    path('api/webpay/confirmar/', WebpayConfirmarPagoView.as_view(), name='webpay_confirmar'),
    path('', include('proyects.urls')),
]


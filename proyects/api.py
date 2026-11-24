from rest_framework import viewsets, permissions
from guardian.shortcuts import assign_perm
from .models import Proyect
from .serializers import ProyectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
import random


class WebpayIniciarPagoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount', 10000)
        buy_order = f"orden-{random.randint(1000, 99999)}"
        session_id = f"sesion-{request.user.id}"
        return_url = request.build_absolute_uri('/api/webpay/confirmar/')

        tx = Transaction.build_for_integration(
            IntegrationCommerceCodes.WEBPAY_PLUS,
            IntegrationApiKeys.WEBPAY
        )
        response = tx.create(buy_order, session_id, amount, return_url)
        return Response({
            "mensaje": "Transacción iniciada en Webpay Plus",
            "token": response['token'],
            "url_pago": response['url']
        }, status=status.HTTP_200_OK)

class WebpayConfirmarPagoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get('token_ws')
        if not token:
            return Response({"error": "Falta token_ws"}, status=status.HTTP_400_BAD_REQUEST)

        tx = Transaction.build_for_integration(
            IntegrationCommerceCodes.WEBPAY_PLUS,
            IntegrationApiKeys.WEBPAY
        )
        response = tx.commit(token)
        return Response(response, status=status.HTTP_200_OK)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Proyect.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProyectSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        # Asigna permisos de objeto usando Django Guardian al creador
        assign_perm('proyects.change_proyect', self.request.user, instance)
        assign_perm('proyects.delete_proyect', self.request.user, instance)

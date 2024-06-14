# -*- coding: utf-8 -*-
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import KombatResponseSerializer, KombatSerializer
from .utils import TalanaKombat


class KombatAPIView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=KombatSerializer,
        responses={200: KombatResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        content = {}
        serializer = KombatSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            movements_and_winner = TalanaKombat(
                player1=validated_data["player1"], player2=validated_data["player2"]
            ).kombat()
            content = movements_and_winner
            return Response(content, status=status.HTTP_200_OK)
        content["error"] = serializer.errors
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

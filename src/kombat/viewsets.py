# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import TalanaKombat


class KombatAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        content = {}
        movements = TalanaKombat(player1=request.data["player1"], player2=request.data["player2"]).kombat()
        content["movements"] = movements
        return Response(content, status=status.HTTP_200_OK)

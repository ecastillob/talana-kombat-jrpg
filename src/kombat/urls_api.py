# -*- coding: utf-8 -*-
from django.urls import path

from . import viewsets

urlpatterns = [
    path("kombat", viewsets.KombatAPIView.as_view(), name="kombat"),
]

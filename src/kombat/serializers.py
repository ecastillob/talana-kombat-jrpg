# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import serializers


class PlayerSerializer(serializers.Serializer):
    movimientos = serializers.ListField(
        child=serializers.CharField(allow_blank=True, max_length=settings.MAX_MOVEMENT_LENGTH), allow_empty=True
    )
    golpes = serializers.ListField(
        child=serializers.CharField(allow_blank=True, max_length=settings.MAX_MOVEMENT_LENGTH), allow_empty=True
    )

    def validate(self, data):
        # validate movements
        validated_movements = []
        for value in data["movimientos"]:
            clean_value = value.upper().strip()
            for char in clean_value:
                if char not in {"A", "S", "D", "W"}:
                    raise serializers.ValidationError("Uno de los botones presionados de un movimiento es ilegal")
            validated_movements.append(clean_value)
        # validate hits
        validated_hits = []
        for value in data["golpes"]:
            clean_value = value.upper().strip()
            for char in clean_value:
                if char not in {"K", "P"}:
                    raise serializers.ValidationError("Uno de los botones presionados de un golpe es ilegal")
            validated_hits.append(clean_value)
        # return validated data
        return {
            "movimientos": validated_movements,
            "golpes": validated_hits,
        }


class KombatSerializer(serializers.Serializer):
    player1 = PlayerSerializer()
    player2 = PlayerSerializer()


class WinnerResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    energy = serializers.IntegerField()


class KombatResponseSerializer(serializers.Serializer):
    movements = serializers.ListField(child=serializers.CharField())
    winner = WinnerResponseSerializer

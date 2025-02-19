from rest_framework import serializers
from .models import Player, Batting, Pitching


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class BattingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batting
        fields = '__all__'


class PitchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitching
        fields = '__all__'


class StatsSerializer(serializers.Serializer):
    batting = BattingSerializer(many=True, required=False)
    pitching = PitchingSerializer(many=True, required=False)
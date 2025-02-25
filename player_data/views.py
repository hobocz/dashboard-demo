from player_data.models import Player, Batting, Pitching
from player_data.serializers import PlayerSerializer, StatsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from collections import namedtuple


""" Simple class views

Django Rest Framework provides ViewSets, mixins, 'already mixed-in generic views',
etc. With a more fully implemented API these could/should be used. However since 
we only need simple data retrieval, the basic APIView is used here.
"""

class PlayerList(APIView):
    def get(self, request, format=None):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)


class PlayerDetail(APIView):
    def get(self, request, id, format=None):
        try:
            player_detail = Player.objects.get(id=id)
        except Player.DoesNotExist:
            raise Http404
        serializer = PlayerSerializer(player_detail)
        return Response(serializer.data)
    

class PlayerStats(APIView):
    def get(self, request, id, format=None):
        try: # make sure the player exists first
            player_detail = Player.objects.get(id=id)
        except Player.DoesNotExist:
            raise Http404
        # Creating a namedtuple structure for the StatsSerializer
        PlayerStats = namedtuple('PlayerStats', ('batting', 'pitching'))
        stats = PlayerStats(
            batting = Batting.objects.filter(player=id),
            pitching = Pitching.objects.filter(player=id)
        )
        serializer = StatsSerializer(stats)
        return Response(serializer.data)
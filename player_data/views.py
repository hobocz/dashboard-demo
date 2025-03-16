from player_data.models import Player, Batting, Pitching
from player_data.serializers import PlayerSerializer, StatsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from collections import namedtuple
from django.http import JsonResponse
from django.db import connection

""" Simple class views

Django Rest Framework provides ViewSets, mixins, 'already mixed-in generic views',
etc. With a more fully implemented API these could/should be used. However since 
we only need simple data retrieval, the basic APIView is used here.
"""

class PlayerList(APIView):
    def get(self, request, format=None):
        stat = request.GET.get('stat')
        print("STAT: ", stat)
        if stat == 'batting':
            players = Player.objects.filter(batting__isnull=False).distinct()
        elif stat == 'pitching':
            players = Player.objects.filter(pitching__isnull=False).distinct()
        else:
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
    

""" Using SQL

The following is an example of using SQL to query the database
intead of the Django ORM.
"""

def cursor_to_dictionaries(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

""" This is the 'Top Young Pitchers Query'. 
Select players who:
- are X years old or younger and
- average X or more pitching wins per year
- in X years or less
Note that the date related functions work with SQLite
and may need to change for other DBs
"""
def typ_sql(max_age, min_avg_wins, max_years):
    return f"""
    SELECT 
        p.id, 
        p.name_first, 
        p.name_last, 
        p.throws, 
        CAST((julianday('now') - julianday(birth_date)) / 365.25 AS INTEGER) AS age,
        COUNT(*) AS years, 
        SUM(s.year_wins) AS wins, 
        ROUND(CAST(SUM(s.year_wins) AS FLOAT) / NULLIF(COUNT(*), 0), 1) AS wins_per_year
    FROM player_data_player AS p
    INNER JOIN (
        SELECT 
            player_id, 
            COUNT(*) AS year_stat_cnt, 
            SUM(wins) AS year_wins
        FROM player_data_pitching
        GROUP BY player_id, year
    ) AS s
    ON p.id = s.player_id
    WHERE p.birth_date > date('now', '-{max_age + 1} years')
    GROUP BY p.id
    HAVING wins_per_year >= {min_avg_wins} AND years <= {max_years}
    ORDER BY wins_per_year DESC, years ASC
    """

# ToDo: the incoming and outgoing data should be run through a proper 
# serializer. For now, we're trusting the post and using the default 
# serializer in the JsonResponse
class TopYoungPitchersView(APIView):
    def post(self, request):
        with connection.cursor() as cursor:
            cursor.execute(typ_sql(
                request.data.get('maxAge'),
                request.data.get('minAvgWins'),
                request.data.get('maxYears')
            ))
            players = cursor_to_dictionaries(cursor)
        return JsonResponse(players, safe=False)

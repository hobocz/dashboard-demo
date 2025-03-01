from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Player
from .serializers import PlayerSerializer


""" Create a simple testable Player

Tests could also be run on a fixture to get additional
and more accurate data. This is assuming data is already
loaded into the DB and the fixture has been exported.
"""
testPlayerData = {
    'id': 123,
    'name_first': 'George',
    'name_use': 'George',
    'name_last': 'Brett',
    'team': 'KC',
    'birth_date': '1953-05-15',
    'height_feet': 6,
    'height_inches': 0,
    'weight': 185,
    'throws': 'R',
    'bats': 'L',
    'primary_position': '5',
}


class PlayerAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.player = Player.objects.create(**testPlayerData)
        self.list_url = reverse('player_list')
        self.detail_url = reverse('player_detail', args=[self.player.id])

    # HTTP Response Tests
    def test_list_players(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name_last', status_code=200)
        self.assertNotContains(response, None, status_code=200)
        first_name = response.json()[0]['name_first']
        self.assertEqual(first_name, 'George')
        id_val = response.json()[0]['id']
        self.assertTrue(isinstance(id_val, int))

    def test_retrieve_player(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    # Serializer Validation Test
    def test_invalid_serializer(self):
        serializer = PlayerSerializer(instance=self.player)
        self.assertEqual(serializer.data['id'], 123)
        self.assertTrue(isinstance(serializer.data['weight'], int))

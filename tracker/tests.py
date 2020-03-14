from django.test import TestCase
from django.urls import reverse

from .models import Number


class TestNumberModel(TestCase):

    def test_increment_count(self):
        number = Number(value=1)
        self.assertIs(number.count, 1)
        number.incrementCount(25)
        self.assertIs(number.count, 26)

class IndexViewTest(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class TrackOrIncrementView(TestCase):

    def test_track_new_number_json(self):
        data = {'number': '2'}
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You added the number 2")

    def test_increment_number_json(self):
        number = Number(value=3)
        number.save()
        self.assertIs(number.value, 3)
        data = {'number': '3', 'increment_value': '10'}
        response = self.client.put(reverse('track_or_increment'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This number has been tracked 11 time(s) so far")

    def test_track_new_number_json_no_number_attribute(self):
        data = {}
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_increment_number_json_number_not_added_yet(self):
        data = {'number': '4', 'increment_value': '10'}
        response = self.client.put(reverse('track_or_increment'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_increment_number_json_increment_value_negative(self):
        number = Number(value=5)
        number.save()
        self.assertIs(number.value, 5)
        data = {'number': '5', 'increment_value': '-1'}
        response = self.client.put(reverse('track_or_increment'), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_track_new_number_form(self):
        data = 'number=2'
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You added the number 2")

    def test_increment_number_form(self):
        number = Number(value=3)
        number.save()
        self.assertIs(number.value, 3)
        data = 'number=3&increment_value=10'
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This number has been tracked 11 time(s) so far")

    def test_track_new_number_form_no_number_attribute(self):
        data = {}
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 400)

    def test_increment_number_form_number_not_added_yet(self):
        data = 'number=4&increment_value=10'
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 400)

    def test_increment_number_form_increment_value_negative(self):
        number = Number(value=5)
        number.save()
        self.assertIs(number.value, 5)
        data = 'number=5&increment_value=-1'
        response = self.client.post(reverse('track_or_increment'), data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 400)

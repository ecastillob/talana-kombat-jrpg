import json
from pathlib import Path

from django.urls import reverse
from rest_framework.test import APISimpleTestCase


class T1DemoTest(APISimpleTestCase):
    databases = "__all__"
    fixture_folder = Path(__file__).resolve().parent / "fixtures"

    def test_01_kombats_bad(self):
        url = reverse("kombat")
        with open(self.fixture_folder / "kombats_bad.json", encoding="utf8") as file:
            examples = json.load(file)
        for kombat in examples:
            response = self.client.post(url, kombat["input"], format="json")
            self.assertEqual(response.status_code, 400)
            self.assertEqual(json.loads(response.content), kombat["output"])

    def test_02_kombats_ok(self):
        url = reverse("kombat")
        with open(self.fixture_folder / "kombats_ok.json", encoding="utf8") as file:
            examples = json.load(file)
        for kombat in examples:
            response = self.client.post(url, kombat["input"], format="json")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, kombat["output"])

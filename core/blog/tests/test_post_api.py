from rest_framework.test import APIClient
from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestPostApi:
    client = APIClient()

    def test_get_post_response_200(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

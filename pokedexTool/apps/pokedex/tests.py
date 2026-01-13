import pytest
from django.urls import reverse


class TestPokedexHomeView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("pokedex:poke-home"))
        assert response.status_code == 302  # redirect to login

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("pokedex:poke-home"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_uses_correct_template(self, client, user):
        client.force_login(user)
        response = client.get(reverse("pokedex:poke-home"))
        assert "pokedex/pokedex-home.html" in [t.name for t in response.templates]

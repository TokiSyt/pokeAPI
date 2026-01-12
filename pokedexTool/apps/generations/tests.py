import pytest
from django.urls import reverse

from apps.generations.models import Generation


class TestGenerationModel:
    @pytest.mark.django_db
    def test_create_generation(self, generation_factory):
        gen = generation_factory(internal_name="generation-i", gen_id=1)
        assert gen.internal_name == "generation-i"
        assert gen.gen_id == 1

    @pytest.mark.django_db
    def test_abilities_list_parses_valid(self, generation_factory):
        gen = generation_factory(abilities="['overgrow', 'blaze', 'torrent']")
        assert gen.abilities_list == ["overgrow", "blaze", "torrent"]

    @pytest.mark.django_db
    def test_abilities_list_returns_fallback_for_empty(self, generation_factory):
        gen = generation_factory(abilities="[]")
        assert gen.abilities_list == ["No abilities"]

    @pytest.mark.django_db
    def test_abilities_list_handles_malformed(self, generation_factory):
        gen = generation_factory(abilities="invalid")
        assert gen.abilities_list == []

    @pytest.mark.django_db
    def test_moves_list_parses_valid(self, generation_factory):
        gen = generation_factory(moves="['tackle', 'pound']")
        assert gen.moves_list == ["tackle", "pound"]

    @pytest.mark.django_db
    def test_moves_list_returns_fallback_for_empty(self, generation_factory):
        gen = generation_factory(moves="[]")
        assert gen.moves_list == ["No moves"]

    @pytest.mark.django_db
    def test_moves_list_handles_malformed(self, generation_factory):
        gen = generation_factory(moves="invalid")
        assert gen.moves_list == []

    @pytest.mark.django_db
    def test_types_list_parses_valid(self, generation_factory):
        gen = generation_factory(types="['normal', 'fire', 'water']")
        assert gen.types_list == ["normal", "fire", "water"]

    @pytest.mark.django_db
    def test_types_list_returns_fallback_for_empty(self, generation_factory):
        gen = generation_factory(types="[]")
        assert gen.types_list == ["No types"]

    @pytest.mark.django_db
    def test_types_list_handles_malformed(self, generation_factory):
        gen = generation_factory(types="invalid")
        assert gen.types_list == []

    @pytest.mark.django_db
    def test_ordering_by_gen_id(self, generation_factory):
        g3 = generation_factory(gen_id=3)
        g1 = generation_factory(gen_id=1)
        g2 = generation_factory(gen_id=2)
        generations = list(Generation.objects.all())
        assert generations == [g1, g2, g3]

    @pytest.mark.django_db
    def test_allowed_users_relationship(self, generation, user):
        generation.allowed_users.add(user)
        assert user in generation.allowed_users.all()


class TestGenSearchView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("generations:gen-search"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("generations:gen-search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filters_by_allowed_users(self, client, user, generation_factory):
        allowed_gen = generation_factory(internal_name="generation-i")
        allowed_gen.allowed_users.add(user)
        other_gen = generation_factory(internal_name="generation-ii")

        client.force_login(user)
        response = client.get(reverse("generations:gen-search"))

        assert allowed_gen in response.context["gens"]
        assert other_gen not in response.context["gens"]


class TestGenDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse(
                "generations:gen-detail", kwargs={"generation_name_or_id": "generation-i"}
            )
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_lookup_by_name(self, client, user, generation_factory):
        gen = generation_factory(internal_name="generation-i")
        gen.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse(
                "generations:gen-detail", kwargs={"generation_name_or_id": "generation-i"}
            )
        )
        assert response.status_code == 200
        assert response.context["generation"] == gen

    @pytest.mark.django_db
    def test_lookup_by_id(self, client, user, generation_factory):
        gen = generation_factory(gen_id=1)
        gen.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse("generations:gen-detail", kwargs={"generation_name_or_id": "1"})
        )
        assert response.status_code == 200
        assert response.context["generation"] == gen

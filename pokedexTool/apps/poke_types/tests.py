import pytest
from django.urls import reverse

from apps.poke_types.models import PokemonType, TypeDamageRelation


class TestPokemonTypeModel:
    @pytest.mark.django_db
    def test_create_type(self, pokemon_type_factory):
        poke_type = pokemon_type_factory(name="fire", type_id=10)
        assert poke_type.name == "fire"
        assert poke_type.type_id == 10

    @pytest.mark.django_db
    def test_str_returns_name_and_id(self, pokemon_type):
        expected = f"{pokemon_type.name}_({pokemon_type.type_id})"
        assert str(pokemon_type) == expected

    @pytest.mark.django_db
    def test_moves_list_parses_valid_string(self, pokemon_type_factory):
        poke_type = pokemon_type_factory(moves="['ember', 'fire-punch']")
        assert poke_type.moves_list == ["ember", "fire-punch"]

    @pytest.mark.django_db
    def test_moves_list_handles_empty(self, pokemon_type_factory):
        poke_type = pokemon_type_factory(moves="[]")
        assert poke_type.moves_list == [" "]  # returns [" "] for empty

    @pytest.mark.django_db
    def test_moves_list_handles_malformed(self, pokemon_type_factory):
        poke_type = pokemon_type_factory(moves="invalid")
        assert poke_type.moves_list == []

    @pytest.mark.django_db
    def test_ordering_by_type_id(self, pokemon_type_factory):
        t3 = pokemon_type_factory(type_id=3)
        t1 = pokemon_type_factory(type_id=1)
        t2 = pokemon_type_factory(type_id=2)
        types = list(PokemonType.objects.all())
        assert types == [t1, t2, t3]


class TestTypeDamageRelation:
    @pytest.mark.django_db
    def test_create_damage_relation(self, type_damage_relation):
        assert type_damage_relation.double_damage_to == "grass, ice"
        assert type_damage_relation.half_damage_from == "grass, ice"

    @pytest.mark.django_db
    def test_str_returns_description(self, type_damage_relation):
        expected = f"Damage relations for {type_damage_relation.type.name}"
        assert str(type_damage_relation) == expected

    @pytest.mark.django_db
    def test_one_to_one_with_type(self, pokemon_type):
        relation = TypeDamageRelation.objects.create(
            type=pokemon_type,
            double_damage_to="water",
            half_damage_to="fire",
        )
        assert relation.type == pokemon_type
        assert pokemon_type.damage_relations == relation


class TestTypeSearchView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("poke_types:types-search"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("poke_types:types-search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_displays_all_types(self, client, user, pokemon_type_factory):
        type1 = pokemon_type_factory(name="fire")
        type2 = pokemon_type_factory(name="water")

        client.force_login(user)
        response = client.get(reverse("poke_types:types-search"))

        assert type1 in response.context["types"]
        assert type2 in response.context["types"]


class TestTypeDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse("poke_types:types-detail", kwargs={"poke_type_name_or_id": "fire"})
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_lookup_by_name(self, client, user, pokemon_type_factory):
        poke_type = pokemon_type_factory(name="fire")
        # TypeDetailView requires a TypeDamageRelation to exist
        TypeDamageRelation.objects.create(
            type=poke_type,
            double_damage_to="grass",
            half_damage_from="water",
        )
        client.force_login(user)
        response = client.get(
            reverse("poke_types:types-detail", kwargs={"poke_type_name_or_id": "fire"})
        )
        assert response.status_code == 200
        assert response.context["type"] == poke_type

    @pytest.mark.django_db
    def test_lookup_by_id(self, client, user, pokemon_type_factory):
        poke_type = pokemon_type_factory(type_id=10)
        # TypeDetailView requires a TypeDamageRelation to exist
        TypeDamageRelation.objects.create(
            type=poke_type,
            double_damage_to="grass",
            half_damage_from="water",
        )
        client.force_login(user)
        response = client.get(
            reverse("poke_types:types-detail", kwargs={"poke_type_name_or_id": "10"})
        )
        assert response.status_code == 200
        assert response.context["type"] == poke_type

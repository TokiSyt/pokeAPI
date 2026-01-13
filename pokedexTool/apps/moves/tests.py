import pytest
from django.urls import reverse

from apps.moves.models import PokemonMove


class TestPokemonMoveModel:
    @pytest.mark.django_db
    def test_create_move(self, pokemon_move_factory):
        move = pokemon_move_factory(name="tackle", move_id=33)
        assert move.name == "tackle"
        assert move.move_id == 33

    @pytest.mark.django_db
    def test_str_returns_name_and_id(self, pokemon_move):
        expected = f"{pokemon_move.name}_{pokemon_move.move_id}"
        assert str(pokemon_move) == expected

    @pytest.mark.django_db
    def test_move_fields(self, pokemon_move_factory):
        move = pokemon_move_factory(
            accuracy=100,
            power=50,
            pp=35,
            priority=0,
            damage_class="physical",
            type="normal",
        )
        assert move.accuracy == 100
        assert move.power == 50
        assert move.pp == 35
        assert move.damage_class == "physical"
        assert move.type == "normal"

    @pytest.mark.django_db
    def test_optional_fields_can_be_null(self, pokemon_move_factory):
        move = pokemon_move_factory(
            accuracy=None,
            power=None,
            effect_chance=None,
        )
        assert move.accuracy is None
        assert move.power is None
        assert move.effect_chance is None

    @pytest.mark.django_db
    def test_ordering_by_move_id(self, pokemon_move_factory):
        m3 = pokemon_move_factory(move_id=3)
        m1 = pokemon_move_factory(move_id=1)
        m2 = pokemon_move_factory(move_id=2)
        moves = list(PokemonMove.objects.all())
        assert moves == [m1, m2, m3]

    @pytest.mark.django_db
    def test_allowed_users_relationship(self, pokemon_move, user):
        pokemon_move.allowed_users.add(user)
        assert user in pokemon_move.allowed_users.all()


class TestMoveSearchView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("poke_moves:moves-search"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("poke_moves:moves-search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filters_by_allowed_users(self, client, user, pokemon_move_factory):
        allowed_move = pokemon_move_factory(name="tackle")
        allowed_move.allowed_users.add(user)
        other_move = pokemon_move_factory(name="scratch")

        client.force_login(user)
        response = client.get(reverse("poke_moves:moves-search"))

        assert allowed_move in response.context["moves"]
        assert other_move not in response.context["moves"]


class TestMoveDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse("poke_moves:move-detail", kwargs={"poke_move_name_or_id": "tackle"})
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_lookup_by_name(self, client, user, pokemon_move_factory):
        move = pokemon_move_factory(name="tackle")
        move.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse("poke_moves:move-detail", kwargs={"poke_move_name_or_id": "tackle"})
        )
        assert response.status_code == 200
        assert response.context["move"] == move

    @pytest.mark.django_db
    def test_lookup_by_id(self, client, user, pokemon_move_factory):
        move = pokemon_move_factory(move_id=33)
        move.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse("poke_moves:move-detail", kwargs={"poke_move_name_or_id": "33"})
        )
        assert response.status_code == 200
        assert response.context["move"] == move

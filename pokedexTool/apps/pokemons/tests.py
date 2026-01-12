import pytest
from django.urls import reverse
from django.db import IntegrityError

from apps.pokemons.models import (
    Pokemon,
    PokemonStat,
    PokemonTypeRelation,
    PokemonAbilityRelation,
)


class TestPokemonModel:
    @pytest.mark.django_db
    def test_create_pokemon(self, pokemon_factory):
        pokemon = pokemon_factory(name="pikachu", pokemon_id=25)
        assert pokemon.name == "pikachu"
        assert pokemon.pokemon_id == 25

    @pytest.mark.django_db
    def test_str_returns_name_and_id(self, pokemon):
        expected = f"{pokemon.name}_({pokemon.pokemon_id})"
        assert str(pokemon) == expected

    @pytest.mark.django_db
    def test_moves_list_parses_valid_string(self, pokemon_factory):
        pokemon = pokemon_factory(moves="['tackle', 'scratch']")
        assert pokemon.moves_list == ["tackle", "scratch"]

    @pytest.mark.django_db
    def test_moves_list_handles_empty_string(self, pokemon_factory):
        pokemon = pokemon_factory(moves="")
        assert pokemon.moves_list == []

    @pytest.mark.django_db
    def test_moves_list_handles_none(self, pokemon_factory):
        pokemon = pokemon_factory(moves=None)
        assert pokemon.moves_list == []

    @pytest.mark.django_db
    def test_moves_list_handles_malformed_string(self, pokemon_factory):
        pokemon = pokemon_factory(moves="invalid string")
        assert pokemon.moves_list == []

    @pytest.mark.django_db
    def test_ordering_by_pokemon_id(self, pokemon_factory):
        p3 = pokemon_factory(pokemon_id=3)
        p1 = pokemon_factory(pokemon_id=1)
        p2 = pokemon_factory(pokemon_id=2)
        pokemons = list(Pokemon.objects.all())
        assert pokemons == [p1, p2, p3]

    @pytest.mark.django_db
    def test_allowed_users_relationship(self, pokemon, user):
        pokemon.allowed_users.add(user)
        assert user in pokemon.allowed_users.all()


class TestPokemonStat:
    @pytest.mark.django_db
    def test_create_stat(self, pokemon):
        stat = PokemonStat.objects.create(
            pokemon=pokemon, stat_name="hp", base_stat=45, effort=0
        )
        assert stat.stat_name == "hp"
        assert stat.base_stat == 45

    @pytest.mark.django_db
    def test_unique_together_constraint(self, pokemon):
        PokemonStat.objects.create(
            pokemon=pokemon, stat_name="hp", base_stat=45, effort=0
        )
        with pytest.raises(IntegrityError):
            PokemonStat.objects.create(
                pokemon=pokemon, stat_name="hp", base_stat=50, effort=1
            )


class TestPokemonTypeRelation:
    @pytest.mark.django_db
    def test_create_type_relation(self, pokemon, pokemon_type):
        relation = PokemonTypeRelation.objects.create(
            pokemon=pokemon, type=pokemon_type, slot=1
        )
        assert relation.slot == 1
        assert relation.pokemon == pokemon
        assert relation.type == pokemon_type

    @pytest.mark.django_db
    def test_unique_together_constraint(self, pokemon, pokemon_type):
        PokemonTypeRelation.objects.create(pokemon=pokemon, type=pokemon_type, slot=1)
        with pytest.raises(IntegrityError):
            PokemonTypeRelation.objects.create(
                pokemon=pokemon, type=pokemon_type, slot=1
            )


class TestPokemonAbilityRelation:
    @pytest.mark.django_db
    def test_create_ability_relation(self, pokemon, pokemon_ability):
        relation = PokemonAbilityRelation.objects.create(
            pokemon=pokemon, ability=pokemon_ability, slot=1, is_hidden=False
        )
        assert relation.slot == 1
        assert relation.is_hidden is False

    @pytest.mark.django_db
    def test_hidden_ability(self, pokemon, pokemon_ability):
        relation = PokemonAbilityRelation.objects.create(
            pokemon=pokemon, ability=pokemon_ability, slot=3, is_hidden=True
        )
        assert relation.is_hidden is True


class TestPokemonSearchView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("pokemons:poke-search"))
        assert response.status_code == 302  # redirect to login

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("pokemons:poke-search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filters_by_allowed_users(self, client, user, pokemon_factory):
        allowed_pokemon = pokemon_factory(name="pikachu")
        allowed_pokemon.allowed_users.add(user)
        other_pokemon = pokemon_factory(name="bulbasaur")  # not allowed

        client.force_login(user)
        response = client.get(reverse("pokemons:poke-search"))

        assert allowed_pokemon in response.context["pokemons"]
        assert other_pokemon not in response.context["pokemons"]


class TestPokemonDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse("pokemons:poke-detail", kwargs={"pokemon_name_or_id": "pikachu"})
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_returns_404_for_nonexistent(self, client, user):
        client.force_login(user)
        response = client.get(
            reverse(
                "pokemons:poke-detail",
                kwargs={"pokemon_name_or_id": "nonexistentpokemon"},
            )
        )
        assert response.status_code == 404

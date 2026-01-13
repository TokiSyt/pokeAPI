import pytest
from django.urls import reverse

from apps.abilities.models import PokemonAbility


class TestPokemonAbilityModel:
    @pytest.mark.django_db
    def test_create_ability(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(name="overgrow", ability_id=65)
        assert ability.name == "overgrow"
        assert ability.ability_id == 65

    @pytest.mark.django_db
    def test_str_returns_name_and_id(self, pokemon_ability):
        expected = f"{pokemon_ability.name}_({pokemon_ability.ability_id})"
        assert str(pokemon_ability) == expected

    @pytest.mark.django_db
    def test_names_list_parses_valid(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(
            names="[{'language': 'en', 'name': 'Overgrow'}]"
        )
        assert ability.names_list == [{"language": "en", "name": "Overgrow"}]

    @pytest.mark.django_db
    def test_names_list_handles_empty(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(names="")
        assert ability.names_list == []

    @pytest.mark.django_db
    def test_names_list_handles_none(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(names=None)
        assert ability.names_list == []

    @pytest.mark.django_db
    def test_names_list_handles_malformed(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(names="invalid")
        assert ability.names_list == []

    @pytest.mark.django_db
    def test_effects_list_parses_valid(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(
            effect_entries="[{'effect': 'Powers up Grass-type moves'}]"
        )
        assert ability.effects_list == [{"effect": "Powers up Grass-type moves"}]

    @pytest.mark.django_db
    def test_effects_list_handles_malformed(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(effect_entries="invalid")
        assert ability.effects_list == []

    @pytest.mark.django_db
    def test_flavor_text_list_returns_second_entry(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(
            flavor_text_entries="[{'text': 'first'}, {'text': 'second'}, {'text': 'third'}]"
        )
        # Returns data[1:2], which is the second entry
        assert ability.flavor_text_list == [{"text": "second"}]

    @pytest.mark.django_db
    def test_flavor_text_list_handles_empty(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(flavor_text_entries="[]")
        assert ability.flavor_text_list == []

    @pytest.mark.django_db
    def test_pokemons_list_parses_valid(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(pokemons="['bulbasaur', 'ivysaur']")
        assert ability.pokemons_list == ["bulbasaur", "ivysaur"]

    @pytest.mark.django_db
    def test_pokemons_list_handles_malformed(self, pokemon_ability_factory):
        ability = pokemon_ability_factory(pokemons="invalid")
        assert ability.pokemons_list == []

    @pytest.mark.django_db
    def test_ordering_by_ability_id(self, pokemon_ability_factory):
        a3 = pokemon_ability_factory(ability_id=3)
        a1 = pokemon_ability_factory(ability_id=1)
        a2 = pokemon_ability_factory(ability_id=2)
        abilities = list(PokemonAbility.objects.all())
        assert abilities == [a1, a2, a3]

    @pytest.mark.django_db
    def test_allowed_users_relationship(self, pokemon_ability, user):
        pokemon_ability.allowed_users.add(user)
        assert user in pokemon_ability.allowed_users.all()


class TestAbilitySearchView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("abilities:ability-search"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("abilities:ability-search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filters_by_allowed_users(self, client, user, pokemon_ability_factory):
        allowed_ability = pokemon_ability_factory(name="overgrow")
        allowed_ability.allowed_users.add(user)
        other_ability = pokemon_ability_factory(name="blaze")

        client.force_login(user)
        response = client.get(reverse("abilities:ability-search"))

        assert allowed_ability in response.context["abilities"]
        assert other_ability not in response.context["abilities"]


class TestAbilityDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse(
                "abilities:ability-detail",
                kwargs={"poke_ability_name_or_id": "overgrow"},
            )
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_lookup_by_name(self, client, user, pokemon_ability_factory):
        ability = pokemon_ability_factory(name="overgrow")
        ability.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse(
                "abilities:ability-detail",
                kwargs={"poke_ability_name_or_id": "overgrow"},
            )
        )
        assert response.status_code == 200
        assert response.context["ability"] == ability

    @pytest.mark.django_db
    def test_lookup_by_id(self, client, user, pokemon_ability_factory):
        ability = pokemon_ability_factory(ability_id=65)
        ability.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse(
                "abilities:ability-detail", kwargs={"poke_ability_name_or_id": "65"}
            )
        )
        assert response.status_code == 200
        assert response.context["ability"] == ability

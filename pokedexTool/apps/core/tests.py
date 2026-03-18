import pytest
import requests
import responses

from apps.core.pokeapi_client import PokeAPIClient


class TestPokeAPIClient:
    @responses.activate
    def test_fetch_returns_parsed_json_on_200(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/tackle",
            json={"name": "tackle", "id": 33},
            status=200,
        )

        client = PokeAPIClient()
        result = client.fetch("move", "tackle")

        assert result == {"name": "tackle", "id": 33}

    @responses.activate
    def test_fetch_returns_none_on_404(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/nonexistent",
            json={"detail": "Not found."},
            status=404,
        )

        client = PokeAPIClient()
        result = client.fetch("move", "nonexistent")

        assert result is None

    @responses.activate
    def test_fetch_returns_none_on_network_error(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/tackle",
            body=requests.ConnectionError("Connection refused"),
        )

        client = PokeAPIClient()
        result = client.fetch("move", "tackle")

        assert result is None

    @responses.activate
    def test_fetch_retries_on_5xx_and_returns_none(self):
        for _ in range(3):
            responses.add(
                responses.GET,
                "https://pokeapi.co/api/v2/move/tackle",
                status=503,
            )

        client = PokeAPIClient(max_retries=2)
        result = client.fetch("move", "tackle")

        assert result is None
        assert len(responses.calls) == 3  # 1 initial + 2 retries

    def test_fetch_respects_timeout(self):
        import unittest.mock as mock

        client = PokeAPIClient(timeout=5.0)
        with mock.patch.object(client._session, "get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"name": "tackle"}
            client.fetch("move", "tackle")
            mock_get.assert_called_once_with(
                "https://pokeapi.co/api/v2/move/tackle", timeout=5.0
            )


class TestImportServiceRegistry:
    def test_register_and_import_for_model(self):
        from apps.core.import_service import _registry, import_for_model, register

        class FakeModel:
            pass

        @register(FakeModel)
        def fake_importer(name_or_id, user=None):
            return f"imported:{name_or_id}"

        try:
            result = import_for_model(FakeModel, "test-item")
            assert result == "imported:test-item"
        finally:
            _registry.pop(FakeModel, None)

    def test_import_for_model_raises_for_unregistered(self):
        import pytest

        from apps.core.import_service import import_for_model

        class UnregisteredModel:
            pass

        with pytest.raises(KeyError):
            import_for_model(UnregisteredModel, "anything")


# Fixture: realistic PokéAPI move response
TACKLE_API_RESPONSE = {
    "id": 33,
    "name": "tackle",
    "accuracy": 100,
    "power": 40,
    "pp": 35,
    "priority": 0,
    "effect_chance": None,
    "type": {"name": "normal", "url": "https://pokeapi.co/api/v2/type/1/"},
    "damage_class": {"name": "physical", "url": "..."},
    "generation": {"name": "generation-i", "url": "..."},
    "meta": {
        "category": {"name": "damage", "url": "..."},
        "ailment": {"name": "none", "url": "..."},
        "ailment_chance": 0,
    },
    "effect_entries": [
        {
            "effect": "Inflicts damage.",
            "short_effect": "Inflicts regular damage.",
            "language": {"name": "en", "url": "..."},
        }
    ],
    "flavor_text_entries": [
        {
            "flavor_text": "A physical attack.",
            "language": {"name": "en", "url": "..."},
        }
    ],
}


class TestMoveImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_creates_move_from_api_data(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/tackle",
            json=TACKLE_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.moves.models import PokemonMove

        move = import_for_model(PokemonMove, "tackle")

        assert move is not None
        assert move.name == "tackle"
        assert move.move_id == 33
        assert move.accuracy == 100
        assert move.power == 40
        assert move.pp == 35
        assert move.type == "normal"
        assert move.damage_class == "physical"
        assert move.generation == "generation-i"
        assert move.short_effect == "Inflicts regular damage."

    @pytest.mark.django_db
    @responses.activate
    def test_import_adds_user_to_allowed_users(self, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/tackle",
            json=TACKLE_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.moves.models import PokemonMove

        move = import_for_model(PokemonMove, "tackle", user=user)

        assert user in move.allowed_users.all()

    @pytest.mark.django_db
    @responses.activate
    def test_import_returns_none_on_api_failure(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/nonexistent",
            json={"detail": "Not found."},
            status=404,
        )

        from apps.core.import_service import import_for_model
        from apps.moves.models import PokemonMove

        result = import_for_model(PokemonMove, "nonexistent")

        assert result is None


class TestPokeDetailViewWithMove:
    @pytest.mark.django_db
    def test_existing_move_renders_200(self, client, user, pokemon_move_factory):
        move = pokemon_move_factory(name="tackle")
        move.allowed_users.add(user)
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse("poke_moves:move-detail", kwargs={"poke_move_name_or_id": "tackle"})
        )

        assert response.status_code == 200
        assert response.context["move"] == move

    @pytest.mark.django_db
    @responses.activate
    def test_missing_move_imports_then_renders(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/tackle",
            json=TACKLE_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse("poke_moves:move-detail", kwargs={"poke_move_name_or_id": "tackle"})
        )

        assert response.status_code == 200
        assert response.context["move"].name == "tackle"

    @pytest.mark.django_db
    @responses.activate
    def test_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/move/fakemove",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "poke_moves:move-detail", kwargs={"poke_move_name_or_id": "fakemove"}
            )
        )

        assert response.status_code == 404
        assert "error" in response.context


# ============== Issue #4: Ability + Generation ==============

OVERGROW_API_RESPONSE = {
    "id": 65,
    "name": "overgrow",
    "generation": {"name": "generation-iii", "url": "..."},
    "is_main_series": True,
    "names": [
        {"name": "Overgrow", "language": {"name": "en", "url": "..."}},
        {"name": "Engrais", "language": {"name": "fr", "url": "..."}},
    ],
    "effect_entries": [
        {
            "effect": "Powers up Grass-type moves.",
            "language": {"name": "en", "url": "..."},
        }
    ],
    "flavor_text_entries": [
        {
            "flavor_text": "Powers up Grass-type moves in a pinch.",
            "language": {"name": "en", "url": "..."},
        },
        {
            "flavor_text": "Powers up Grass-type moves in a pinch.",
            "language": {"name": "en", "url": "..."},
        },
    ],
    "pokemon": [
        {"pokemon": {"name": "bulbasaur", "url": "..."}},
        {"pokemon": {"name": "ivysaur", "url": "..."}},
    ],
}

GENERATION_I_API_RESPONSE = {
    "id": 1,
    "name": "generation-i",
    "names": [
        {"name": "Generation I", "language": {"name": "en", "url": "..."}},
    ],
    "main_region": {"name": "kanto", "url": "..."},
    "abilities": [{"name": "stench", "url": "..."}, {"name": "drizzle", "url": "..."}],
    "moves": [{"name": "pound", "url": "..."}, {"name": "karate-chop", "url": "..."}],
    "types": [{"name": "normal", "url": "..."}, {"name": "fire", "url": "..."}],
}


class TestAbilityImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_creates_ability_from_api_data(self, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/overgrow",
            json=OVERGROW_API_RESPONSE,
            status=200,
        )

        from apps.abilities.models import PokemonAbility
        from apps.core.import_service import import_for_model

        ability = import_for_model(PokemonAbility, "overgrow", user=user)

        assert ability is not None
        assert ability.name == "overgrow"
        assert ability.ability_id == 65
        assert ability.generation == "generation-iii"
        assert ability.is_main_series is True
        assert user in ability.allowed_users.all()


class TestGenerationImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_creates_generation_from_api_data(self, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/generation/generation-i",
            json=GENERATION_I_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.generations.models import Generation

        gen = import_for_model(Generation, "generation-i", user=user)

        assert gen is not None
        assert gen.name == "Generation I"
        assert gen.gen_id == 1
        assert gen.internal_name == "generation-i"
        assert gen.main_region == "kanto"
        assert user in gen.allowed_users.all()


class TestAbilityDetailView:
    @pytest.mark.django_db
    def test_existing_ability_with_user_renders_200(
        self, client, user, pokemon_ability_factory
    ):
        ability = pokemon_ability_factory(name="overgrow")
        ability.allowed_users.add(user)
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "abilities:ability-detail",
                kwargs={"poke_ability_name_or_id": "overgrow"},
            )
        )

        assert response.status_code == 200
        assert response.context["ability"] == ability

    @pytest.mark.django_db
    @responses.activate
    def test_ability_for_other_user_triggers_reimport(
        self, client, user, user_factory, pokemon_ability_factory
    ):
        other_user = user_factory()
        ability = pokemon_ability_factory(name="overgrow", ability_id=65)
        ability.allowed_users.add(other_user)
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/overgrow",
            json=OVERGROW_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "abilities:ability-detail",
                kwargs={"poke_ability_name_or_id": "overgrow"},
            )
        )

        assert response.status_code == 200
        ability.refresh_from_db()
        assert user in ability.allowed_users.all()

    @pytest.mark.django_db
    @responses.activate
    def test_missing_ability_imports_then_renders(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/overgrow",
            json=OVERGROW_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "abilities:ability-detail",
                kwargs={"poke_ability_name_or_id": "overgrow"},
            )
        )

        assert response.status_code == 200
        assert response.context["ability"].name == "overgrow"

    @pytest.mark.django_db
    @responses.activate
    def test_ability_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/fakeability",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "abilities:ability-detail",
                kwargs={"poke_ability_name_or_id": "fakeability"},
            )
        )

        assert response.status_code == 404
        assert "error" in response.context


class TestGenerationDetailView:
    @pytest.mark.django_db
    def test_existing_generation_with_user_renders_200(
        self, client, user, generation_factory
    ):
        gen = generation_factory(internal_name="generation-i")
        gen.allowed_users.add(user)
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "generations:gen-detail",
                kwargs={"generation_name_or_id": "generation-i"},
            )
        )

        assert response.status_code == 200
        assert response.context["generation"] == gen

    @pytest.mark.django_db
    @responses.activate
    def test_missing_generation_imports_then_renders(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/generation/generation-i",
            json=GENERATION_I_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "generations:gen-detail",
                kwargs={"generation_name_or_id": "generation-i"},
            )
        )

        assert response.status_code == 200
        assert response.context["generation"].internal_name == "generation-i"

    @pytest.mark.django_db
    @responses.activate
    def test_generation_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/generation/fakegeneration",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "generations:gen-detail",
                kwargs={"generation_name_or_id": "fakegeneration"},
            )
        )

        assert response.status_code == 404
        assert "error" in response.context


# ============== Issue #5: Type resource ==============

NORMAL_TYPE_API_RESPONSE = {
    "id": 1,
    "name": "normal",
    "generation": {"name": "generation-i", "url": "..."},
    "move_damage_class": {"name": "physical", "url": "..."},
    "moves": [{"name": "tackle", "url": "..."}, {"name": "scratch", "url": "..."}],
    "damage_relations": {
        "double_damage_from": [{"name": "fighting", "url": "..."}],
        "half_damage_from": [],
        "no_damage_from": [{"name": "ghost", "url": "..."}],
        "double_damage_to": [],
        "half_damage_to": [
            {"name": "rock", "url": "..."},
            {"name": "steel", "url": "..."},
        ],
        "no_damage_to": [{"name": "ghost", "url": "..."}],
    },
}


class TestTypeImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_creates_type_and_damage_relation(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/normal",
            json=NORMAL_TYPE_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.poke_types.models import PokemonType, TypeDamageRelation

        poke_type = import_for_model(PokemonType, "normal")

        assert poke_type is not None
        assert poke_type.name == "normal"
        assert poke_type.type_id == 1
        assert poke_type.generation == "generation-i"
        relation = TypeDamageRelation.objects.get(type=poke_type)
        assert "fighting" in relation.double_damage_from
        assert "ghost" in relation.no_damage_from
        assert "ghost" in relation.no_damage_to

    @pytest.mark.django_db
    @responses.activate
    def test_import_returns_none_on_api_failure(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/faketype",
            json={"detail": "Not found."},
            status=404,
        )

        from apps.core.import_service import import_for_model
        from apps.poke_types.models import PokemonType

        result = import_for_model(PokemonType, "faketype")

        assert result is None


class TestTypeDetailView:
    @pytest.mark.django_db
    def test_existing_type_renders_200_with_damage_relation(
        self, client, user, pokemon_type_factory, type_damage_relation_factory
    ):
        poke_type = pokemon_type_factory(name="normal")
        type_damage_relation_factory(type=poke_type)
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "poke_types:types-detail", kwargs={"poke_type_name_or_id": "normal"}
            )
        )

        assert response.status_code == 200
        assert response.context["type"] == poke_type
        assert response.context["type_relation"] is not None

    @pytest.mark.django_db
    @responses.activate
    def test_missing_type_imports_then_renders(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/normal",
            json=NORMAL_TYPE_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "poke_types:types-detail", kwargs={"poke_type_name_or_id": "normal"}
            )
        )

        assert response.status_code == 200
        assert response.context["type"].name == "normal"
        assert response.context["type_relation"] is not None

    @pytest.mark.django_db
    @responses.activate
    def test_type_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/faketype",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "poke_types:types-detail", kwargs={"poke_type_name_or_id": "faketype"}
            )
        )

        assert response.status_code == 404
        assert "error" in response.context

    @pytest.mark.django_db
    def test_no_allowed_users_check(
        self, client, user_factory, pokemon_type_factory, type_damage_relation_factory
    ):
        """check_user=False: any logged-in user can view any type without triggering reimport."""
        user_factory()
        user2 = user_factory()
        poke_type = pokemon_type_factory(name="normal")
        type_damage_relation_factory(type=poke_type)
        client.force_login(user2)

        from django.urls import reverse

        response = client.get(
            reverse(
                "poke_types:types-detail", kwargs={"poke_type_name_or_id": "normal"}
            )
        )

        assert response.status_code == 200
        assert response.context["type"] == poke_type


# ============== Issue #6: Location + Area ==============

PALLET_TOWN_API_RESPONSE = {
    "id": 1,
    "name": "pallet-town",
    "names": [{"name": "Pallet Town", "language": {"name": "en", "url": "..."}}],
    "region": {"name": "kanto", "url": "..."},
    "areas": [{"name": "pallet-town-area", "url": "..."}],
    "game_indices": [
        {"game_index": 1, "generation": {"name": "generation-i", "url": "..."}}
    ],
}

PALLET_TOWN_AREA_API_RESPONSE = {
    "id": 1,
    "name": "pallet-town-area",
    "names": [{"name": "Pallet Town Area", "language": {"name": "en", "url": "..."}}],
    "location": {"name": "pallet-town", "url": "..."},
    "encounter_method_rates": [
        {
            "encounter_method": {"name": "walk", "url": "..."},
            "version_details": [{"rate": 10, "version": {"name": "red", "url": "..."}}],
        }
    ],
    "pokemon_encounters": [
        {"pokemon": {"name": "pidgey", "url": "..."}},
        {"pokemon": {"name": "rattata", "url": "..."}},
    ],
}


class TestLocationImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_creates_location_from_api_data(self, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location/pallet-town",
            json=PALLET_TOWN_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.locations.models import Location

        location = import_for_model(Location, "pallet-town", user=user)

        assert location is not None
        assert location.location_name == "Pallet Town"
        assert location.internal_location_name == "pallet-town"
        assert location.location_id == 1
        assert location.region_name == "kanto"
        assert user in location.allowed_users.all()

    @pytest.mark.django_db
    @responses.activate
    def test_import_returns_none_on_api_failure(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location/fakelocation",
            json={"detail": "Not found."},
            status=404,
        )

        from apps.core.import_service import import_for_model
        from apps.locations.models import Location

        result = import_for_model(Location, "fakelocation")

        assert result is None


class TestAreaImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_area_creates_location_via_registry_when_missing(self, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location-area/pallet-town-area",
            json=PALLET_TOWN_AREA_API_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location/pallet-town",
            json=PALLET_TOWN_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.locations.models import Area, Location

        area = import_for_model(Area, "pallet-town-area", user=user)

        assert area is not None
        assert area.internal_area_name == "pallet-town-area"
        assert area.area_name == "Pallet Town Area"
        assert area.location.internal_location_name == "pallet-town"
        assert Location.objects.filter(internal_location_name="pallet-town").exists()
        assert user in area.allowed_users.all()

    @pytest.mark.django_db
    @responses.activate
    def test_import_area_uses_existing_location_without_reimport(
        self, user, location_factory
    ):
        existing_location = location_factory(internal_location_name="pallet-town")
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location-area/pallet-town-area",
            json=PALLET_TOWN_AREA_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.locations.models import Area

        area = import_for_model(Area, "pallet-town-area", user=user)

        assert area is not None
        assert area.location == existing_location
        assert len(responses.calls) == 1

    @pytest.mark.django_db
    @responses.activate
    def test_import_returns_none_on_api_failure(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location-area/fakearea",
            json={"detail": "Not found."},
            status=404,
        )

        from apps.core.import_service import import_for_model
        from apps.locations.models import Area

        result = import_for_model(Area, "fakearea")

        assert result is None


class TestLocationDetailView:
    @pytest.mark.django_db
    def test_existing_location_with_user_renders_200(
        self, client, user, location_factory
    ):
        location = location_factory(internal_location_name="pallet-town")
        location.allowed_users.add(user)
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "locations:locations-detail",
                kwargs={"location_name_or_id": "pallet-town"},
            )
        )

        assert response.status_code == 200
        assert response.context["location"] == location

    @pytest.mark.django_db
    @responses.activate
    def test_missing_location_imports_then_renders(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location/pallet-town",
            json=PALLET_TOWN_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "locations:locations-detail",
                kwargs={"location_name_or_id": "pallet-town"},
            )
        )

        assert response.status_code == 200
        assert response.context["location"].internal_location_name == "pallet-town"

    @pytest.mark.django_db
    @responses.activate
    def test_location_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location/fakelocation",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "locations:locations-detail",
                kwargs={"location_name_or_id": "fakelocation"},
            )
        )

        assert response.status_code == 404
        assert "error" in response.context


class TestAreaDetailView:
    @pytest.mark.django_db
    def test_existing_area_with_user_renders_200(
        self, client, user, area_factory, location_factory
    ):
        location = location_factory(internal_location_name="pallet-town")
        area = area_factory(internal_area_name="pallet-town-area", location=location)
        area.allowed_users.add(user)
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "locations:locations-area-detail",
                kwargs={"location_area_name_or_id": "pallet-town-area"},
            )
        )

        assert response.status_code == 200
        assert response.context["area"] == area

    @pytest.mark.django_db
    @responses.activate
    def test_missing_area_imports_then_renders(self, client, user, location_factory):
        location_factory(internal_location_name="pallet-town")
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location-area/pallet-town-area",
            json=PALLET_TOWN_AREA_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "locations:locations-area-detail",
                kwargs={"location_area_name_or_id": "pallet-town-area"},
            )
        )

        assert response.status_code == 200
        assert response.context["area"].internal_area_name == "pallet-town-area"

    @pytest.mark.django_db
    @responses.activate
    def test_area_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/location-area/fakearea",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse(
                "locations:locations-area-detail",
                kwargs={"location_area_name_or_id": "fakearea"},
            )
        )

        assert response.status_code == 404
        assert "error" in response.context


# ============== Issue #7: Pokemon ==============

BULBASAUR_TYPE_API_RESPONSE = {
    "id": 12,
    "name": "grass",
    "generation": {"name": "generation-i", "url": "..."},
    "move_damage_class": {"name": "special", "url": "..."},
    "moves": [{"name": "razor-leaf", "url": "..."}],
    "damage_relations": {
        "double_damage_from": [{"name": "fire", "url": "..."}],
        "half_damage_from": [{"name": "water", "url": "..."}],
        "no_damage_from": [],
        "double_damage_to": [{"name": "water", "url": "..."}],
        "half_damage_to": [{"name": "fire", "url": "..."}],
        "no_damage_to": [],
    },
}

OVERGROW_ABILITY_API_RESPONSE = {
    "id": 65,
    "name": "overgrow",
    "generation": {"name": "generation-iii", "url": "..."},
    "is_main_series": True,
    "names": [{"name": "Overgrow", "language": {"name": "en", "url": "..."}}],
    "effect_entries": [
        {
            "effect": "Powers up Grass-type moves.",
            "language": {"name": "en", "url": "..."},
        }
    ],
    "flavor_text_entries": [
        {
            "flavor_text": "Powers up Grass-type moves in a pinch.",
            "language": {"name": "en", "url": "..."},
        }
    ],
    "pokemon": [{"pokemon": {"name": "bulbasaur", "url": "..."}}],
}

BULBASAUR_API_RESPONSE = {
    "id": 1,
    "name": "bulbasaur",
    "height": 7,
    "weight": 69,
    "base_experience": 64,
    "sprites": {
        "front_default": "https://pokeapi.co/media/sprites/pokemon/1.png",
        "front_shiny": "https://pokeapi.co/media/sprites/pokemon/shiny/1.png",
    },
    "moves": [
        {"move": {"name": "razor-leaf", "url": "..."}},
        {"move": {"name": "tackle", "url": "..."}},
        {"move": {"name": "growl", "url": "..."}},
    ],
    "types": [{"slot": 1, "type": {"name": "grass", "url": "..."}}],
    "abilities": [
        {"ability": {"name": "overgrow", "url": "..."}, "is_hidden": False, "slot": 1}
    ],
    "stats": [
        {"base_stat": 45, "effort": 0, "stat": {"name": "hp", "url": "..."}},
        {"base_stat": 49, "effort": 0, "stat": {"name": "attack", "url": "..."}},
    ],
}


class TestPokemonImportService:
    @pytest.mark.django_db
    @responses.activate
    def test_import_creates_pokemon_with_relations_and_stats(
        self, user, pokemon_type_factory, pokemon_ability_factory
    ):
        pokemon_type_factory(name="grass")
        pokemon_ability_factory(name="overgrow")
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/bulbasaur",
            json=BULBASAUR_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.pokemons.models import (
            Pokemon,
            PokemonAbilityRelation,
            PokemonStat,
            PokemonTypeRelation,
        )

        pokemon = import_for_model(Pokemon, "bulbasaur", user=user)

        assert pokemon is not None
        assert pokemon.name == "bulbasaur"
        assert pokemon.pokemon_id == 1
        assert PokemonTypeRelation.objects.filter(pokemon=pokemon).count() == 1
        assert PokemonAbilityRelation.objects.filter(pokemon=pokemon).count() == 1
        assert PokemonStat.objects.filter(pokemon=pokemon).count() == 2
        assert user in pokemon.allowed_users.all()

    @pytest.mark.django_db
    @responses.activate
    def test_import_triggers_type_and_ability_import_via_registry_when_missing(
        self, user
    ):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/bulbasaur",
            json=BULBASAUR_API_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/grass",
            json=BULBASAUR_TYPE_API_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/overgrow",
            json=OVERGROW_ABILITY_API_RESPONSE,
            status=200,
        )

        from apps.core.import_service import import_for_model
        from apps.poke_types.models import PokemonType
        from apps.pokemons.models import Pokemon

        pokemon = import_for_model(Pokemon, "bulbasaur", user=user)

        assert pokemon is not None
        assert PokemonType.objects.filter(name="grass").exists()

    @pytest.mark.django_db
    @responses.activate
    def test_import_returns_none_on_api_failure(self):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/fakemon",
            json={"detail": "Not found."},
            status=404,
        )

        from apps.core.import_service import import_for_model
        from apps.pokemons.models import Pokemon

        result = import_for_model(Pokemon, "fakemon")

        assert result is None


class TestPokemonDetailViewNeedsReimport:
    @pytest.mark.django_db
    def test_needs_reimport_true_when_stats_missing(
        self, user, pokemon_factory, pokemon_type_factory, pokemon_ability_factory
    ):
        from apps.pokemons.models import PokemonAbilityRelation, PokemonTypeRelation
        from apps.pokemons.views import PokemonDetailView

        pokemon = pokemon_factory()
        pokemon.allowed_users.add(user)
        poke_type = pokemon_type_factory()
        ability = pokemon_ability_factory()
        PokemonTypeRelation.objects.create(pokemon=pokemon, type=poke_type, slot=1)
        PokemonAbilityRelation.objects.create(pokemon=pokemon, ability=ability, slot=1)
        # No stats — should trigger reimport

        from django.test import RequestFactory

        view = PokemonDetailView()
        request = RequestFactory().get("/")
        request.user = user

        assert view.needs_reimport(pokemon, request) is True

    @pytest.mark.django_db
    def test_needs_reimport_false_when_all_data_present(
        self, user, pokemon_factory, pokemon_type_factory, pokemon_ability_factory
    ):
        from apps.pokemons.models import (
            PokemonAbilityRelation,
            PokemonStat,
            PokemonTypeRelation,
        )
        from apps.pokemons.views import PokemonDetailView

        pokemon = pokemon_factory()
        pokemon.allowed_users.add(user)
        poke_type = pokemon_type_factory()
        ability = pokemon_ability_factory()
        PokemonTypeRelation.objects.create(pokemon=pokemon, type=poke_type, slot=1)
        PokemonAbilityRelation.objects.create(pokemon=pokemon, ability=ability, slot=1)
        PokemonStat.objects.create(
            pokemon=pokemon, stat_name="hp", base_stat=45, effort=0
        )

        from django.test import RequestFactory

        view = PokemonDetailView()
        request = RequestFactory().get("/")
        request.user = user

        assert view.needs_reimport(pokemon, request) is False


class TestPokemonDetailView:
    @pytest.mark.django_db
    def test_existing_pokemon_with_full_data_renders_200(
        self,
        client,
        user,
        pokemon_factory,
        pokemon_type_factory,
        pokemon_ability_factory,
    ):
        from apps.pokemons.models import (
            PokemonAbilityRelation,
            PokemonStat,
            PokemonTypeRelation,
        )

        pokemon = pokemon_factory(name="bulbasaur")
        pokemon.allowed_users.add(user)
        poke_type = pokemon_type_factory(name="grass")
        ability = pokemon_ability_factory(name="overgrow")
        PokemonTypeRelation.objects.create(pokemon=pokemon, type=poke_type, slot=1)
        PokemonAbilityRelation.objects.create(pokemon=pokemon, ability=ability, slot=1)
        PokemonStat.objects.create(
            pokemon=pokemon, stat_name="hp", base_stat=45, effort=0
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse("pokemons:poke-detail", kwargs={"pokemon_name_or_id": "bulbasaur"})
        )

        assert response.status_code == 200
        assert response.context["pokemon"] == pokemon
        assert response.context["type_relations"] is not None
        assert response.context["ability_relations"] is not None
        assert response.context["stats"] is not None

    @pytest.mark.django_db
    @responses.activate
    def test_missing_pokemon_full_import_flow(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/bulbasaur",
            json=BULBASAUR_API_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/type/grass",
            json=BULBASAUR_TYPE_API_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/ability/overgrow",
            json=OVERGROW_ABILITY_API_RESPONSE,
            status=200,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse("pokemons:poke-detail", kwargs={"pokemon_name_or_id": "bulbasaur"})
        )

        assert response.status_code == 200
        assert response.context["pokemon"].name == "bulbasaur"
        assert response.context["type_relations"].count() == 1
        assert response.context["ability_relations"].count() == 1
        assert response.context["stats"].count() == 2

    @pytest.mark.django_db
    @responses.activate
    def test_pokemon_import_failure_renders_404(self, client, user):
        responses.add(
            responses.GET,
            "https://pokeapi.co/api/v2/pokemon/fakemon",
            json={"detail": "Not found."},
            status=404,
        )
        client.force_login(user)

        from django.urls import reverse

        response = client.get(
            reverse("pokemons:poke-detail", kwargs={"pokemon_name_or_id": "fakemon"})
        )

        assert response.status_code == 404
        assert "error" in response.context

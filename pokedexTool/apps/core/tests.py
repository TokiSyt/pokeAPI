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

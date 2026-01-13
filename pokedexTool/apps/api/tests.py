import pytest
from django.urls import reverse


class TestTokenAuthentication:
    @pytest.mark.django_db
    def test_obtain_token(self, client, user):
        response = client.post(
            reverse("api:api-auth"),
            {"username": user.username, "password": "testpass123"},
        )
        assert response.status_code == 200
        assert "token" in response.json()

    @pytest.mark.django_db
    def test_obtain_token_invalid_credentials(self, client, user):
        response = client.post(
            reverse("api:api-auth"),
            {"username": user.username, "password": "wrongpassword"},
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_bearer_token_authentication(self, api_client, user_with_token):
        user, token = user_with_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.key}")
        response = api_client.get(reverse("api:api-poke-list"))
        assert response.status_code == 200


class TestAPIListEndpoints:
    @pytest.mark.django_db
    def test_pokemon_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-poke-list"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_pokemon_list_returns_data(self, api_client, pokemon):
        response = api_client.get(reverse("api:api-poke-list"))
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    @pytest.mark.django_db
    def test_moves_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-move-list"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_abilities_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-ability-list"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_types_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-types-list"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_locations_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-locations-list"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_areas_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-areas-list"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_generations_list_no_auth_required(self, api_client):
        response = api_client.get(reverse("api:api-generations-list"))
        assert response.status_code == 200


class TestAPIDetailEndpoints:
    @pytest.mark.django_db
    def test_pokemon_detail_requires_admin(self, authenticated_client, pokemon):
        response = authenticated_client.get(
            reverse("api:api-poke-detail", kwargs={"pokemon_name": pokemon.name})
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_pokemon_detail_admin_access(self, admin_client, pokemon):
        response = admin_client.get(
            reverse("api:api-poke-detail", kwargs={"pokemon_name": pokemon.name})
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_move_detail_requires_admin(self, authenticated_client, pokemon_move):
        response = authenticated_client.get(
            reverse(
                "api:api-move-detail",
                kwargs={"pokemon_move_name": pokemon_move.name},
            )
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_move_detail_admin_access(self, admin_client, pokemon_move):
        response = admin_client.get(
            reverse(
                "api:api-move-detail",
                kwargs={"pokemon_move_name": pokemon_move.name},
            )
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_ability_detail_requires_admin(self, authenticated_client, pokemon_ability):
        response = authenticated_client.get(
            reverse(
                "api:api-ability-detail",
                kwargs={"pokemon_ability_name": pokemon_ability.name},
            )
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_ability_detail_admin_access(self, admin_client, pokemon_ability):
        response = admin_client.get(
            reverse(
                "api:api-ability-detail",
                kwargs={"pokemon_ability_name": pokemon_ability.name},
            )
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_type_detail_requires_admin(self, authenticated_client, pokemon_type):
        response = authenticated_client.get(
            reverse(
                "api:api-type-detail",
                kwargs={"pokemon_type_name": pokemon_type.name},
            )
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_type_detail_admin_access(self, admin_client, pokemon_type):
        response = admin_client.get(
            reverse(
                "api:api-type-detail",
                kwargs={"pokemon_type_name": pokemon_type.name},
            )
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_location_detail_requires_admin(self, authenticated_client, location):
        response = authenticated_client.get(
            reverse(
                "api:api-location-detail",
                kwargs={"location_name": location.location_name},
            )
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_location_detail_admin_access(self, admin_client, location):
        response = admin_client.get(
            reverse(
                "api:api-location-detail",
                kwargs={"location_name": location.location_name},
            )
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_area_detail_requires_admin(self, authenticated_client, area):
        response = authenticated_client.get(
            reverse("api:api-area-detail", kwargs={"area_name": area.area_name})
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_area_detail_admin_access(self, admin_client, area):
        response = admin_client.get(
            reverse("api:api-area-detail", kwargs={"area_name": area.area_name})
        )
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_generation_detail_requires_admin(self, authenticated_client, generation):
        response = authenticated_client.get(
            reverse(
                "api:api-generation-detail",
                kwargs={"generation_name": generation.internal_name},
            )
        )
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_generation_detail_admin_access(self, admin_client, generation):
        response = admin_client.get(
            reverse(
                "api:api-generation-detail",
                kwargs={"generation_name": generation.internal_name},
            )
        )
        assert response.status_code == 200


class TestAPIPagination:
    @pytest.mark.django_db
    def test_pagination_present_in_response(self, api_client, pokemon_factory):
        # Create multiple pokemon
        for i in range(35):
            pokemon_factory(pokemon_id=i + 100)

        response = api_client.get(reverse("api:api-poke-list"))
        data = response.json()

        assert "count" in data
        assert "next" in data
        assert "previous" in data
        assert "results" in data
        assert len(data["results"]) == 30  # PAGE_SIZE is 30

    @pytest.mark.django_db
    def test_pagination_second_page(self, api_client, pokemon_factory):
        # Create multiple pokemon
        for i in range(35):
            pokemon_factory(pokemon_id=i + 100)

        response = api_client.get(reverse("api:api-poke-list") + "?page=2")
        data = response.json()

        assert len(data["results"]) == 5  # remaining items


class TestAPIMenuView:
    @pytest.mark.django_db
    def test_api_menu_requires_login(self, client):
        response = client.get(reverse("api:api-menu"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_api_menu_authenticated(self, client, user):
        client.force_login(user)
        response = client.get(reverse("api:api-menu"))
        assert response.status_code == 200

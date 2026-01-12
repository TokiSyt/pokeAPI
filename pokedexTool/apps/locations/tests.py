import pytest
from django.urls import reverse

from apps.locations.models import Location, Area


class TestLocationModel:
    @pytest.mark.django_db
    def test_create_location(self, location_factory):
        location = location_factory(
            internal_location_name="pallet-town", location_id=1
        )
        assert location.internal_location_name == "pallet-town"
        assert location.location_id == 1

    @pytest.mark.django_db
    def test_str_returns_name_and_id(self, location):
        expected = f"{location.internal_location_name}_{location.location_id}"
        assert str(location) == expected

    @pytest.mark.django_db
    def test_areas_list_parses_valid(self, location_factory):
        location = location_factory(areas="['route-1', 'route-2']")
        assert location.areas_list == ["route-1", "route-2"]

    @pytest.mark.django_db
    def test_areas_list_handles_malformed(self, location_factory):
        location = location_factory(areas="invalid")
        assert location.areas_list == []

    @pytest.mark.django_db
    def test_game_indices_list_parses_tuples(self, location_factory):
        location = location_factory(game_indices="[(1, 'red'), (2, 'blue')]")
        result = location.game_indices_list
        assert result == [(1, "red"), (2, "blue")]

    @pytest.mark.django_db
    def test_game_indices_list_single_tuple(self, location_factory):
        location = location_factory(game_indices="(1, 'red')")
        result = location.game_indices_list
        assert result == [(1, "red")]

    @pytest.mark.django_db
    def test_game_indices_list_handles_malformed(self, location_factory):
        location = location_factory(game_indices="invalid")
        assert location.game_indices_list == []

    @pytest.mark.django_db
    def test_ordering_by_location_id(self, location_factory):
        l3 = location_factory(location_id=3)
        l1 = location_factory(location_id=1)
        l2 = location_factory(location_id=2)
        locations = list(Location.objects.all())
        assert locations == [l1, l2, l3]

    @pytest.mark.django_db
    def test_allowed_users_relationship(self, location, user):
        location.allowed_users.add(user)
        assert user in location.allowed_users.all()


class TestAreaModel:
    @pytest.mark.django_db
    def test_create_area(self, area_factory):
        area = area_factory(internal_area_name="route-1-area", area_id=1)
        assert area.internal_area_name == "route-1-area"
        assert area.area_id == 1

    @pytest.mark.django_db
    def test_area_belongs_to_location(self, area):
        assert area.location is not None
        assert isinstance(area.location, Location)

    @pytest.mark.django_db
    def test_encounter_method_rates_list_parses_tuples(self, area_factory):
        area = area_factory(encounter_method_rates="[('walk', 10), ('surf', 5)]")
        result = area.encounter_method_rates_list
        assert result == [("walk", 10), ("surf", 5)]

    @pytest.mark.django_db
    def test_encounter_method_rates_list_handles_malformed(self, area_factory):
        area = area_factory(encounter_method_rates="invalid")
        assert area.encounter_method_rates_list == []

    @pytest.mark.django_db
    def test_pokemon_encounters_list_parses_valid(self, area_factory):
        area = area_factory(
            pokemon_encounters="[{'pokemon': 'pikachu', 'chance': 5}]"
        )
        assert area.pokemon_encounters_list == [{"pokemon": "pikachu", "chance": 5}]

    @pytest.mark.django_db
    def test_pokemon_encounters_list_handles_malformed(self, area_factory):
        area = area_factory(pokemon_encounters="invalid")
        assert area.pokemon_encounters_list == []

    @pytest.mark.django_db
    def test_ordering_by_area_id(self, location, area_factory):
        # Create areas with same location to test ordering
        a3 = area_factory(location=location, area_id=3)
        a1 = area_factory(location=location, area_id=1)
        a2 = area_factory(location=location, area_id=2)
        areas = list(Area.objects.filter(location=location))
        assert areas == [a1, a2, a3]

    @pytest.mark.django_db
    def test_allowed_users_relationship(self, area, user):
        area.allowed_users.add(user)
        assert user in area.allowed_users.all()


class TestLocationSearchView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(reverse("locations:locations-search"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_authenticated_access(self, client, user):
        client.force_login(user)
        response = client.get(reverse("locations:locations-search"))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_filters_by_allowed_users(self, client, user, location_factory):
        allowed_location = location_factory(internal_location_name="pallet-town")
        allowed_location.allowed_users.add(user)
        other_location = location_factory(internal_location_name="viridian-city")

        client.force_login(user)
        response = client.get(reverse("locations:locations-search"))

        assert allowed_location in response.context["locations"]
        assert other_location not in response.context["locations"]


class TestLocationDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse(
                "locations:locations-detail",
                kwargs={"location_name_or_id": "pallet-town"},
            )
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_lookup_by_name(self, client, user, location_factory):
        location = location_factory(internal_location_name="pallet-town")
        location.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse(
                "locations:locations-detail",
                kwargs={"location_name_or_id": "pallet-town"},
            )
        )
        assert response.status_code == 200
        assert response.context["location"] == location

    @pytest.mark.django_db
    def test_lookup_by_id(self, client, user, location_factory):
        location = location_factory(location_id=1)
        location.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse("locations:locations-detail", kwargs={"location_name_or_id": "1"})
        )
        assert response.status_code == 200
        assert response.context["location"] == location


class TestAreaDetailView:
    @pytest.mark.django_db
    def test_requires_login(self, client):
        response = client.get(
            reverse(
                "locations:locations-area-detail", kwargs={"location_area_name_or_id": "route-1"}
            )
        )
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_lookup_by_name(self, client, user, area_factory):
        area = area_factory(internal_area_name="route-1-area")
        area.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse(
                "locations:locations-area-detail",
                kwargs={"location_area_name_or_id": "route-1-area"},
            )
        )
        assert response.status_code == 200
        assert response.context["area"] == area

    @pytest.mark.django_db
    def test_lookup_by_id(self, client, user, area_factory):
        area = area_factory(area_id=1)
        area.allowed_users.add(user)
        client.force_login(user)
        response = client.get(
            reverse("locations:locations-area-detail", kwargs={"location_area_name_or_id": "1"})
        )
        assert response.status_code == 200
        assert response.context["area"] == area

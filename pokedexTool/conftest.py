import factory
import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.abilities.models import PokemonAbility
from apps.generations.models import Generation
from apps.locations.models import Area, Location
from apps.moves.models import PokemonMove
from apps.poke_types.models import PokemonType, TypeDamageRelation
from apps.pokemons.models import (
    Pokemon,
    PokemonStat,
)

User = get_user_model()


# ============== User Factories ==============


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"testuser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.set_password(extracted or "testpass123")
        obj.save()


class AdminUserFactory(UserFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    is_staff = True
    is_superuser = True


# ============== Pokemon Factories ==============


class PokemonTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PokemonType

    name = factory.Sequence(lambda n: f"type{n}")
    type_id = factory.Sequence(lambda n: n + 1)
    generation = "generation-i"
    move_damage_class = "physical"
    moves = "['tackle', 'scratch']"


class PokemonAbilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PokemonAbility

    name = factory.Sequence(lambda n: f"ability{n}")
    ability_id = factory.Sequence(lambda n: n + 1)
    generation = "generation-i"
    is_main_series = True
    names = "[{'language': 'en', 'name': 'Test Ability'}]"
    effect_entries = "[{'effect': 'Test effect', 'language': 'en'}]"
    flavor_text_entries = "[{'flavor_text': 'First', 'language': 'en'}, {'flavor_text': 'Second', 'language': 'en'}]"
    pokemons = "['pikachu', 'bulbasaur']"


class PokemonMoveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PokemonMove

    name = factory.Sequence(lambda n: f"move{n}")
    move_id = factory.Sequence(lambda n: n + 1)
    accuracy = 100
    power = 50
    pp = 20
    priority = 0
    effect_chance = None
    damage_class = "physical"
    type = "normal"
    generation = "generation-i"
    category = "damage"
    ailment = "none"
    ailment_chance = 0
    short_effect = "Test short effect"
    effect = "Test effect description"
    flavor_text = "Test flavor text"


class PokemonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pokemon

    pokemon_id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f"pokemon{n}")
    height = 10
    weight = 100
    base_experience = 64
    moves = "['tackle', 'scratch']"


class PokemonStatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PokemonStat

    pokemon = factory.SubFactory(PokemonFactory)
    stat_name = "hp"
    base_stat = 45
    effort = 0


class TypeDamageRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TypeDamageRelation

    type = factory.SubFactory(PokemonTypeFactory)
    no_damage_to = ""
    half_damage_to = "rock, steel"
    double_damage_to = "grass, ice"
    no_damage_from = ""
    half_damage_from = "grass, ice"
    double_damage_from = "water, ground"


# ============== Location Factories ==============


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    location_id = factory.Sequence(lambda n: n + 1)
    internal_location_name = factory.Sequence(lambda n: f"location-{n}")
    location_name = factory.Sequence(lambda n: f"Location {n}")
    region_name = "kanto"
    areas = "['area-1', 'area-2']"
    game_indices = "[(1, 'red'), (2, 'blue')]"


class AreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Area

    area_id = factory.Sequence(lambda n: n + 1)
    location = factory.SubFactory(LocationFactory)
    internal_area_name = factory.Sequence(lambda n: f"area-{n}")
    area_name = factory.Sequence(lambda n: f"Area {n}")
    encounter_method_rates = "[('walk', 10)]"
    pokemon_encounters = "[{'pokemon': 'pikachu', 'chance': 5}]"


# ============== Generation Factory ==============


class GenerationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Generation

    gen_id = factory.Sequence(lambda n: n + 1)
    internal_name = factory.Sequence(lambda n: f"generation-{n}")
    name = factory.Sequence(lambda n: f"Generation {n}")
    main_region = "kanto"
    abilities = "['overgrow', 'blaze', 'torrent']"
    moves = "['tackle', 'pound']"
    types = "['normal', 'fire', 'water']"


# ============== Pytest Fixtures ==============


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return AdminUserFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def user_with_token(db):
    user = UserFactory()
    token, _ = Token.objects.get_or_create(user=user)
    return user, token


@pytest.fixture
def pokemon(db):
    return PokemonFactory()


@pytest.fixture
def pokemon_type(db):
    return PokemonTypeFactory()


@pytest.fixture
def pokemon_ability(db):
    return PokemonAbilityFactory()


@pytest.fixture
def pokemon_move(db):
    return PokemonMoveFactory()


@pytest.fixture
def location(db):
    return LocationFactory()


@pytest.fixture
def area(db):
    return AreaFactory()


@pytest.fixture
def generation(db):
    return GenerationFactory()


@pytest.fixture
def type_damage_relation(db):
    return TypeDamageRelationFactory()


# Factory fixtures for creating multiple instances
@pytest.fixture
def user_factory(db):
    return UserFactory


@pytest.fixture
def admin_user_factory(db):
    return AdminUserFactory


@pytest.fixture
def pokemon_factory(db):
    return PokemonFactory


@pytest.fixture
def pokemon_type_factory(db):
    return PokemonTypeFactory


@pytest.fixture
def pokemon_ability_factory(db):
    return PokemonAbilityFactory


@pytest.fixture
def pokemon_move_factory(db):
    return PokemonMoveFactory


@pytest.fixture
def location_factory(db):
    return LocationFactory


@pytest.fixture
def area_factory(db):
    return AreaFactory


@pytest.fixture
def generation_factory(db):
    return GenerationFactory

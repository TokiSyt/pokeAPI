# Pokédex Tool

A Django-based web application that integrates with PokéAPI to let users search, view, and manage Pokémon data with a personal Pokédex.

## Features

- **Personal Pokédex** - Maintain your own collection of Pokémon
- **Search** - Find Pokémon, Moves, Abilities, Types, Locations, and Generations by name or ID
- **Auto-fetch** - Data not in database is automatically fetched from PokéAPI and stored
- **REST API** - Token-based API for programmatic access
- **Docker Support** - Ready for containerized deployment with PostgreSQL

## Tech Stack

- Django 5.x
- Django REST Framework
- PostgreSQL (Docker) / SQLite (local)
- Tailwind CSS
- pytest

## Quick Start

### Local Development (SQLite)

```bash
cd pokedexTool
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Docker Development (PostgreSQL)

```bash
cd pokedexTool
cp .env.example .env     # Configure environment
make upbuild             # Build and start containers
make migrate             # Run migrations
make superuser           # Create admin user
```

See `make help` for all available commands.

## API

Base URL: `/api/`

**Authentication:** POST to `/api/auth/` with username/password, then use `Authorization: Bearer <token>` header.

**Endpoints:**
- `/api/pokemons/` - Pokémon data
- `/api/moves/` - Move data
- `/api/abilities/` - Ability data
- `/api/types/` - Type data
- `/api/locations/` - Location data
- `/api/areas/` - Area data
- `/api/generations/` - Generation data

## Testing

```bash
# Local
pytest

# Docker
make test

# With coverage
make test-cov
```

## Development

```bash
# Linting and formatting
make ruff

# Tailwind CSS watch mode
npm run watch:css
```

## License

MIT License - for educational purposes.

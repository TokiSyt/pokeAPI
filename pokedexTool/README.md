Pokedex Tool

A Django-based web application that integrates with the PokeAPI to allow users to search, view, and manage Pokémon data.
Users can maintain their own Pokédex, search for Pokémon by name or ID, and view details including types, abilities, and stats.


Installation
Prerequisites

Python 3.10+

Virtualenv or Conda

Git

Steps

Clone the repository:

git clone https://github.com/your-username/pokedex-tool.git
cd pokedex-tool


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver

Usage

Log in with your account.

Search for a Pokémon by name or ID.

If not in the database, it will be fetched from PokeAPI and stored.

Pokémon details and stats are displayed, and the Pokémon becomes visible in your personal Pokédex.

Development Notes

Pokémon data is stored in the database and associated with the users who have searched for them.

To pre-populate the database with all Pokémon, a management command is available (disabled by default to avoid hitting PokeAPI rate limits).

Roadmap

Add pagination and filters to the Pokédex view.

Improve error handling and logging.

Add tests with pytest and DRF test cases.

Support caching or async tasks (Celery/Redis) for bulk imports.

Extend support for moves and evolution chains.

License

This project is for educational purposes. You may use, modify, and distribute it under the MIT License.Installation
Prerequisites

Python 3.10+

Virtualenv or Conda

Git

Steps

Clone the repository:

git clone https://github.com/your-username/pokedex-tool.git
cd pokedex-tool


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run a local development server:

python manage.py runserver

Usage

Log in with your account.

Search for a Pokémon by name or ID.

If not in the database, it will be fetched from PokeAPI and stored.

Pokémon details and stats are displayed, and the Pokémon becomes visible in your personal Pokédex.

Development Notes

Pokémon data is stored in the database and associated with the users who have searched for them.

To pre-populate the database with all Pokémon, a management command is available (disabled by default to avoid hitting PokeAPI rate limits).

Roadmap

Add pagination and filters to the Pokédex view.

Improve error handling and logging.

Add tests with pytest and DRF test cases.

Support caching or async tasks (Celery/Redis) for bulk imports.

Extend support for moves, evolution chains and areas.


License

This project is for educational purposes. You may use, modify, and distribute it under the MIT License.
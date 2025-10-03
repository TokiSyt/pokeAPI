# Pokédex Tool

A Django-based web application that integrates with the PokéAPI
 to let users search, view, and manage Pokémon data.

# Features:

Maintain your own personal Pokédex

Search Pokémon by name or ID

View details such as types, abilities, and stats


# Installation Prerequisites

Python 3.10+

Virtualenv or Conda

Git

Clone the repository

git clone https://github.com/your-username/pokedex-tool.git <br>
cd pokedex-tool

Create and activate a virtual environment

Linux/macOS:
python -m venv venv <br>
source venv/bin/activate

Windows:
python -m venv venv <br>
venv\Scripts\activate

# 

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser


Run the development server

python manage.py runserver

# Usage

Log in with your account

Search for a Pokémon by name or ID

If not found in the database, it will be fetched from PokéAPI and stored

View detailed stats, abilities, and add Pokémon to your personal Pokédex

# Development Notes

Pokémon data is stored in the general database and their visualization is tied to the users who searched it

A multi-thread management command exists to pre-populate the database with all Pokémon for the list in pokedexTool\apps\pokemons\services\pokemon_import.py

Disabled by default (to avoid hitting API rate limits). Use at your own risk.

# Roadmap

 Add pagination and filters to the Pokédex view

 Improve error handling and logging

 Add tests with pytest and DRF test cases

 Extend support for moves, evolution chains, and areas

# License

This project is for educational purposes.
You may use, modify, and distribute it under the MIT License.

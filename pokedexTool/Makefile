DOCKER_COMPOSE = docker-compose
DOCKER_WEB = $(DOCKER_COMPOSE) exec web
MANAGE = $(DOCKER_WEB) python manage.py

.PHONY: help
help:
	@echo "Docker:  build | up | upd | upbuild | down | restart | logs | clean"
	@echo "Django:  migrate | makemigrations | superuser | shell | collectstatic"
	@echo "CSS:     css | css-watch | css-install"
	@echo "Dev:     bash | dbshell | test | ps"

# Docker
.PHONY: build up upd upbuild down restart logs logs-web clean
build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

upd:
	$(DOCKER_COMPOSE) up -d

upbuild:
	$(DOCKER_COMPOSE) up --build

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f

logs-web:
	$(DOCKER_COMPOSE) logs -f web

clean:
	$(DOCKER_COMPOSE) down -v

# Django
.PHONY: migrate makemigrations superuser shell collectstatic check
migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

collectstatic:
	$(MANAGE) collectstatic --noinput

check:
	$(MANAGE) check

# Dev
.PHONY: bash dbshell test test-cov ps
bash:
	$(DOCKER_WEB) bash

dbshell:
	$(DOCKER_COMPOSE) exec db psql -U pokeapi_user -d pokeapi

test:
	$(DOCKER_WEB) pytest

test-cov:
	$(DOCKER_WEB) pytest --cov=apps --cov-report=term-missing

ps:
	$(DOCKER_COMPOSE) ps

# CSS (Tailwind)
.PHONY: css css-watch css-install
css-install:
	npm install

css:
	npm run build:css

css-watch:
	npm run watch:css

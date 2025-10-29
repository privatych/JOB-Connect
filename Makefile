.PHONY: build up up-prod logs logs-prod down down-prod ps

build:
	docker compose -f docker-compose.yml build

up:
	docker compose -f docker-compose.yml up -d --build

logs:
	docker compose -f docker-compose.yml logs -f

down:
	docker compose -f docker-compose.yml down

up-prod:
	docker compose -f docker-compose.prod.yml up -d --build

logs-prod:
	docker compose -f docker-compose.prod.yml logs -f

down-prod:
	docker compose -f docker-compose.prod.yml down

ps:
	docker compose ps

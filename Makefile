export PYTHONPATH=$(shell pwd)/
export PYTHONDONTWRITEBYTECODE=1

run:
	docker-compose up --build

test:
	docker-compose up --build -d
	docker-compose exec web bash -c "cd b3_inoa && pytest . --disable-warnings"

down: ## down all containers
	docker-compose down -v

isort: # sort imports PEP8
	docker-compose run --rm web bash -c "isort ."

black: # linter to organize readable code
	docker-compose run --rm web bash -c "python -m black ."
	
clear:
	docker-compose down -v
	docker system prune -af
	docker volume prune -f

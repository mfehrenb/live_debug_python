build:
		docker-compose build

test:
		docker-compose run app sh -c "pytest . && flake8 ."
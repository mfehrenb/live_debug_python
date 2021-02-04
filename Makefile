build:
		docker-compose build

test:
		docker-compose run app sh -c "pytest . && flake8 ."

migrations:
		docker-compose run app sh -c "python3 manage.py makemigrations"

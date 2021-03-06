build:
		docker-compose build

test:
		docker-compose run app sh -c "pytest . && flake8 ."

migrations:
		docker-compose run app sh -c "python3 manage.py makemigrations"

local:
		docker-compose up

local_db_only:
		docker-compose up db

superuser:
		docker-compose run app sh -c "python3 manage.py createsuperuser"


build:
	docker-compose build

up:
	docker-compose up --build -d

down:
	docker-compose down --rmi all
up:
	docker-compose up -d db
	sleep 5
	docker-compose up -d app

down:
	docker-compose down

stats:
	docker-compose stats

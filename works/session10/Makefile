
pull: start
	docker compose exec ollama ollama pull smollm:135m-base-v0.2-q2_K

start:
	docker compose up -d --build --force-recreate --remove-orphans

run: start pull
	docker compose restart
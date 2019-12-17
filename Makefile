up:
	@docker-compose up -d

down:
	@docker-compose down

ps:
	@docker-compose ps

logs:
	@docker-compose logs -f git

exec:
	@docker exec -it git-sync-p_git_1 sh
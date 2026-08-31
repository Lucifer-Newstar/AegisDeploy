# =============================================================================
# AegisSRE — developer task runner
#   make help       list targets
#   make infra-up   start the local stack (Postgres, Redis, observability)
#   make infra-down stop and remove the local stack (volumes included)
#   make lint       validate YAML files locally (needs python3 + pyyaml)
#   make docs       serve the docs locally
# =============================================================================

.PHONY: help infra-up infra-down infra-logs lint docs

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

infra-up: ## Start local dependencies (Postgres, Redis, Prometheus, Grafana, Loki, Tempo, OTel)
	docker compose up -d --wait

infra-down: ## Stop and remove the local stack (including data volumes)
	docker compose down -v

infra-logs: ## Follow logs of the local stack
	docker compose logs -f

lint: ## Validate all YAML files (docker compose config + python yaml parse)
	@echo "→ compose config"
	@docker compose config --quiet 2>/dev/null || python3 scripts/validate_yaml.py
	@echo "→ yaml files"
	@python3 scripts/validate_yaml.py

docs: ## Serve docs locally
	@python3 -m http.server 8000 -d docs 2>/dev/null || python3 -m http.server 8000

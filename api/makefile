## core
# variables
DOCKER_COMPOSE := docker compose -f docker-compose.yml -p trade
UV := uv
UVX := $(UV)x
SERVER_CONTAINER := server-trade
# Tag for the prod image; override with TAG=<repository>:<tag>.
TAG ?= trade-api:prod
# Registry the push-prod target logs in to; override with REGISTRY=<host> (default GitHub Container Registry).
REGISTRY ?= ghcr.io
# ``-t`` only when make itself has a terminal. seed:default prompts for a
# password when PASSWORD= is absent, and turning echo off needs a tty; CI has
# none and passes PASSWORD=, where asking docker for a tty is a hard error.
TTY_FLAG := $(shell [ -t 0 ] && echo -t)

# phony targets
.PHONY: clean-host clean-volumes clean-all ps build build-prod push-prod up stop down restart install install-dev check check-ci run export add logs migrate seed\:default setup help

## operation
# system cleanup
clean-host: # Prune all unused Docker data on the host
	docker system prune --all --force
	docker volume prune --all --force
	docker buildx prune --all --force
	docker builder prune --all --force

clean-volumes: # Remove this project's volumes (db)
	$(DOCKER_COMPOSE) down -v

clean-all: # Stop containers, remove volumes & images
	$(DOCKER_COMPOSE) down -v --rmi all

# docker control
ps: # List containers
	$(DOCKER_COMPOSE) ps -a

build: # Build Docker images
	$(DOCKER_COMPOSE) build

build-prod: # Build the prod image (arm64). TAG=<repository>:<tag> optional, default trade-api:prod
	docker buildx build --platform linux/arm64 --target prod \
		--build-arg ENV=prod --build-arg WORK_DIR=/workdir --build-arg INSTALL_DIR=/opt/install \
		--build-arg PW_DIR=/pwdir -t $(TAG) --load .

push-prod: # Build, then push the prod image to a registry. TAG=<registry>/<repository>:<tag> required; REGISTRY= optional (default ghcr.io); log in first with `docker login`
	@case "$(TAG)" in */*:*) ;; *) echo "set TAG=<registry>/<repository>:<tag> (e.g. $(REGISTRY)/<owner>/trade-api:<tag>)"; exit 1;; esac
	$(MAKE) build-prod
	docker push $(TAG)

up: # Start containers
	$(DOCKER_COMPOSE) up -d

stop: # Stop containers
	$(DOCKER_COMPOSE) stop

down: # Remove containers
	$(DOCKER_COMPOSE) down

restart: # Restart containers
	make stop
	make build
	make up

logs: # Show live logs
	$(DOCKER_COMPOSE) logs -f

# python tools (uv)
install: # Install all dependencies
	$(UV) sync --all-groups

install-dev: # Add development dependencies
	$(UV) add --dev ruff ty

check: # Run lint + type checks
	make install
	$(UVX) ruff check --fix
	$(UV) run ty check

check-ci: # Run lint + type checks without fixing anything. For CI.
	make install
	$(UVX) ruff check
	$(UV) run ty check

run: # Run FastAPI dev server
	make check
	$(UV) run uvicorn src.main:app --reload --loop uvloop

export: # Export requirements.txt
	$(UV) export --format requirements-txt --output requirements.txt

# git
add: # Stage all changes
	git add .

# database scripts
migrate: # Run database migrations
	docker exec $(SERVER_CONTAINER) python -m scripts.migrate

# seed:default takes its inputs the way auth's does: EMAIL= is required and is
# refused here, before docker is reached; the rest are optional. The password
# is never a setting and has no default — omitted, the seeder prompts for it on
# stdin, which keeps it out of shell history and out of ps.
# scripts/seed.py says what each does.
SEED_REQUIRED := EMAIL
SEED_GUARD = $(foreach v,$(1),$(if $($(v)),,$(error $(v) is required — e.g. make $@ EMAIL=admin@example.com. Tip: `export` the ones that never change once, since make reads environment variables as make variables)))
SEED_ARGS = --email "$(EMAIL)" $(if $(USERNAME),--username "$(USERNAME)") $(if $(PASSWORD),--password "$(PASSWORD)") $(if $(NAME),--name "$(NAME)")

seed\:default: # Bootstrap the deployment's own data, once per deployment: the SUPERADMIN account. EMAIL=<address> required. USERNAME=<handle> optional — omitted, drawn from the local part of EMAIL. NAME=<display name> optional — omitted, drawn from USERNAME. PASSWORD=<password> optional — omitted, prompted on stdin; there is no default password and no setting to fall back on. A re-run reuses the account that exists and never changes its password
	@$(call SEED_GUARD,$(SEED_REQUIRED))
	docker exec -i $(TTY_FLAG) $(SERVER_CONTAINER) python -m scripts.seed_default $(SEED_ARGS)

# The seed runs from the recipe rather than as a prerequisite, and must stay
# that way. GNU Make 3.81 stores ``seed\:default`` in a prerequisite list
# verbatim, backslash and all, so it never matches the target of that name —
# and because .PHONY carries the same escaped spelling, make resolves the
# phantom node by doing nothing instead of failing. On the command line the
# escape resolves, so a sub-make gets it right.
setup: migrate # Run migrations then seed:default — its variables (EMAIL= required, the rest optional) are passed through
	@$(MAKE) --no-print-directory seed:default

# help
# The name class carries ``\:`` so seed:default is listed too: its name is
# escaped for GNU Make 3.81 (see the note above ``setup``), and a plain
# ``[a-zA-Z_-]+:`` stops dead at the backslash. The backslash is stripped for
# display: it is make's escape, not part of the name.
help:
	@grep -E '^[a-zA-Z_-]+(\\:[a-zA-Z_-]+)*:.*#' $(MAKEFILE_LIST) | awk 'match($$0, /^[a-zA-Z_-]+(\\:[a-zA-Z_-]+)*/) { name = substr($$0, 1, RLENGTH); gsub(/\\/, "", name); help = $$0; sub(/^[^#]*#/, "", help); printf "\033[36m%-20s\033[0m %s\n", name, help }'

## core
# variables
# This file owns no logic. Each target hands off to the stack that does:
# api/makefile for Python and Docker, ui/package.json for the SPA.
#
# Variables typed on the command line reach the sub-make on their own — GNU make
# forwards command-line overrides through MAKEFLAGS — so the seed target takes
# its inputs the way api/makefile documents them:
#
#   make api-seed-default EMAIL=admin@example.com
#
# and the password prompt still reads from the terminal. Run
# `make -C api help` for the full seed documentation.
API := api
UI := ui
BUN := bun
UI_PORT := 5173

# phony targets
.PHONY: check setup down restart clean help \
	api-check api-check-ci api-run api-up api-stop api-down api-build api-build-prod api-push-prod api-restart api-ps api-logs \
	api-migrate api-install api-export api-clean-all api-clean-volumes api-clean-host \
	api-seed-default api-setup \
	ui-install ui-dev ui-down ui-restart ui-build ui-check ui-format

## both stacks
check: api-check ui-check # Lint + typecheck both stacks

setup: api-setup # Run API migrations, then seed:default (EMAIL= required)

down: api-down ui-down # Stop both stacks: remove the API containers, kill the UI dev server

restart: api-restart ui-restart # Restart both stacks: rebuild + restart the API containers, then relaunch the UI dev server

clean: api-clean-volumes # Remove the project's volumes (db)

## api — delegates to api/makefile
api-check: # Lint + typecheck the API
	$(MAKE) -C $(API) check

api-check-ci: # Lint + typecheck the API without fixing anything (for CI)
	$(MAKE) -C $(API) check-ci

api-run: # Run the API dev server on the host
	$(MAKE) -C $(API) run

api-up: # Start the API and database containers
	$(MAKE) -C $(API) up

api-stop: # Stop the API containers
	$(MAKE) -C $(API) stop

api-down: # Remove the API containers
	$(MAKE) -C $(API) down

api-build: # Build the API Docker images
	$(MAKE) -C $(API) build

api-build-prod: # Build the prod API image (TAG=<repository>:<tag> optional)
	$(MAKE) -C $(API) build-prod

api-push-prod: # Build and push the prod API image (TAG=<registry>/<repository>:<tag> required)
	$(MAKE) -C $(API) push-prod

api-restart: # Stop, rebuild, and start the API containers
	$(MAKE) -C $(API) restart

api-ps: # List the API containers
	$(MAKE) -C $(API) ps

api-logs: # Follow the API container logs
	$(MAKE) -C $(API) logs

api-migrate: # Run database migrations
	$(MAKE) -C $(API) migrate

api-install: # Install API dependencies
	$(MAKE) -C $(API) install

api-export: # Export requirements.txt
	$(MAKE) -C $(API) export

api-clean-all: # Stop containers, remove volumes and images
	$(MAKE) -C $(API) clean-all

api-clean-volumes: # Remove the project's volumes (db)
	$(MAKE) -C $(API) clean-volumes

api-clean-host: # Prune all unused Docker data on the host
	$(MAKE) -C $(API) clean-host

# seed — colon-named upstream (seed:default); dashed here so the name needs no escaping
api-seed-default: # Bootstrap the deployment's SUPERADMIN account (EMAIL= required)
	$(MAKE) -C $(API) seed:default

api-setup: # Migrate, then seed:default
	$(MAKE) -C $(API) setup

## ui — delegates to ui/package.json
ui-install: # Install UI dependencies
	$(BUN) install --cwd $(UI)

ui-dev: # Run the UI dev server on 5173 (formats and typechecks first)
	$(BUN) run --cwd $(UI) web:dev

ui-down: # Stop the UI dev server (kill whatever listens on UI_PORT)
	@pids=$$(lsof -tiTCP:$(UI_PORT) -sTCP:LISTEN); [ -n "$$pids" ] && kill $$pids || true

ui-restart: # Wipe node_modules + bun.lock, reinstall, then run the dev server
	$(BUN) run --cwd $(UI) web:restart

ui-build: # Build the UI for production
	$(BUN) run --cwd $(UI) web:build

ui-check: # Typecheck the UI
	$(BUN) run --cwd $(UI) web:chk

ui-format: # Format the UI sources
	$(BUN) run --cwd $(UI) web:fmt

# help
help:
	@grep -E '^[a-zA-Z_-]+:.*?#' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?#"}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

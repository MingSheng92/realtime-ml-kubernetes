####################################################################################
## Kind Cluster
####################################################################################
start-kind-cluster: ## start kind cluster
	@echo "Starting cluster"
	docker start rwml-34fa-control-plane
	@echo "Kind cluster started"

stop-kind-cluster: ## stop kind cluster
	@echo "Stopping cluster"
	docker stop rwml-34fa-control-plane
	@echo "Kind cluster stopped"

####################################################################################
## Kafka-ui
####################################################################################
port-forward-ui: ## port forward kafka-ui
	@echo "Port forwarding kafka-ui"
	kubectl -n kafka port-forward svc/kafka-ui 8182:8080

tmux-port-forward-ui: ## port forward kafka-ui in tmux
	@echo "Port forwarding kafka-ui in tmux"
	tmux new-session -d -s kafka-ui 'kubectl -n kafka port-forward svc/kafka-ui 8182:8080'
	@echo "Port forward completed. You can access the UI at http://localhost:8182"

####################################################################################
## Dev makefile commands
####################################################################################

dev: # manaul run as standalone app, testing purpose
	@if [ -z "${service}" ]; then \
		echo "ERROR: 'service' variable not set. Usage: make dev service=service-name"; \
		exit 1; \
	fi
	uv run services/${service}/src/${service}/main.py

push-dev:
	@if [ -z "${service}" ]; then \
		echo "ERROR: 'service' variable not set. Usage: make push-dev service=service-name"; \
		exit 1; \
	fi
	kind load docker-image ${service}:v1.0.0 --name rwml-34fa

build-dev: 
	@if [ -z "${service}" ]; then \
		echo "ERROR: 'service' variable not set. Usage: make build-dev service=service-name"; \
		exit 1; \
	fi
	@echo "Building ${service} image"
	docker build -t ${service}:v1.0.0 -f docker/service.Dockerfile --build-arg SERVICE_NAME=${service} .
	@echo "Build complete for ${service}"

deploy-dev: build push
	@if [ -z "${service}" ]; then \
		echo "ERROR: 'service' variable not set. Usage: make deploy-dev service=service-name"; \
		exit 1; \
	fi
	@echo "Deploying ${service} to dev"
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml 
	@echo "Deployment for ${service} to dev done"

####################################################################################
## Prod makefile commands
####################################################################################
# pre-requisite for build-push-prod : docker login ghcr.io -u <username> -p <token>
build-push-prod: ## we use buildx to avoid any cross platform issues, and push to github container registry
	@if [ -z "${service}" ]; then \
		echo "ERROR: 'service' variable not set. Usage: make build-push-prod service=service-name"; \
		exit 1; \
	fi
	@echo "Building ${service} image"
	@export ver_serial=$$(date +%s) && \
	docker buildx build --push \
			--platform linux/arm64 \
			-t ghcr.io/mingsheng92/${service}:0.1.0-beta.$${ver_serial} \
			-f docker/service.Dockerfile \
			--build-arg SERVICE_NAME=${service} \
			.
	@echo "Build complete for ${service}" 


deploy-prod:
	@if [ -z "${service}" ]; then \
		echo "ERROR: 'service' variable not set. Usage: make deploy-prod service=service-name"; \
		exit 1; \
	fi
	@echo "Deploying ${service} to prod"
	kubectl delete -f deployments/prod/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/prod/${service}/${service}.yaml 
	@echo "Deployment for ${service} to dev prod"


####################################################################################
## Linting and formatting with ruff
####################################################################################
lint: ## most likely wont use this because we are using pre-commit
	ruff check . --fix
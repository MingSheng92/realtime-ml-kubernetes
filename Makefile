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
## dev makefile commands
####################################################################################

dev: 
	uv run services/${service}/src/${service}/main.py

push:
	kind load docker-image ${service}:v1.0.0 --name rwml-34fa

build: 
	@echo "Building ${service} image"
	docker build -t ${service}:v1.0.0 -f docker/service.Dockerfile --build-arg SERVICE_NAME=${service} .
	@echo "Build complete for ${service}"

deploy: build push
	kubectl delete -f deployments/dev/${service}/${service}.yaml --ignore-not-found=true
	kubectl apply -f deployments/dev/${service}/${service}.yaml 

lint: 
	ruff check . --fix
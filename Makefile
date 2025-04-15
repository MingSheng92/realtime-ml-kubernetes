dev: 
	uv run services/${service}/src/${service}/main.py

push:
	kind load docker-image trades:v1.0.0 --name rwml-34fa

build: 
	docker build -t ${service}:v1.0.0 -f docker/${service}.Dockerfile .

buildop:
	docker build -t trades:v1.0.0 -f docker/trades_op.Dockerfile .

deploy: build push
	@kubectl delete -f deployments/dev/trades/trades.yaml || echo "No existing deployment to delete."
	kubectl apply -f deployments/dev/trades/trades.yaml

lint: 
	ruff check . --fix
dev: 
	uv run services/trades/src/trades/main.py

push:
	kind load docker-image trades:v1.0.0 --name rwml-34fa

build: 
	docker build -t trades:v1.0.0 -f docker/trades.Dockerfile .
	@echo "Build completed" 

deploy: build push
	kubectl delete -f deployments/dev/trades/trades.yaml
	kubectl apply -f deployments/dev/trades/trades.yaml
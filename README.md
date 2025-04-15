### Realtime Crypto Prediction ML System 

This repository contains my journey in learning/refresh memories on building an end to end machine learning system that predicts the cryto price in realtime. 

What I use for this project: 
- dev-container: to run this project in container environment
- package-management : uv, python package mangement and project manager, written in rust and blazing fast. 
- linting & formatting: ruff 
- ochestration: kubernetes, kind for cluster management, k9s as ui, dockers.
- data-streaming: kafka to load realtime crypto trade data, quixstream to load in dataframe for data transformation.
- pre-commits: to setup precommit hooks to perform ruff linting and formatting.

Note to self: Once pre-commit hook set up, docker desktop cannot commit for this repo anymore since it will not be able to trigger precommit hooks.

##### architecture diagram 

##### Initialize the project
Here we use kafka to load in "trades" topic in realtime and converts into features for training
Then we make use of news api and LLM to summarize news for market indicator, finetuning pipeline to ensure the summarization quality and vllm to serve it for inference
Kubernetes to ochestrate the microservices. 

with uv, creating packages as microservices is extremely straightforward. 
```
cd services
uv init --lib trades
```
With this, each service can be treated as a separate workspace. It utilize [tool.uv.workspace] section to define all work space members. In order to add a workspace as a dependency 
```
uv add trades
```
To add other dependencies, for example public libraries: quixstreams 
```
uv add quixstreams
```
##### Setting up Kafka


to be refined.
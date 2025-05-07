### Realtime Crypto Prediction ML System 

This repository contains my journey in learning/refresh memories on building an end to end machine learning system that predicts the cryto price in realtime. 

What I use for this project:
-  Dev container: To run the project in a containerized environment (Windows has issues with some libraries).
-  Package management: Using uv, a Python package manager and project manager written in Rust — it's blazing fast.
- Linting & formatting: ruff for linting and code formatting.
- Testing: Unit and integration tests using pytest (WIP).
- Orchestration: Kubernetes for orchestration, kind for local cluster management, k9s as the UI, and Docker for containerization.
- Data streaming: Kafka is used to stream real-time crypto trade data. quixstream loads the data into DataFrames for transformation.
- Pre-commits: Pre-commit hooks are configured to enforce ruff linting and formatting before commits.
- RisingWave: After ingesting and transforming data from the Kraken API (trades, candles, and technical indicators) via Kafka, we use RisingWave as a real-time feature store. It stores all historical data and supports both model training and model monitoring.
- Monitoring: Grafana is used to monitor the performance of the trained ML model against actual trade data.

<b>Note to self:</b>
- Once pre-commit hook set up, GitHub desktop cannot commit for this repo anymore since it will not be able to trigger precommit hooks.
- Use multistage docker build to ensure optimized docker image size.

##### Pre-requisites  
To make sure everything can run smoothly, make sure to set up github token 

Then you can create an .env.local file to setup the credentials locally for dev
```
export GITHUB_USER=YOUR_USERNAME
export GITHUB_PAT=TOKEN_CREDS
```
Next, run the command to login to github container registry
```
docker login ghcr.io -u <username> -p <token>
```

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


##### 
to be refined.
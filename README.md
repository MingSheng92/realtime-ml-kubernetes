### Realtime Crypto Prediction ML System 

This repository contains my journey in learning/refresh memories on building an end to end machine learning system that predicts the cryto price in realtime. 

##### architecture diagram 

##### 
Here we use kafka to load in "trades" topic in realtime and converts into features for training
Then we make use of news api and LLM to summarize news for market indicator, finetuning pipeline to ensure the summarization quality and vllm to serve it for inference
Kubernetes to ochestrate the microservices. 

to be refined.
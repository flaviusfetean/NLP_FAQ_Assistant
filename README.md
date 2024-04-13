# NLP_FAQ_Assistant
Objective: Develop a solution that can provide answers to users' questions by matching their queries with contextually similar questions in a predefined FAQ database. This system should further be enhanced to interact with the OpenAI API when it can't find a close enough match within the local FAQ database.

## How to use

### Using Docker

1. Make sure docker engine is running on the computer (You need to install docker if needed, a very easy variant is to install [Docker Desktop](https://www.docker.com/products/docker-desktop/))
2. Open a command prompt in the repository root
    - Run `docker compose up`. This might take some time until docker images are first pulled from the server (10 minutes on my machine).
    - There might be a problem if you have already set up another docker network on the same addresses (see picture):
      
    ![docker_network_error](https://github.com/flaviusfetean/NLP_FAQ_Assistant/assets/44545905/6dba8c21-9bc7-4b72-ad8a-bbf521bc78c3)
    - In this case you will need to delete the containers which use that network, and run `docker network prune`, so that networks are removed, and then rerun `docker compose up`
3. After the containers are up and running, open in the browser http://localhost:3000/
4. Chat with the assistant! 

   ![app screenshot](https://github.com/flaviusfetean/NLP_FAQ_Assistant/assets/44545905/2934af5e-0ba2-4d1a-9143-e563266eccdd)
5. **Other mentions**
    - For the first interaction, it will take some time for the backend to initialize, as the database needs to be populated (might take 1-2 minutes on the average PC).
    - In the beginning, you might be unauthenticated to Openai, in which case the interactions not resolved by the database will be carried by the local model.
    - To connect to Openai, you can enter a valid key in the corresponding field (top), and press enter, so the questions are forwarded to Openai if not found in the database. If the key is not valid, however, the interactions will still be managed by the local model.
    - The questions which are forwarded will also be saved locally.
    - The local model is currently [Llama2](https://www.llama2.ai/) by default. It might be more intensive and slow, but should work fine if you have more than 8GB of RAM.
    - There is the alternative to switch the model to [Orca-mini](https://ollama.com/library/orca-mini), which is less than half the size so if will be less intensive. However you will notice a decrease in the quality of the responses. To switch to Orca-mini, you will need to follow these steps:
        - Open the [Dockerfile](./Dockerfile) from the repository folder and modify the line 24 so it exports `orca-mini` instead of `llama2`:
        -     ENV OLLAMA_MODEL=orca-mini
        - Create in the repository folder a new file named `config.py`, and write an api key as shown below (Does not need to be valid. This step is necessary because that variable is used in the code, but not present in the repo for safety concerns of Github. It is, however, present in the subsequent Docker image):
        -     api_key='your_api_key_here'
        - Create in the [faq-front](./faq-front) folder, a file named `.env` and export the path to the backend as follows:
        -     REACT_APP_API=http://localhost:8000
        - Run `docker compose build`, and then `docker compose up`. The local model should now be `Orca-mini`. A nice addition to the application would be to make the model configurable from the frontend. 

### Locally 

#### Prerequisites 
1. Necessary python libraries installed, which are listed in [requirements.txt](./requirements.txt). Cd into the repo root and run `pip install -r requirements.txt`.
2. [PostgreSQL](https://www.postgresql.org/download/)
3. [pgvector](https://github.com/pgvector/pgvector) extension for Postgres. Follow the installation steps from their repository.
4. [Ollama](https://ollama.com/) for running LLM's locally and easily integrate them in the code.
   - After installing Ollama, cd into the folder where it is installed, open a Command Prompt there, and download the models that you want using `ollama pull` command, for example:
   -     ollama pull orca-mini
   - Find more details on what you can do with Ollama and what are the supported models on their [Github repo](https://github.com/ollama/ollama?tab=readme-ov-file).
5. [Node.js](https://nodejs.org/en) (the LTS version, as it contains npm which is necessary for running the frontend).

#### Usage
1. Create in the repository folder a new file named `config.py`, and write an api key as shown below (Does not need to be valid. This step is necessary because that variable is used in the code, but not present in the repo for safety concerns of Github. It is, however, present in the subsequent Docker image):
```
api_key='your_api_key_here'
```
2. Create in the [faq-front](./faq-front) folder, a file named `.env` and export the path to the backend as follows:
```
REACT_APP_API=http://localhost:8000
```
3. Open a terminal in the repository root and run:
```
uvicorn app.main:app --reload
```
4. Open a new terminal in the repository root and run:
```
cd ./faq-front/
npm install
npm start
```
5. These commands should automatically start the frontend. Otherwise, just open in the browser http://localhost:3000/

## Further Improvements
1. **Add the possibility to switch between local models**.
2. **Send server responses to the frontend in chunks** not a really useful thing but looks cool + the integrations with openai and ollama allow easily receiving of LLM output in chunks)
3. **Synchronize the databases of different models**.
    - As their embeddings are different, it makes sense that they are also kept and searched into different locations. Currently, different collections are held in the same database and used based on the model name.
    - However, if a model caches an embedding in its database, it will not be replicated in the databases of the others, even if it could be useful.
    - This may be done either by computing in-place the embedding of the other models and inserting them, or by pulling at initialization all of the other model's cache.
4. **Compute the similarities between questions in a smarter way**.
    - Currently the way this is implemented is by measuring cosine distance between the embeddings computed by the models. However, this may not be the optimal way as there are multiple occasions where the retrieved questions are wrong, or not matched even if they should.
    - For example, if you prompt `What are the steps to consider for a trip to Japan?` (obviously not present in the local database), it will be forwarded to Openai and the steps to take for a trip to Japan will be retrieved and cached (steps which include learning Japanese, getting a Japanese visa, etc). If you then prompt `What are the steps to consider for a trip to Germany?`, the same cached answer for Japan will be retrieved, even if it would be completely wrong.
    - Methods to consider are to also take into account what are the most important words in a question, compute ROUGE scores between questions, or also compare the embeddings of the questions with the answers, as often questions may be entirely contained in their respective answers.
5. **Enable GPU inference for the local Ollama models** (in Docker)
    - Instructions on how to do it are present on the [Docker Hub repo of Ollama](https://hub.docker.com/r/ollama/ollama) 

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

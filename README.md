# NLP_FAQ_Assistant
Objective: Develop a solution that can provide answers to users' questions by matching their queries with contextually similar questions in a predefined FAQ database. This system should further be enhanced to interact with the OpenAI API when it can't find a close enough match within the local FAQ database.

## How to use

### Using Docker

1. Make sure docker engine is running on the computer (You need to install docker if needed, a very easy variant is to install [Docker Desktop](https://www.docker.com/products/docker-desktop/))
2. Open a command prompt in the repository root
    - run 'docker compose up'
    - There might be a problem if you have already set up another docker network on the same addresses (see picture): 
    ![docker_network_error](https://github.com/flaviusfetean/NLP_FAQ_Assistant/assets/44545905/6dba8c21-9bc7-4b72-ad8a-bbf521bc78c3)
    - In this case you will need to delete the containers which use that network, and run 'docker network prune', so that networks are removed, and then rerun 'docker compose up'
3. After the containers are up and running, open in the browser http://localhost:3000/
4. Chat with the assistant! (You don't have to insert the key for now, it will work either way)
   ![app screenshot](https://github.com/flaviusfetean/NLP_FAQ_Assistant/assets/44545905/2934af5e-0ba2-4d1a-9143-e563266eccdd)

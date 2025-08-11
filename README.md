# open-cec-api
Refactor of the CEC API using FastAPI and a refined data model



### Setup
Clone this repo and `cd` into it. Then, run the following:
```bash
python3 -m venv cec_env
source cec_env/bin/activate
python3 -m pip install poetry
poetry install
```

### Running
```bash
docker compose -f deploy/docker-compose.yml up --build
```

### Database

```bash
docker exec -it open-cec-api-postgres-1 psql -d open_cec_db -U open_cec_user
```


### ENV

You will need a .env file which contains entries for the following:
```
OPEN_CEC_API_API_KEY_HASH
```
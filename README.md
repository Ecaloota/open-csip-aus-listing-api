# open-cec-api
Refactor of the CEC API using FastAPI and a refined data model



### Setup
Clone this repo and `cd` into it. Then, run the following:
```bash
conda create -n open_cec_api python=3.12
conda activate open_cec_api
pip install poetry
poetry install
```

### Database
```bash
docker exec -it open-cec-api-postgres-1 psql -d open_cec_db -U open_cec_user
```
# ACCT5123.Q21.CTTT_Group5

## backend setup
```
cd backend
docker compose up -d
python -m backend.scripts.import_csv 
python -m backend.app 
```
stop docker container
```aiignore
docker compoes down
```
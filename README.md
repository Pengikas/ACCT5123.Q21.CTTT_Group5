# ACCT5123.Q21.CTTT_Group5

## setup
### docker 
```
docker compose -f backend/docker-compose.yml up -d
```
### backend 
```
python -m pip install -r requirements.txt
python -m backend.scripts.import_csv 
python -m backend.app 
```

### frontend 
```aiignore
python -m streamlit run frontend/app.py
```
### stop docker container
```
docker compose -f backend/docker-compose.yml down
```
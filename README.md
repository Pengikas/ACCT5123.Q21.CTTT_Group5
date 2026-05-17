# ACCT5123.Q21.CTTT_Group5

## setup
### docker 
```
cd backend
docker compose up -d
cd ..
```
### backend 
```
python -m backend.scripts.import_csv 
python -m backend.app 
```

### frontend 
```aiignore
python -m streamlit run frontend/app.py
```
### stop docker container
```
docker compose down
```
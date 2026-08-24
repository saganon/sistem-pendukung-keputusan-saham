# Sistem Pendukung Keputusan Saham

## Getting Started
Install all dependencies. Go to `backend` directory and run below command:

```
pip3 install .
```

Go to backend. Run the server
```
PYTHONPATH=src uvicorn dss_stock.api.app:app --reload --port 8000
```

Fix lint
```
ruff check --fix
```

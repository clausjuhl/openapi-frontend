# openapi-frontend
Simple frontend for an openapi-backend.

Loosely modelled on encode/hostedapi

# Run
uvicorn source.app:app --port 5000 --host 0.0.0.0 --env-file .env 

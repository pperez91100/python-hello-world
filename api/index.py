from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import requests

app = FastAPI()

# Configuration pour autoriser tous les domaines en CORS (à ajuster en fonction de vos besoins en sécurité)
origins = ["https://python-hello-world-roan-nine.vercel.app/", "http://localhost:3000"]

# Ajouter le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration du logging
logging.basicConfig(filename="requests.log", level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_host = request.client.host
    public_ip = get_public_ip()
    request_method = request.method
    request_url = request.url.path
    logging.info(f"IP: {client_host} | Public IP: {public_ip} | Method: {request_method} | URL: {request_url}")
    response = await call_next(request)
    return response

def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        return "N/A"

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

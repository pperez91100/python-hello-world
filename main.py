from fastapi import FastAPI, Request
import logging
import requests
import uvicorn

app = FastAPI()

# Configuration du logging pour afficher les informations dans la console
logging.basicConfig(level=logging.INFO)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

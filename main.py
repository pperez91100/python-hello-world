from fastapi import FastAPI, Request, HTMLResponse
import requests
import uvicorn
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_host = request.client.host
    public_ip = get_public_ip()
    request_method = request.method
    request_url = request.url.path
    log_message = f"IP: {client_host} | Public IP: {public_ip} | Method: {request_method} | URL: {request_url}"
    app.state.logs.append(log_message)  # Ajoutez le message au registre des logs
    response = await call_next(request)
    return response

def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        data = response.json()
        return data["ip"]
    except Exception as e:
        return "N/A"

@app.get("/", response_class=HTMLResponse)
def read_root():
    logs = "<br>".join(app.state.logs)  # Obtenez les logs sous forme de chaîne HTML
    return f"<html><body><h1>Logs:</h1><p>{logs}</p></body></html>"

if __name__ == "__main__":
    app.state.logs = []  # Initialisez la liste des logs dans l'état de l'application
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

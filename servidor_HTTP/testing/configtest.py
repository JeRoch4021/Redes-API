import subprocess
import time
import pytest
import requests

@pytest.fixture(scope="session", autouse=True)
def iniciar_servidor():
    # Ejecutar el servidor en segundo plano
    server = subprocess.Popen(["uvicorn", "servidor_HTTP.main:app", "--port", "8000" ])
    # Esperar a que el servidor arranque
    time.sleep(3)

    # Verificar si el servidor esta respondiendo
    try:
        response = requests.get("http://127.0.0.1:8000/posts")
        assert response.status_code == 200
    except Exception as ex:
        server.kill()
        raise RuntimeError("El servidor no se pudo iniciar correctamente", ex)
    
    yield # Aquí se ejecutan los tests

    server.kill()

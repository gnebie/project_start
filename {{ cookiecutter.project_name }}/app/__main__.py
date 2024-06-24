from app.config.settings import settings
from app.create_app import create_app

app = create_app()

def main():
    # Démarrez l'application ASGI avec uvicorn si ce fichier est exécuté directement
    # import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    pass


if __name__ == "__main__":
    main()
from dotenv import load_dotenv

load_dotenv() # load des variables d'environnement 

from src.server import app


app.run(host='0.0.0.0', port=3000) # Permet de lancer le serveur web avec l'app dans le fichier ./src/server.py

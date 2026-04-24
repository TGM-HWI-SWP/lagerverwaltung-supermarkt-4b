from pymongo import MongoClient  # MongoDB Client für Verbindung zur Datenbank
from pymongo.server_api import ServerApi  # ermöglicht Nutzung einer festen Server-API-Version (stabil/kompatibel)

uri = "mongodb+srv://rajkovicgabriel_db_user:GR12345GR@cluster0.jge9ku6.mongodb.net/?appName=Cluster0"  # Verbindungsstring inkl. Authentifizierung

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))  # erstellt Client mit API-Version 1 → verhindert Breaking Changes

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')  # sendet Ping-Befehl an MongoDB → prüft ob Verbindung funktioniert
    print("Pinged your deployment. You successfully connected to MongoDB!")  # Erfolgsmeldung
except Exception as e:
    print(e)  # gibt Fehler aus falls Verbindung fehlschlägt
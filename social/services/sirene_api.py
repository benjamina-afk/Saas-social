import requests

API_KEY = "683c16b7-7e0a-4713-bc16-b77e0ac71357"  # celle que tu vois dans 'Clés d’API'
BASE_URL = "https://api.insee.fr/api-sirene/3.11/siret"

def get_siret_info(siret: str):
    """
    Appelle l'API Sirene avec la clé API du portail.
    Retourne le JSON si le SIRET existe, sinon None.
    """
    url = f"{BASE_URL}/{siret}"

    headers = {
        "X-INSEE-Api-Key-Integration": API_KEY,  # <- NOM TRÈS IMPORTANT
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=10)

    print("INSEE status:", response.status_code)
    print("INSEE body:", response.text)

    if response.status_code == 200:
        return response.json()

    return None

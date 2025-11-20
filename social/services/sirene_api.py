import requests

# 🔑 Mets ici ta vraie clé d'API du nouveau portail Insee
API_KEY = "683c16b7-7e0a-4713-bc16-b77e0ac71357"

# ✅ Nouvelles URLs officielles (version 3.11)
BASE_SIREN_URL = "https://api.insee.fr/api-sirene/3.11/siren"
BASE_SIRET_URL = "https://api.insee.fr/api-sirene/3.11/siret"


def _headers():
    """
    Headers conformes à la doc Insee :
    la clé d'API se met dans X-INSEE-Api-Key-Integration
    """
    return {
        "X-INSEE-Api-Key-Integration": API_KEY,
        "Accept": "application/json",
    }


def get_siren_info(siren: str):
    """
    Appel direct au service /siren/{siren}
    """
    url = f"{BASE_SIREN_URL}/{siren}"

    print("INSEE URL:", url)

    response = requests.get(url, headers=_headers(), timeout=10)

    print("INSEE status:", response.status_code)
    print("INSEE body:", response.text)

    if response.status_code != 200:
        return None

    return response.json()


def get_siret_info(siret: str):
    """
    Appel direct au service /siret/{siret}
    (on s’en servira éventuellement plus tard)
    """
    url = f"{BASE_SIRET_URL}/{siret}"

    print("INSEE URL:", url)

    response = requests.get(url, headers=_headers(), timeout=10)

    print("INSEE status:", response.status_code)
    print("INSEE body:", response.text)

    if response.status_code != 200:
        return None

    return response.json()
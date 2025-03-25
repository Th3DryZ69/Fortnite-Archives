# import requests
# from base64 import b64encode

# def get_access_token():
#     try:
#         client_id = '34a02cf8f4414e29b15921876da36f9a'
#         client_secret = 'daafbccc737745039dffe53d94fc76cf'
#         authorization = b64encode(f"{client_id}:{client_secret}".encode()).decode()

#         response = requests.post(
#             "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
#             data={
#                 "grant_type": "client_credentials",
#                 "token_token": "eg1",
#                 "scope": "launcher:download:Live:* READ"
#             },
#             headers={
#                 "Authorization": f"Basic {authorization}",
#                 "Content-Type": "application/x-www-form-urlencoded"
#             }
#         )

#         response.raise_for_status()
#         return response.json()['access_token']
#     except requests.RequestException as e:
#         print(f"Erreur lors de l'obtention du token: {e}")
#         return None

# def get_manifest(platform, token):
#     urls = {
#         'Android': '5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds',
#         'IOS': '5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds',
#         'Windows': '4fe75bbc5a674f4f9b356b5c90567da5/Fortnite'
#     }

#     if platform not in urls:
#         raise ValueError('Platform not supported')

#     try:
#         url = f"https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/{platform}/{urls[platform]}?label=Live"
#         response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Erreur lors de la récupération du manifest: {e}")
#         return None

# def main():
#     platform = input("Choisissez la plateforme (Android, IOS, Windows): ")

#     # Transformer uniquement "IOS" en majuscule
#     if platform.lower() == "ios":
#         platform = "IOS"

#     token = get_access_token()
#     if not token:
#         print("Impossible d'obtenir le token d'accès.")
#         return

#     asset_response = get_manifest(platform, token)
#     if not asset_response:
#         print("Erreur lors de la récupération des informations du manifest.")
#         return

#     manifest_version = asset_response.get('buildVersion')
#     manifest_url, signature = None, None

#     while True:
#         asset_response = get_manifest(platform, token)
#         if not asset_response:
#             print("Erreur lors de la récupération des informations du manifest.")
#             return
        
#         signature = asset_response['items']['MANIFEST']['signature']
#         distribution = asset_response['items']['MANIFEST']['distribution']
#         path = asset_response['items']['MANIFEST']['path']
#         manifest_url = f"{distribution}{path}?{signature}"

#         if not signature.startswith('Policy='):
#             break

#     print(f"Voici le lien du dernier manifest pour {platform}:")
#     print(f"Version: {manifest_version}")
#     print(f"Lien de téléchargement: {manifest_url}")

# if __name__ == "__main__":
#     main()





import requests
from base64 import b64encode

def get_access_token():
    try:
        client_id = '34a02cf8f4414e29b15921876da36f9a'
        client_secret = 'daafbccc737745039dffe53d94fc76cf'
        authorization = b64encode(f"{client_id}:{client_secret}".encode()).decode()

        response = requests.post(
            "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
            data={
                "grant_type": "client_credentials",
                "token_token": "eg1",
                "scope": "launcher:download:Production:* READ"
            },
            headers={
                "Authorization": f"Basic {authorization}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        response.raise_for_status()
        print(response.json()['access_token'])
        return response.json()['access_token']
        
    except requests.RequestException as e:
        print(f"Erreur lors de l'obtention du token: {e}")
        return None

def get_manifest(platform, token):
    urls = {
        'Android': '5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds',
        'IOS': '5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds',
        'Windows': '4fe75bbc5a674f4f9b356b5c90567da5/Fortnite',
        # 'Windows': '1e8bda5cfbb641b9a9aea8bd62285f73/Fortnite_Studio'
    }
    
    try:
        url = f"https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/{platform}/{urls[platform]}?label=Live"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération du manifest pour {platform}: {e}")
        return None

def main():
    token = get_access_token()
    if not token:
        print("Impossible d'obtenir le token d'accès.")
        return

    platforms = ['Android', 'IOS', 'Windows']
    
    for platform in platforms:
        asset_response = get_manifest(platform, token)
        if not asset_response:
            continue

        manifest_version = asset_response.get('buildVersion')
        manifest_url, signature = None, None

        while True:
            asset_response = get_manifest(platform, token)
            if not asset_response:
                break
            
            signature = asset_response['items']['MANIFEST']['signature']
            distribution = asset_response['items']['MANIFEST']['distribution']
            path = asset_response['items']['MANIFEST']['path']
            manifest_url = f"{distribution}{path}?{signature}"

            if not signature.startswith('Policy='):
                break

        print(f"\n✅ Dernier manifest pour {platform}:")
        print(f"📌 Version: {manifest_version}")
        print(f"📥 Lien de téléchargement: {manifest_url}")

if __name__ == "__main__":
    main()
import requests
import json
from datetime import datetime
from datetime import timedelta

# Fonction pour déterminer si c'est actuellement les vacances scolaires
def is_vacances_scolaires_now(start_date, end_date):
    # Obtenez la date du jour au format YYYY-MM-DD
    aujourdhui = datetime.now().strftime('%Y-%m-%d')
    if aujourdhui < start_date or aujourdhui > end_date:
        return False
    else:
        return True

def is_vacances_scolaires_tomorrow(start_date, end_date):
    # Obtenez la date du lendemain au format YYYY-MM-DD
    demain = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    if demain < start_date or demain > end_date:
        return False
    else:
        return True
    
def is_vacances_scolaires_next_week(start_date, end_date):
    # Obtenez la date d'aujourd'hui
    aujourdhui = datetime.now()
    
    # Obtenez la date de la semaine prochaine
    semaine_prochaine = aujourdhui + timedelta(days=7)
    
    # Formatez les dates au format YYYY-MM-DD
    aujourdhui_str = aujourdhui.strftime('%Y-%m-%d')
    semaine_prochaine_str = semaine_prochaine.strftime('%Y-%m-%d')
    
    if semaine_prochaine_str < start_date or semaine_prochaine_str > end_date:
        return False
    else:
        return True

###########################
###########################
###########################
###########################
# Paramètres de la requête
location = 'Orléans-Tours' # choisir par la liste des acamdémies 
# liste des académies : 'Corse', 'Polynésie', 'Nouvelle Calédonie', 'Guyane', 'Aix-Marseille',
# 'Amiens', 'Besançon', 'Bordeaux', 'Clermont-Ferrand', 'Créteil', 'Dijon', 'Grenoble', 'Lille',
# 'Limoges', 'Lyon', 'Montpellier', 'Nancy-Metz', 'Nantes', 'Nice', 'Orléans-Tours', 'Paris',
# 'Poitiers', 'Reims', 'Rennes', 'Strasbourg', 'Toulouse', 'Versailles', 'Mayotte', 'Réunion',
# 'Martinique', 'Saint Pierre et Miquelon', 'Wallis et Futuna', 'Caen', 'Rouen', 'Guadeloupe', 'Normandie'

rows = 1
aujourdhui = datetime.now().strftime('%Y-%m-%d')

# URL de l'API
url = f"https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-calendrier-scolaire/records?where=end_date%3E%22{aujourdhui}%22&order_by=end_date%20ASC&limit={rows}&refine=location%3A{location}"

# Effectuer la requête GET
response = requests.get(url)

# Vérifier si la requête a réussi (code de statut HTTP 200)
if response.status_code == 200:
    # Convertir la réponse JSON en un dictionnaire Python
    data = json.loads(response.text)
    
    vacances = data["results"][0]
    vacances['aujourdhui'] = is_vacances_scolaires_now(vacances['start_date'], vacances['end_date'])
    vacances['demain'] = is_vacances_scolaires_tomorrow(vacances['start_date'], vacances['end_date'])
    vacances['semaine prochaine'] = is_vacances_scolaires_next_week(vacances['start_date'], vacances['end_date'])
    
    # Afficher les données (vous pouvez les traiter selon vos besoins)
    print(json.dumps(vacances, indent=2))
else:
    print(f"La requête a échoué avec le code de statut {response.status_code}")


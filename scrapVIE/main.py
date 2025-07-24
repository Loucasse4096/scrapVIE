import requests
import json
import os
import sys
from argparse import ArgumentParser
from email_utils import send_email

def scrap_airbus(debug=False):
    url = "https://ag.wd3.myworkdayjobs.com/wday/cxs/ag/Airbus/jobs"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "x-calypso-csrf-token": "15716289-4ac0-4e01-a44a-5a2009d94fca",
        "origin": "https://ag.wd3.myworkdayjobs.com",
        "referer": "https://ag.wd3.myworkdayjobs.com/Airbus?workerSubType=f5811cef9cb5016cb7041bb2470a8418",
    }
    data = {
        "appliedFacets": {"workerSubType": ["f5811cef9cb5016cb7041bb2470a8418"]},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }
    if debug:
        print(f"[DEBUG] POST {url}")
        print(f"[DEBUG] Headers: {headers}")
        print(f"[DEBUG] Data: {data}")
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    if debug:
        print("[DEBUG] Réponse JSON brute :\n")
        print(json.dumps(response.json(), indent=2)[:2000])
        print("\n[DEBUG] --- Fin de l'aperçu de la réponse JSON ---\n")
    jobs = []
    for job in response.json().get('jobPostings', []):
        job_obj = {
            'title': job.get('title'),
            'location': job.get('locationsText'),
            'url': f"https://ag.wd3.myworkdayjobs.com{job.get('externalPath')}",
            'postedOn': job.get('postedOn'),
            'ref': job.get('bulletFields', [None])[0]
        }
        if debug:
            print(f"[DEBUG] Job extrait : {job_obj}")
        jobs.append(job_obj)
    if debug:
        print(f"[DEBUG] Total jobs extraits : {len(jobs)}")
    return jobs

def scrap_thales(debug=False):
    url = "https://careers.thalesgroup.com/widgets"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "origin": "https://careers.thalesgroup.com",
        "referer": "https://careers.thalesgroup.com/fr/fr/search-results",
        "x-csrf-token": "efeef485f4424c249ba4a34808c54488",
    }
    data = {
        "lang": "fr_fr",
        "deviceType": "desktop",
        "country": "fr",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": 0,
        "jobs": True,
        "counts": True,
        "all_fields": ["category", "country", "state", "city", "type", "workerSubType", "workLocation"],
        "size": 10,
        "clearAll": False,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page18",
        "siteType": "external",
        "keywords": "",
        "global": True,
        "selected_fields": {"workerSubType": ["VIE - French International Internship Programme (Fixed Term)"]},
        "locationData": {}
    }
    if debug:
        print(f"[DEBUG] POST {url}")
        print(f"[DEBUG] Headers: {headers}")
        print(f"[DEBUG] Data: {data}")
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    if debug:
        print("[DEBUG] Réponse JSON brute :\n")
        print(json.dumps(response.json(), indent=2)[:2000])
        print("\n[DEBUG] --- Fin de l'aperçu de la réponse JSON ---\n")
    jobs = []
    for job in response.json().get('refineSearch', {}).get('data', {}).get('jobs', []):
        job_obj = {
            'title': job.get('title'),
            'location': job.get('location'),
            'url': job.get('applyUrl'),
            'postedOn': job.get('postedDate'),
            'ref': job.get('jobId')
        }
        if debug:
            print(f"[DEBUG] Job extrait : {job_obj}")
        jobs.append(job_obj)
    if debug:
        print(f"[DEBUG] Total jobs extraits : {len(jobs)}")
    return jobs

def scrap_vie_business(debug=False):
    url = "https://civiweb-api-prd.azurewebsites.net/api/Offers/search"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Origin": "https://mon-vie-via.businessfrance.fr",
        "Referer": "https://mon-vie-via.businessfrance.fr/",
    }
    data = {
        "limit": 50,
        "skip": 0,
        "query": "",
        "specializationsIds": ["212"],
        "activitySectorId": [],
        "missionsTypesIds": [],
        "missionsDurations": [],
        "gerographicZones": [],
        "countriesIds": [],
        "studiesLevelId": [],
        "companiesSizes": [],
        "entreprisesIds": [0],
        "missionStartDate": None
    }
    if debug:
        print(f"[DEBUG] POST {url}")
        print(f"[DEBUG] Headers: {headers}")
        print(f"[DEBUG] Data: {data}")
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    if debug:
        print("[DEBUG] Réponse JSON brute :\n")
        print(json.dumps(response.json(), indent=2)[:2000])
        print("\n[DEBUG] --- Fin de l'aperçu de la réponse JSON ---\n")
    jobs = []
    for job in response.json().get('result', []):
        job_obj = {
            'title': job.get('missionTitle'),
            'location': job.get('cityNameEn') or job.get('cityName'),
            'url': None,  # Pas d'URL directe fournie
            'postedOn': job.get('creationDate'),
            'ref': job.get('id')
        }
        if debug:
            print(f"[DEBUG] Job extrait : {job_obj}")
        jobs.append(job_obj)
    if debug:
        print(f"[DEBUG] Total jobs extraits : {len(jobs)}")
    return jobs

def scrap_societe_generale(debug=False):
    url = "https://careers.societegenerale.com/search-proxy.php"
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization-api": "Bearer eyJ0eXAiOiJKV1QiLCJraWQiOiJpcHhUM1gvWUdxZmFmbmRFM3o5clRTM2xqQ2c9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJkMDZkYzFhNi0xODczLTQ5YWItYTk2OS05ZGJiY2ZhYThmYTkiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXVkaXRUcmFja2luZ0lkIjoiOGM5NjQxZTMtYzM4ZC00ZjZkLWJkZjQtNDZjODdjY2Q2Zjg5LTIwMzY0NzA0NSIsInN1Ym5hbWUiOiJkMDZkYzFhNi0xODczLTQ5YWItYTk2OS05ZGJiY2ZhYThmYTkiLCJpc3MiOiJodHRwczovL3Nzby5zZ21hcmtldHMuY29tOjQ0My9zZ2Nvbm5lY3Qvb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoiVFhZdlpVRE42YnF4MGZ1bUk5OUc5dkwtVmQwIiwiY2xpZW50X2lkIjoiZDA2ZGMxYTYtMTg3My00OWFiLWE5NjktOWRiYmNmYWE4ZmE5IiwiYXVkIjoiZDA2ZGMxYTYtMTg3My00OWFiLWE5NjktOWRiYmNmYWE4ZmE5IiwibmJmIjoxNzUzMzU3NTI1LCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwic2NvcGUiOlsic2d4QEBvcmlnaW5fbmV0d29ya0BASW50ZXJuZXQiLCJhcGkuY29ycHNyYy0wMDI1Ny52MSJdLCJhdXRoX3RpbWUiOjE3NTMzNTc1MjUsInJlYWxtIjoiLyIsImV4cCI6MTc1MzM1ODEyNSwiaWF0IjoxNzUzMzU3NTI1LCJleHBpcmVzX2luIjo2MDAsImp0aSI6Im9paE1uR1U2SzdhRVpBUHJKMTdxMFNHbHFJWSJ9.fFGB93tGhnSzvdLbfdigNL9tYKd_6yvKTc9l4BjVBhUT-e900Bp_p3DdKs0Ljo0aKG9BNMIoZynONvcVnJLbV2FkjGTryZhFRbTuqoVeYp-44hcWC2VCgp09v76R4BnD9p0Sms1HdJLPHnTTj-U01Lp3p_-husJ-59TEn3iI7lGRDz7IA0S4q4Vc_hAB5a1PBRqhMAcFOwP8BckLya_46NFxaiGXD9yoPQn7Osu21fo3xRQR9PumHccxaSwvNio3n5vHUbu_OBhK6gOKw8sBJjpsu0nFITHa2KIqz4aQXi7AgSSBlar2J1WEMVUG1y8hqW_zo05KXHTRiIsbYoS73A",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://careers.societegenerale.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://careers.societegenerale.com/rechercher?refinementList[jobType][0]=COOPERATIVE&refinementList[jobFunction][0]=BJ725",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "x-proxy-url": "https://api.socgen.com/business-support/it-for-it-support/cognitive-service-knowledge/api/v1/search-profile"
    }
    data = {
        "profile": "ces_profile_sgcareers",
        "query": {
            "advanced": [
                {
                    "type": "simple",
                    "name": "sourcestr6",
                    "op": "eq",
                    "value": "job"
                },
                {
                    "type": "multi",
                    "name": "sourcestr8",
                    "op": "eq",
                    "values": ["COOPERATIVE"]
                }
            ],
            "skipCount": 10,
            "skipFrom": 0
        },
        "lang": "fr",
        "responseType": "SearchResult"
    }
    if debug:
        print(f"[DEBUG] POST {url}")
        print(f"[DEBUG] Headers: {headers}")
        print(f"[DEBUG] Data: {data}")
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    if debug:
        print("[DEBUG] Réponse JSON brute :\n")
        print(json.dumps(response.json(), indent=2)[:2000])
        print("\n[DEBUG] --- Fin de l'aperçu de la réponse JSON ---\n")
    jobs = []
    for job in response.json().get('Result', {}).get('Docs', []):
        job_obj = {
            'title': job.get('title'),
            'location': job.get('sourcestr7'),
            'url': job.get('url1'),
            'postedOn': job.get('sourcedatetime1'),
            'ref': job.get('sourcestr4')
        }
        if debug:
            print(f"[DEBUG] Job extrait : {job_obj}")
        jobs.append(job_obj)
    if debug:
        print(f"[DEBUG] Total jobs extraits : {len(jobs)}")
    return jobs

def load_existing_jobs(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_jobs(site, jobs, debug=False):
    output_file = f"{site}_jobs.json"
    existing_jobs = load_existing_jobs(output_file)
    existing_refs = {job.get('ref') for job in existing_jobs}
    new_jobs = []
    for job in jobs:
        if job['ref'] in existing_refs:
            print(f"Job déjà présent (ref={job['ref']}) : {job['title']}")
        else:
            new_jobs.append(job)
            existing_refs.add(job['ref'])
    if new_jobs:
        all_jobs = existing_jobs + new_jobs
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)
        print(f"{len(new_jobs)} nouveaux jobs ajoutés dans {output_file}")
    else:
        print(f"Aucun nouveau job à ajouter pour {site}.")
    return new_jobs


def main():
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Activer le mode debug')
    parser.add_argument('--site', type=str, default=None, choices=['airbus', 'thales', 'vie_business', 'societe_generale'], help='Site à scraper (airbus, thales, vie_business ou societe_generale)')
    parser.add_argument('--all', action='store_true', help='Scraper tous les sites à la fois')
    args = parser.parse_args()
    debug = args.debug or os.environ.get('DEBUG', '0') == '1'

    sites = ['airbus', 'thales', 'vie_business', 'societe_generale'] if args.all else ([args.site] if args.site else ['airbus'])

    all_new_jobs = []
    for site in sites:
        print(f"\n--- Scraping {site} ---")
        if site == 'airbus':
            jobs = scrap_airbus(debug=debug)
        elif site == 'thales':
            jobs = scrap_thales(debug=debug)
        elif site == 'vie_business':
            jobs = scrap_vie_business(debug=debug)
        elif site == 'societe_generale':
            jobs = scrap_societe_generale(debug=debug)
        else:
            print(f"Site non supporté : {site}")
            continue
        new_jobs = save_jobs(site, jobs, debug=debug)
        for job in new_jobs:
            job['origin'] = site
        all_new_jobs.extend(new_jobs)

    # Affichage du résumé final
    if all_new_jobs:
        print("\nRésumé des nouveaux jobs ajoutés :")
        lines = []
        for job in all_new_jobs:
            line = f"- [{job['origin']}] {job['title']} | {job['location']} | {job['url'] if job['url'] else ''}"
            print(line)
            lines.append(line)
        # Envoi du mail
        body = "Résumé des nouveaux jobs ajoutés :\n\n" + "\n".join(lines)
        print("\nEnvoi du mail...")
        send_email(body)
    else:
        print("\nAucun nouveau job ajouté sur l'ensemble des sites.")

if __name__ == "__main__":
    main() 
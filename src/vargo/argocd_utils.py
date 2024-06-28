import json
import requests
import urllib3

from .statics import ApplicationReport

def argocd_generate_token(argocd_ip, argocd_port, username, password):
    urllib3.disable_warnings()
    session = requests.Session()
    full_url = f"https://{argocd_ip}:{argocd_port}/api/v1/session"
    
    headers = {
        "Content-Type": 'application/json',
    }
    
    payload = {
        "username": username,
        "password": password
    }
    
    auth = None
    
    try:
        auth = session.post(full_url, headers=headers, json=payload, verify=False)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    
    if auth is None:
        print("No response when generating argocd token.")
        return None
    elif auth.status_code != 200:
        print(auth.status_code)
        print(auth.content)
        return None
    
    if 'token' in json.loads(auth.content):
        return json.loads(auth.content)['token']
    
    return None

def argocd_get_applications(argocd_ip, argocd_port, token):
    session = requests.Session()
    full_url = f"https://{argocd_ip}:{argocd_port}/api/v1/applications"
    
    headers = {
        "Authorization": f'Bearer {token}'
    }
    
    resp = None
    
    try:
        resp = session.get(full_url, headers=headers, verify=False)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    
    if resp is not None and resp.status_code != 200:
        print(resp.status_code)
        print(resp.content)
        return None
    
    return json.loads(resp.content)['items']

def argocd_refresh_application(argocd_ip, argocd_port, token, application_name):
    session = requests.Session()
    full_url = f"https://{argocd_ip}:{argocd_port}/api/v1/applications/{application_name}"
    
    headers = {
        "Authorization": f'Bearer {token}'
    }
    
    params = {
        "refresh": "true"
    }
    
    resp = None
    
    try:
        resp = session.get(full_url, headers=headers, params=params, verify=False)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    
    if resp is not None and resp.status_code != 200:
        print(resp.status_code)
        print(resp.content)
        return None
    
    return json.loads(resp.content)
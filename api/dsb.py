import requests

API_URL = 'https://mobileapi.dsbcontrol.de/'

def auth(user: int, password: str) -> dict:
  result = requests.get(API_URL + f"authid?bundleid=de.heinekingmedia.dsbmobile&appversion=35&osversion=22&pushid&user={user}&password={password}")
  
  if not result.json(): return { 'error': 'invalid login credentials' }
  elif not result.ok: return { 'error': 'request to the dsb servers did not succeed' }
  else: return { 'authid': result.json() }
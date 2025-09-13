import requests
import json
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException

roblox_cookie = {".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_D68C5189906EBC81E1725D1EDCD281521104845B280B979C31C4CE344904403CE11935550E69B60175642331DC03160CC80B7AA5377182AFFF096E91AA1B994C9BCBA0FED3A430646807D2782DD0B42AD8D9FF14F7D2749732884FC30F51D98EDD838FF56DAE250E349B387CBCAFC18046A83A6C60ADE1C92A17432E0D255FE6F9B1554878FF40BC050BF79EA24E84AD009FEA63CF4B88BBEFBDADB22A0357930AB4779235E6A2FD85F0424C94E2A35638659F794478CD69F831E0C4E6C3C4EE0F1976C16F6EBE25BACC1E81CE03E1DB71FA678E7AA9CC2DD468C3A287B656662DF257003E6DB6D2DAE7057361DA40002903219CAE083C419A00CEA8DF2F161DC1BCA3B826D46FA20FA71C13152F36044B4F819AE765ECDA99AF5FB3F6D97E93F35AEDA0A2EB138AEE3EEAC70D97A7210B28EBEC7A0FDE670C07B24C3285F2A620FE57B80CF46809FAC8BF5D7B9640E22830DD5E55B0FD18920DBF5E5B8E7D72C507F7AEF6971712CCB97909BDB08B7811BC4208E415300F91BCAC004E3386EED3AD7A41E0FC4196C9928FB0C59C7E13794FEA2DCCA6687731894AF1A101BE0CA5FA55503F266829EBE8780206BEDFC6849D320C7E077F463F4EFC4A2A0D74234F0DAB8E7F772503BBCDA5EAC0D6DBB2ED23173B25B14FF64AE48D3E4195ED5AE90195EBBCD274EB139C4CC3E4E01793C58091C898FF464FE8FB015D3D565069BC13843C0D9A7C503B572F027712B908A3AB8158A518846DC07894983E6542182E50E1A105797A56D9E85497143F8016C9B33F146D8E798DA2438513DECF35433A09161D510E8D8422CD93AB794B163FC39A35CB686C5B7FABA5509D1152CF620B20A4E40D99714F86AC01C0936C7DBDFEC7A993ED4468916F249291B3BF267635CDE842ED946A61192B5193D7AD735AE3AFDA9D2ECAF5323BAFE4A2EF497A7AA504FCBE7E1B10B33A0F12CEEEB55D6AB956CEEFCD5AFFE66977874A4427DD03154490A5D0EBBA26F341C3C3614162950957F199E254AA7401A9E23D401341863D46D4EA"}
def clothings(id):
  clothings = 0
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
    check = session.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30").result()
    check = check.json()
  except RequestException as e:
    print(e)
    return 0

  def get_page(cursor=None):
      nonlocal check
      try:
        if cursor:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30&cursor={cursor}"
        else:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30"
        check = session.get(url).result().json()
      except RequestException as e:
        print(e)  
        return 0
      return check

  while True:
      if "data" in check:
          clothings += len(check['data'])
      if "nextPageCursor" not in check or not check['nextPageCursor']:
          break
      else:
          check = get_page(check['nextPageCursor'])
  return clothings

def robux(id):
  # Import Local Cookie Variable
  global roblox_cookie
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://economy.roblox.com/v1/groups/{id}/currency', cookies=roblox_cookie, timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    data = json.loads(response.text)
    if "robux" in data:
      robux = data.get("robux", 0)
    else:
      robux = 0
  except RequestException as e:
    print(e)
    return 0
  return robux


def gamevisits(id):
  # Create a FuturesSession object
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))

  # Make the API request asynchronously
  try:
    future = session.get(f'https://games.roblox.com/v2/groups/{id}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc', timeout=5)
  except RequestException as e:
    print(e)
    return 0

  # Wait for the request to complete and load the response into a dictionary
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
      
  except RequestException as e:
    print(e)
    return 0

  # If there are no games, return "None"
  if not data:
    return 0
  
  # Find the total number of visits for all games
  total_visits = 0
  for game in data:
    visits = game["placeVisits"]
    total_visits += visits
  return total_visits
  
def gamecount(id):
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://games.roblox.com/v2/groups/{id}/gamesV2?accessFilter=2&limit=100&sortOrder=Asc', timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
  except RequestException as e:
    print(e)
    return 0
  if not data:
    return 0
  else:
    return len(data)  

def groupimage(id):
  # Create a session with retries enabled
  session = FuturesSession()
  retry = Retry(connect=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('https://', adapter)

  # Send the request asynchronously and return a Future object
  future = session.get(f'https://thumbnails.roblox.com/v1/groups/icons?groupIds={id}&size=150x150&format=Png&isCircular=false', timeout=5)

  # Wait for the request to complete and handle any errors that may occur
  try:
    response = future.result()
    icon_url = response.json()
    if "data" in icon_url and len(icon_url["data"]) > 0:
       image = icon_url["data"][0]["imageUrl"]
    else:
       image = "https://cdn.discordapp.com/emojis/894984341665488917.gif?size=44&quality=lossless"

  except RequestException as e:
    print(e)
    image = "https://cdn.discordapp.com/emojis/894984341665488917.gif?size=44&quality=lossless"
  return image 
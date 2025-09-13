import os
import requests
import re
import multiprocessing
from src.main.controllers import Controller
from src.main.arguments import parse_args

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_content_from_sources():
    """
    Makes HTTP requests to the sources, retrieves the content, parses the content for
    proxy information, removes duplicates, and sorts the proxies.
    """
    sources = [
        'https://proxs.ru/freeproxy_efab2cc53937074.txt',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'http://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'http://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
        'http://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
    ]

    content = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)  # Added timeout for robustness
            response.raise_for_status()  # Raise an HTTPError for bad responses
            content.append(response.text)
        except requests.RequestException as e:
            print(f"Error retrieving data from {url}: {e}")

    proxies = []
    regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
    for text in content:
        proxies += re.findall(regex, text)
    
    proxies = list(set(proxies))
    proxies.sort()

    with open('proxies.txt', 'w') as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    
    return proxies

def get_proxies_option():
    while True:
        user_choice = input("Do you want to auto-scrape proxies from sources (1) or use proxies from 'proxies.txt' (2)? Enter 1 or 2: ")
        if user_choice in ['1', '2']:
            return int(user_choice)
        else:
            print("Invalid choice. Please enter 1 or 2.")

def create_proxies_file():
    """Creates an empty 'proxies.txt' file."""
    with open('proxies.txt', 'w') as f:
        f.write('')

# Check if 'proxies.txt' exists and create it if not
if not os.path.exists('proxies.txt'):
    create_proxies_file()

if __name__ == "__main__":
    choice = get_proxies_option()
    
    if choice == 1:
        proxies = get_content_from_sources()
        clear_console()  # Clear the console after scraping proxies
    elif choice == 2:
        # Read proxies from 'proxies.txt'
        try:
            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file]
        except FileNotFoundError:
            print("Error: 'proxies.txt' file not found. Please make sure the file exists with proxy data.")
            exit(1)
    
    # Run the main controller logic
    multiprocessing.freeze_support()
    controller = Controller(arguments=parse_args())
    
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass

import aiohttp
import webbrowser
from bs4 import BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


async def get_statblock_html(creature_name):
    if " " in creature_name:
        creature_name = creature_name.replace(" ", "-")
    creature_name = creature_name.lower().strip("#").strip("+")

    # URL to scrape
    url = f'https://5ecompendium.github.io/bestiary/creature/{creature_name}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Check if request was successful
            if response.status == 200:
                # Parse the HTML content
                return BeautifulSoup(await response.text(), 'html.parser')
            else:
                print(f"Failed to retrieve page. Status code: {response.status}")
                return None


async def get_statblock(creature_name):
    # Get the HTML content
    soup = await get_statblock_html(creature_name)
    if soup is None:
        return None

    try:
        # Extract creature name and type
        creature_name = soup.find('h1').text.strip() if soup.find('h1') else "Unknown Creature"
        creature_type = soup.find('h2').text.strip() if soup.find('h2') else "Unknown Type"

        # Extract abilities
        abilities = {}
        for ability in soup.find_all('div', class_='abilities'):
            for stat in ability.find_all('div'):
                ability_name = stat.find('h4').text.strip() if stat.find('h4') else "Unknown"
                ability_score = stat.find('p').text.strip() if stat.find('p') else "N/A"
                abilities[ability_name] = ability_score

        # Extract special traits
        important_info = {}
        for trait in soup.find_all('div', class_='property-line'):
            trait_name = trait.find('h4').text.strip() if trait.find('h4') else "Unknown"
            trait_value = trait.find('p').text.strip() if trait.find('p') else "N/A"
            important_info[trait_name] = trait_value

        # Function to safely extract text or return a default message
        def safe_extract(header_id):
            header = soup.find('h3', id=header_id)
            if header and header.find_next('p'):
                return header.find_next('p').text.strip()
            return "Not available"

        # Extract actions, reactions, and legendary actions
        actions = safe_extract('actions')
        reactions = safe_extract('reactions')
        legendary_actions = safe_extract('legendary-actions')

        # Compile the statblock
        monster_statblock = {
            "creature_name": creature_name,
            "creature_type": creature_type,
            "ability_scores": abilities,
            "important_info": important_info,
            "actions": actions,
            "reactions": reactions,
            "legendary_actions": legendary_actions
        }

        return monster_statblock

    except Exception as e:
        print(f"Error parsing statblock: {e}")
        return None
def open_statblock(creature_type, driver):
    creature_type = strip_numbers(creature_type)
    url = f'https://5ecompendium.github.io/bestiary/creature/{creature_type}'

    # Specify the path to the GeckoDriver executable
    if driver is None:
        gecko_driver_path = './utils/gecko_driver/geckodriver.exe'  # Change this to your geckodriver path

        # Start a Selenium WebDriver session with Firefox
        service = Service(executable_path=gecko_driver_path)
        driver = webdriver.Firefox(service=service)

    # Check if the URL is already open in any tab
    found = False
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.current_url == url:
            found = True
            break

    # If not found, open the URL in a new tab
    if not found:
        driver.get(url)

        # Optionally, wait for a specific element to ensure the page is loaded
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        except TimeoutException:
            print("Page load timed out!")

    # Focus back on the found or newly opened tab
    if found:
        driver.switch_to.window(handle)

    return driver

def strip_numbers(creature_type):
    creature_type_clean = re.sub(r'\d+', '', creature_type)
    if " " in creature_type_clean:
        creature_type_clean = creature_type_clean.replace(" ", "-")
    creature_type_clean = creature_type_clean.lower().strip("#").strip("+")
    return creature_type_clean
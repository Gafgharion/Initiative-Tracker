import aiohttp
import webbrowser
from bs4 import BeautifulSoup
import re


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
def open_statblock(creature_type):
    creature_type = strip_numbers(creature_type)
    url = f'https://5ecompendium.github.io/bestiary/creature/{creature_type}'
    webbrowser.open(url)

def strip_numbers(creature_type):
    creature_type_clean = re.sub(r'\d+', '', creature_type)
    if " " in creature_type_clean:
        creature_type_clean = creature_type_clean.replace(" ", "-")
    creature_type_clean = creature_type_clean.lower().strip("#").strip("+")
    return creature_type_clean
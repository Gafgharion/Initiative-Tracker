import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def get_statblock(creature_name):
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
                soup = BeautifulSoup(await response.text(), 'html.parser')

                # Extract creature name and type
                creature_name = soup.find('h1').text.strip()
                creature_type = soup.find('h2').text.strip()

                # Extract abilities
                abilities = {}
                for ability in soup.find_all('div', class_='abilities'):
                    for stat in ability.find_all('div'):
                        ability_name = stat.find('h4').text.strip()
                        ability_score = stat.find('p').text.strip()
                        abilities[ability_name] = ability_score

                # Extract special traits
                important_info = {}
                for trait in soup.find_all('div', class_='property-line'):
                    trait_name = trait.find('h4').text.strip()
                    trait_value = trait.find('p').text.strip()
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
            else:
                print(f"Failed to retrieve page. Status code: {response.status}")
                return None

    return monster_statblock

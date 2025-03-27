import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = "https://mtbans.com"  # Replace with the actual URL

# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Check if request was successful

# Parse the HTML page using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with the banlist (in this case the table has the id 'banlist-table')
table = soup.find('table', {'id': 'banlist-table'})

# Find all rows in the table body
rows = table.find('tbody').find_all('tr')

# Iterate through each row and extract the relevant information
banned_users = []
for row in rows:
    # Extract the banned user name
    user_cell = row.find_all('td')[0]
    user_name = user_cell.get_text(strip=True)

    # Extract the user's Steam ID
    user_steam_id = user_cell.find('a').get('href')
    user_steam_id = user_steam_id.replace('https://steamcommunity.com/profiles/', '')
    
    # Extract the "last banned" time
    last_banned_cell = row.find_all('td')[1]
    last_banned = last_banned_cell.get_text(strip=True)
    
    # Extract the ban count (if present)
    ban_count_cell = row.find_all('td')[2]
    ban_count = ban_count_cell.get_text(strip=True).replace(' ', '').replace('\n', ' ')

    # Extract the ban reason(s) if present
    # TODO: Not yet implemented, will likely require a change to selenium, thanks to vue
    ban_reasons = []
    # if ban_count_cell:
    #     ban_count_link = ban_count_cell.find('a')
    #     ban_count_link_url = f"{url}{ban_count_link.get('href')}"
    #     ban_count_link_response = requests.get(ban_count_link_url)
    #     ban_count_link_response.raise_for_status()
    #     ban_count_link_soup = BeautifulSoup(ban_count_link_response.text, 'html.parser')
    #     ban_count_link_table = ban_count_link_soup.find('table', {'id': 'bansview-table'})
    #     ban_count_link_rows = ban_count_link_table.find('tbody').find_all('tr')
    #     for ban_count_link_row in ban_count_link_rows:
    #         ban_reasons.append({
    #             'banned_by': ban_count_link_row.find_all('td')[0].get_text(strip=True),
    #             'server_name': ban_count_link_row.find_all('td')[1].get_text(strip=True),
    #             'issued': ban_count_link_row.find_all('td')[2].get_text(strip=True),
    #             'reason': ban_count_link_row.find_all('td')[3].get_text(strip=True),
    #         })
    
    # Store the data in a dictionary
    banned_users.append({
        'user_name': user_name,
        'user_steam_id': user_steam_id,
        'last_banned': last_banned,
        'ban_count': ban_count,
        'ban_reasons': ban_reasons
    })

# Print the extracted data
for user in banned_users:
    print(user)

import requests
import base64
import json
import re
import os

# Constants
USERNAME = 'your_username'  # Replace with your actual username
PASSWORD = 'your_password'  # Replace with your actual password
DECK_API_ENDPOINT = 'https://your-nextcloud-instance.com/index.php/apps/deck/api/v1.0'
BOARD_NAME = 'Certifications'

def valid_filename(title):
    # Replace ':' with ' - ' and remove other invalid characters
    return re.sub(r'[<>:"/\\|?*]', '', title.replace(':', ' -'))

def fetch_boards():
    basic_auth = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "OCS-APIRequest": "true",
        "Content-Type": "application/json"
    }
    url = f"{DECK_API_ENDPOINT}/boards"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except json.JSONDecodeError:
        print("Error parsing response as JSON.")
        return []

def fetch_board_id(boards):
    for board in boards:
        if isinstance(board, dict) and board.get('title') == BOARD_NAME:
            return board.get('id')
    return None

def fetch_cards(board_id):
    basic_auth = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "OCS-APIRequest": "true",
        "Content-Type": "application/json"
    }
    url = f"{DECK_API_ENDPOINT}/boards/{board_id}/stacks"
    response = requests.get(url, headers=headers)
    try:
        stacks = response.json()
    except json.JSONDecodeError:
        print("Error parsing response as JSON.")
        return []

    card_details = []
    for stack in stacks:
        if isinstance(stack, dict):
            for card in stack.get('cards', []):
                if isinstance(card, dict):
                    card_details.append({
                        'title': card.get('title', 'Untitled'),
                        'description': card.get('description', '')  # Adjust field name if necessary
                    })
    return card_details

def write_card_to_file(title, description):
    # Skip writing file if description is empty
    if not description.strip():
        return

    directory = f"Cards/{BOARD_NAME}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, valid_filename(title) + '.md')
    with open(filename, 'w') as file:
        file.write(description)

def fetch_stacks_and_cards(board_id):
    basic_auth = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {basic_auth}",
        "OCS-APIRequest": "true",
        "Content-Type": "application/json"
    }
    url = f"{DECK_API_ENDPOINT}/boards/{board_id}/stacks"
    response = requests.get(url, headers=headers)
    try:
        stacks = response.json()
    except json.JSONDecodeError:
        print("Error parsing response as JSON.")
        return []

    stacks_with_cards = {}
    for stack in stacks:
        stack_title = stack.get('title', 'Unknown')
        card_dicts = [{'title': card.get('title', 'Untitled'), 'description': card.get('description', '')} 
                      for card in stack.get('cards', []) if isinstance(card, dict)]
        stacks_with_cards[stack_title] = card_dicts
    return stacks_with_cards

def write_main_markdown(stacks_with_cards):
    main_file_path = f"{BOARD_NAME}.md"
    with open(main_file_path, 'w') as file:
        file.write("---\n\nkanban-plugin: basic\n\n---\n\n")

        # Reverse the order of stacks
        for stack, cards in reversed(stacks_with_cards.items()):
            file.write(f"## {stack}\n\n")
            for card in cards:
                if card['description'].strip():  # Check if description is not empty
                    valid_title = valid_filename(card['title'])
                    file.write(f"- [ ] [[{valid_title}]]\n")
                else:
                    file.write(f"- [ ] {card['title']}\n")  # Non-linked format for empty cards
            file.write("\n")

        kanban_settings = json.dumps({
            "kanban-plugin": "basic",
            "new-note-folder": f"Kanban/Cards/{BOARD_NAME}"
        })
        file.write(f"%% kanban:settings\n```\n{kanban_settings}\n```\n%%\n")

def main():
    try:
        boards = fetch_boards()
        board_id = fetch_board_id(boards)
        if board_id is None:
            print("Board not found.")
            return

        stacks_with_cards = fetch_stacks_and_cards(board_id)

        # Writing individual card markdown files
        for stack, cards in stacks_with_cards.items():
            for card in cards:
                card_title = card.get('title', 'Untitled')
                card_description = card.get('description', '')
                write_card_to_file(card_title, card_description)

        # Writing the main markdown file
        write_main_markdown(stacks_with_cards)

        print(f"{BOARD_NAME}.md file created with current card statuses.")
        print("Individual markdown files for each card are also created.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Nextcloud Deck to Obsidian Kanban Migration Script
This was written with AI. [ChatGPT Share](https://chat.openai.com/share/ada3f5f5-1966-4ebf-baa9-ef2fc63ecf9d)

## Overview
This Python script facilitates the migration of kanban boards from Nextcloud Deck to The [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban). It fetches cards from a specified board in Nextcloud Deck and creates corresponding markdown files for use as notes in Obsidian.

## Features
- Fetches cards from a specified Nextcloud Deck board.
- Generates individual markdown files for each card with content.
- Creates a main markdown file that organizes cards into their respective stacks as seen in Nextcloud Deck for [Obsidian Kanban](https://github.com/mgmeyers/obsidian-kanban) compatibility.
- Skips empty cards and does not create links for them in the main file.
- Handles special characters in card titles to ensure compatibility with filesystem constraints.

## Requirements
- Python environment with `requests` library installed.
- Access credentials (username and password) for Nextcloud Deck.
- URL to the Nextcloud Deck instance.

## Usage
1. **Configuration**: Set your Nextcloud credentials and the URL of your Nextcloud Deck instance in the script.
2. **Specify Board Name**: Set the `BOARD_NAME` variable to the name of the board you wish to migrate.
3. **Run the Script**: Execute the script. It will create a directory named "Cards/<BOARD_NAME>" and place individual card markdown files within it. Additionally, a main markdown file named "<BOARD_NAME>.md" is created.

## Notes
- The script assumes a standard JSON response structure from the Nextcloud Deck API.
- Cards without content are noted but not linked in the main markdown file.
- The script assumes you place your boards in "Kanban/", you can change the settings in the board to change the new location of the cards.

## Limitations
- The script does not migrate attachments or images.

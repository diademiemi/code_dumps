import pygame
import re
import os
import textwrap
import time

# Markdown parsing
def parse_markdown(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except IOError:
        return []

    tiers = []
    current_tier = None
    for line in lines:
        if line.startswith('# '):
            if current_tier:
                tiers.append(current_tier)
            header, color = re.findall(r'\[(.*?)\]\((.*?)\)', line)[0]
            current_tier = {'header': header, 'color': color, 'items': []}
        elif line.startswith('- '):
            img_match = re.search(r'!\[.*?\]\((.*?)\)', line)
            text = re.search(r'\[(.*?)\]', line)
            if img_match:
                img_path = img_match.group(1)
                if text:
                    text = text.group(1)
                    current_tier['items'].append(('image_text', text, img_path))
                else:
                    current_tier['items'].append(('image', img_path))
            else:
                item = line.strip('- ').strip()
                current_tier['items'].append(('text', item))
    if current_tier:
        tiers.append(current_tier)
    return tiers

# Pygame rendering
pygame.init()

# Configuration
WIDTH, HEIGHT = 800, 600
ITEM_SIZE = 100
FONT_SIZE = 18
SIDE_BAR_WIDTH = ITEM_SIZE * 3 // 4
MARKDOWN_FILE = 'example.md'
RELOAD_INTERVAL = 1  # Seconds

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Markdown Tier List')
font = pygame.font.SysFont('Impact', FONT_SIZE)
clock = pygame.time.Clock()

def load_image(path):
    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (ITEM_SIZE, ITEM_SIZE))
    else:
        # Return a placeholder if the image does not exist
        placeholder = pygame.Surface((ITEM_SIZE, ITEM_SIZE))
        placeholder.fill((255, 0, 0))
        return placeholder

def render_text(surface, text, pos, max_width, max_lines, border_size=2):
    lines = textwrap.wrap(text, max_width)
    if len(lines) > max_lines:
        font_size = FONT_SIZE * (max_lines // len(lines) + 1)
        font = pygame.font.SysFont('Impact', font_size)
    else:
        font = pygame.font.SysFont('Impact', FONT_SIZE)

    def render_with_border(line, x, y):
        # Render the border
        text_surface = font.render(line, True, (0, 0, 0))
        offsets = [(ox, oy) for ox in range(-border_size, border_size + 1) for oy in range(-border_size, border_size + 1) if ox != 0 or oy != 0]
        for offset in offsets:
            surface.blit(text_surface, (x + offset[0], y + offset[1]))

        # Render the original text
        text_surface = font.render(line, True, (255, 255, 255))
        surface.blit(text_surface, (x, y))

    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(ITEM_SIZE // 2, pos))
        render_with_border(line, text_rect.x, text_rect.y)
        pos += font.get_height()

def render_item(item_type, text='', img_path=None):
    surface = pygame.Surface((ITEM_SIZE, ITEM_SIZE))
    if item_type == 'text':
        surface.fill((20, 20, 20))
        lines = textwrap.wrap(text, 15)
        render_text(surface, text, ITEM_SIZE // 2 - (len(lines) - 1) * 9, max_width=15, max_lines=2)
    elif item_type == 'image':
        surface.blit(load_image(img_path), (0, 0))
    elif item_type == 'image_text':
        surface.blit(load_image(img_path), (0, 0))

        lines = textwrap.wrap(text, 15)

        render_text(surface, text, ITEM_SIZE - FONT_SIZE - (len(lines) - 1) * 18, max_width=15, max_lines=2)
    return surface

def main():
    last_reload_time = time.time()
    tiers = parse_markdown(MARKDOWN_FILE)
    running = True

    while running:
        current_time = time.time()
        if current_time - last_reload_time >= RELOAD_INTERVAL:
            tiers = parse_markdown(MARKDOWN_FILE)
            last_reload_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((25, 25, 25))  # Background color
        x, y = SIDE_BAR_WIDTH, 0

        for tier in tiers:
            num_items = len(tier['items'])
            tier_rows = (num_items - 1) // ((WIDTH - SIDE_BAR_WIDTH) // ITEM_SIZE) + 1
            tier_height = tier_rows * ITEM_SIZE
            # Draw sidebar for the tier
            header_surface = font.render(tier['header'], True, (0, 0, 0))
            header_bg = pygame.Surface((SIDE_BAR_WIDTH, tier_height))
            header_bg.fill(pygame.Color(tier['color']))
            screen.blit(header_bg, (0, y))
            screen.blit(header_surface, (10, y + (tier_height - FONT_SIZE) // 2))

            # Draw items in the tier
            x = SIDE_BAR_WIDTH
            for i, item in enumerate(tier['items']):
                if x + ITEM_SIZE > WIDTH:
                    x = SIDE_BAR_WIDTH
                    y += ITEM_SIZE
                item_surface = render_item(*item)
                screen.blit(item_surface, (x, y))
                x += ITEM_SIZE

            y += 100

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
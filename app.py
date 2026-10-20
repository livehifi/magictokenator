import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# 300 DPI dimensions for 30mm x 50mm
WIDTH = 354
HEIGHT = 591

# --- MTG Data Dictionaries ---
MTG_TYPES = [
    "✏️ Custom Type...",
    "Token Creature", "Token Artifact", "Token Enchantment", "Token",
    "Creature", "Artifact", "Enchantment", "Land", "Planeswalker", "Battle"
]

MTG_SUBTYPES = [
    "None", "✏️ Custom Subtype...",
    "Advisor", "Angel", "Ape", "Archer", "Artificer", "Assassin", "Assembly-Worker", "Avatar", 
    "Barbarian", "Basilisk", "Bat", "Bear", "Beast", "Berserker", "Bird", "Blood", "Boar", 
    "Cat", "Centaur", "Cleric", "Clue", "Construct", "Coward", "Crab", "Crocodile", 
    "Demon", "Devil", "Dinosaur", "Djinn", "Dog", "Dragon", "Drake", "Druid", "Dwarf", 
    "Elemental", "Elephant", "Elf", "Equipment", 
    "Faerie", "Fish", "Food", "Fox", "Frog", "Fungus", 
    "Gargoyle", "Giant", "Goblin", "God", "Golem", "Griffin", 
    "Hag", "Harpy", "Hellion", "Hippopotamus", "Homunculus", "Horror", "Horse", "Hound", "Human", "Hydra", 
    "Illusion", "Imp", "Incarnation", "Incubator", "Insect", 
    "Juggernaut", "Kavu", "Kithkin", "Knight", "Kobold", "Kraken", 
    "Leech", "Leviathan", "Lizard", "Map", "Manticore", "Masticore", "Mercenary", "Merfolk", "Minotaur", "Monk", "Mutant", "Myr", "Mystic", 
    "Naga", "Ninja", "Noble", "Nymph", "Ogre", "Ooze", "Orc", 
    "Pegasus", "Pest", "Phyrexian", "Pilot", "Plant", "Powerstone", 
    "Rat", "Rebel", "Rhino", "Rogue", 
    "Salamander", "Samurai", "Saproling", "Scarecrow", "Scorpion", "Serpent", "Shade", "Shaman", "Shapeshifter", "Shard", "Skeleton", "Slime", "Sliver", "Soldier", "Soltari", "Sphinx", "Spider", "Spirit", "Sponge", "Squid", "Squirrel", "Starfish", "Survivor", 
    "Tentacle", "Thopter", "Treasure", "Treefolk", "Troll", "Turtle", 
    "Unicorn", "Vampire", "Vedalken", "Viashino", "Wall", "Warrior", "Weird", "Werewolf", "Whale", "Wizard", "Wolf", "Wolverine", "Wombat", "Worm", "Wraith", "Wurm", 
    "Yeti", "Zombie"
]

def generate_label(name, card_type_str, text, power, toughness, rotate_landscape):
    # Create white canvas
    img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    
    font_bold_path = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    font_reg_path = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

    max_text_width = WIDTH - 50 # 25px padding on left and right

    # --- Auto-Scale Name Font ---
    name_size = 32
    try:
        font_title = ImageFont.truetype(font_bold_path, name_size)
        while draw.textlength(name, font=font_title) > max_text_width and name_size > 12:
            name_size -= 1
            font_title = ImageFont.truetype(font_bold_path, name_size)
    except IOError:
        font_title = ImageFont.load_default()

    # --- Auto-Scale Type/Subtype Font ---
    type_size = 26
    try:
        font_type = ImageFont.truetype(font_bold_path, type_size)
        while draw.textlength(card_type_str, font=font_type) > max_text_width and type_size > 10:
            type_size -= 1
            font_type = ImageFont.truetype(font_bold_path, type_size)
    except IOError:
        font_type = ImageFont.load_default()

    # Static Fonts for Rules Text and P/T
    try:
        font_text =
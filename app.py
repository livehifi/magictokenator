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
        font_text = ImageFont.truetype(font_reg_path, 24)
        font_pt   = ImageFont.truetype(font_bold_path, 30)
    except IOError:
        font_text = font_pt = ImageFont.load_default()

    # Outer Border
    draw.rectangle([10, 10, WIDTH-10, HEIGHT-10], outline="black", width=4)

    # Name Box (Vertically centered based on scaled font size)
    draw.rectangle([15, 15, WIDTH-15, 65], outline="black", width=2, fill="#e8e8e8")
    name_bbox = draw.textbbox((0, 0), name, font=font_title)
    name_y = 15 + (50 - (name_bbox[3] - name_bbox[1])) // 2 - 2
    draw.text((25, name_y), name, font=font_title, fill="black")

    # Blank Art Box Placeholder
    draw.rectangle([15, 70, WIDTH-15, 315], outline="black", width=2, fill="#ffffff")

    # Type Box (Vertically centered based on scaled font size)
    draw.rectangle([15, 320, WIDTH-15, 365], outline="black", width=2, fill="#e8e8e8")
    type_bbox = draw.textbbox((0, 0), card_type_str, font=font_type)
    type_y = 320 + (45 - (type_bbox[3] - type_bbox[1])) // 2 - 2
    draw.text((25, type_y), card_type_str, font=font_type, fill="black")

    # Text Box
    draw.rectangle([15, 370, WIDTH-15, HEIGHT-15], outline="black", width=2, fill="#fdfdfd")
    
    # Wrap and draw rules text
    lines = textwrap.wrap(text, width=28)
    y_text = 380
    for line in lines:
        draw.text((25, y_text), line, font=font_text, fill="black")
        y_text += 28

    # Power/Toughness Box (Bottom Right)
    if power or toughness:
        pt_text = f"{power} / {toughness}"
        pt_bbox = draw.textbbox((0, 0), pt_text, font=font_pt)
        pt_width = pt_bbox[2] - pt_bbox[0]
        
        pt_x = WIDTH - pt_width - 35
        pt_y = HEIGHT - 65
        
        draw.rectangle([pt_x - 12, pt_y - 5, WIDTH - 15, HEIGHT - 15], outline="black", width=2, fill="#e8e8e8")
        draw.text((pt_x, pt_y), pt_text, font=font_pt, fill="black")

    # Rotate for 50x30mm landscape printers if requested
    if rotate_landscape:
        img = img.rotate(-90, expand=True)

    return img

st.set_page_config(page_title="MTG Label Proxy Maker")
st.title("MTG Token Label Maker")
st.write("Generates a print-ready PNG for a 50mm x 30mm label printer.")

# UI Inputs
name = st.text_input("Card Name", "Zombie")

# Type Selection
col_type, col_sub = st.columns(2)

with col_type:
    selected_type = st.selectbox("Type", MTG_TYPES, index=1)
    if selected_type == "✏️ Custom Type...":
        final_type = st.text_input("Enter Custom Type", "Creature")
    else:
        final_type = selected_type

with col_sub:
    selected_sub = st.selectbox("Subtype", MTG_SUBTYPES, index=MTG_SUBTYPES.index("Zombie"))
    if selected_sub == "✏️ Custom Subtype...":
        final_sub = st.text_input("Enter Custom Subtype", "Warrior")
    elif selected_sub == "None":
        final_sub = ""
    else:
        final_sub = selected_sub

# Combine Type and Subtype
if final_sub.strip():
    card_type_str = f"{final_type} - {final_sub}"
else:
    card_type_str = final_type

text = st.text_area("Text Box", "This creature enters the battlefield tapped.")

col1, col2 = st.columns(2)
power = col1.text_input("Power", "2")
toughness = col2.text_input("Toughness", "2")

rotate = st.checkbox("Rotate 90° for Landscape Feed (50x30mm)", value=True)

if st.button("Generate Token", type="primary"):
    img = generate_label(name, card_type_str, text, power, toughness, rotate)
    
    # Show Preview
    st.image(img, caption="Token Preview", width=300)
    
    # Prepare Download
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download PNG Label",
        data=byte_im,
        file_name=f"{name.replace(' ', '_')}_token.png",
        mime="image/png"
    )
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

# 300 DPI dimensions for 30mm x 50mm
WIDTH = 354
HEIGHT = 591

def generate_label(name, card_type, text, power, toughness, rotate_landscape):
    # Create white canvas
    img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    draw = ImageDraw.Draw(img)

    # Load fonts (using system fonts installed via Docker)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 26)
        font_type = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 20)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 18)
        font_pt = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 24)
    except IOError:
        font_title = font_type = font_text = font_pt = ImageFont.load_default()

    # Outer Border
    draw.rectangle([10, 10, WIDTH-10, HEIGHT-10], outline="black", width=4)

    # Name Box
    draw.rectangle([15, 15, WIDTH-15, 60], outline="black", width=2, fill="#e8e8e8")
    draw.text((25, 22), name, font=font_title, fill="black")

    # Blank Art Box Placeholder
    draw.rectangle([15, 65, WIDTH-15, 315], outline="black", width=2, fill="#ffffff")

    # Type Box
    draw.rectangle([15, 320, WIDTH-15, 360], outline="black", width=2, fill="#e8e8e8")
    draw.text((25, 328), card_type, font=font_type, fill="black")

    # Text Box
    draw.rectangle([15, 365, WIDTH-15, HEIGHT-15], outline="black", width=2, fill="#fdfdfd")
    
    # Wrap and draw rules text
    lines = textwrap.wrap(text, width=38)
    y_text = 375
    for line in lines:
        draw.text((25, y_text), line, font=font_text, fill="black")
        y_text += 22

    # Power/Toughness Box (Bottom Right)
    if power or toughness:
        pt_text = f"{power} / {toughness}"
        pt_bbox = draw.textbbox((0, 0), pt_text, font=font_pt)
        pt_width = pt_bbox[2] - pt_bbox[0]
        
        pt_x = WIDTH - pt_width - 30
        pt_y = HEIGHT - 55
        
        draw.rectangle([pt_x - 10, pt_y - 5, WIDTH - 15, HEIGHT - 15], outline="black", width=2, fill="#e8e8e8")
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
card_type = st.text_input("Type - Subtype", "Token Creature - Zombie")
text = st.text_area("Text Box", "This creature enters the battlefield tapped.")

col1, col2 = st.columns(2)
power = col1.text_input("Power", "2")
toughness = col2.text_input("Toughness", "2")

rotate = st.checkbox("Rotate 90° for Landscape Feed (50x30mm)", value=True)

if st.button("Generate Token", type="primary"):
    img = generate_label(name, card_type, text, power, toughness, rotate)
    
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
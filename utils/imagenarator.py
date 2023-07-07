import re
import textwrap
import os

from PIL import Image, ImageDraw, ImageFont
from rich.progress import track
from TTS.engine_wrapper import process_text

def draw_multiple_line_text(
    image, text, font, text_color, padding, wrap=10, transparent=True
) -> None:
    """
    Draw multiline text over given image
    """
    draw = ImageDraw.Draw(image)
    Fontperm = font.getsize(text)
    image_width, image_height = image.size
    lines = textwrap.wrap(text, width=wrap)

    y = (image_height / 2) - (
        ((Fontperm[1] + (len(lines) * padding) / len(lines)) * len(lines)) / 2
    )
    for line in lines:
        line_width, line_height = font.getsize(line)
        if transparent:
            shadowcolor = "black"
            for i in range(1, 5):
                draw.text(
                    ((image_width - line_width) / 2 - i, y - i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 + i, y - i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 - i, y + i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 + i, y + i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
        draw.text(((image_width - line_width) / 2, y), line, font=font, fill=text_color)
        y += line_height + padding

def split_string(string, max_words):
    words = string.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def remove_spaces(string):
    string = re.sub(r'\. +', '.', string)
    string = re.sub(r'\.', '. ', string)
    return string

def imagemaker(theme, reddit_obj: dict, txtclr, padding=0, transparent=True) -> None:
    """
    Render Images for video
    """
    title = process_text(reddit_obj["thread_title"], False)
    texts = reddit_obj["thread_post"]
    id = re.sub(r"[^\w\s-]", "", reddit_obj["thread_id"])
    
    concat_texts = ''.join(texts)
    concat_texts = remove_spaces(concat_texts)
    bite_size_texts = split_string(concat_texts, 3)
    bite_size_texts.append('quibble')

    if transparent:
        font = ImageFont.truetype(os.path.join("fonts", "Roboto-Bold.ttf"), 220)
        tfont = ImageFont.truetype(os.path.join("fonts", "Roboto-Bold.ttf"), 200)
    else:
        tfont = ImageFont.truetype(
            os.path.join("fonts", "Roboto-Bold.ttf"), 200
        )  # for title
        font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), 220)
    size = (1920, 1080)

    image = Image.new("RGBA", size, theme)

    # for title
    draw_multiple_line_text(
        image, title, tfont, txtclr, padding, wrap=30, transparent=transparent
    )

    image.save(f"assets/temp/{id}/png/title.png")

    for idx, text in track(enumerate(bite_size_texts), "Rendering Image"):
        image = Image.new("RGBA", size, theme)
        text = process_text(text, False)
        draw_multiple_line_text(
            image, text, font, txtclr, padding, wrap=30, transparent=transparent
        )
        image.save(f"assets/temp/{id}/png/img{idx}.png")

import mcp.types as types
from mcp.server.fastmcp import FastMCP, Image
from typing import Any, Dict, List
from dataclasses import dataclass
from pydantic import BaseModel,ConfigDict,Field,ValidationError
import json
import random
import re

## Constants
ASSETS_DIR = "assets"
MIMETYPE = "image/jpeg"


## Dataclasses
@dataclass(frozen=True)
class TarotCard:
    name: str
    number: str
    arcana: str
    suit: str
    img_path: str
    is_reversed: bool = False
    
    def __str__(self) -> str:
        if self.suit:
            return f"{self.name} of {self.suit} {'reversed' if self.is_reversed else ''}"
        return f"{self.name} ({self.arcana}) {'reversed' if self.is_reversed else ''}"
    
    def __repr__(self) -> str:
        """
        since the name for my asset is already unique and has all the info I just will try to
        turn name into snakecase format example:
        Ten of Pentacles -> ten_of_pentacles
        """
        return to_snake_slug(self.name)
    

## Util funcs
def load_asset_card(img_name:str)->str:
    return f"{ASSETS_DIR}/cards/{img_name}"

def load_all_cards()-> List[TarotCard]:
    cards = []
    with open(f"{ASSETS_DIR}/tarot-images.json") as f:
        card_data = json.load(f)
    for card_info in card_data['cards']:
        cards.append(
            TarotCard(
                name=card_info['name'],
                number=card_info['number'],
                arcana=card_info.get('arcana',""), 
                suit=card_info.get("suit","") or "",
                img_path=card_info['img']
            )
        )
    return cards

def to_snake_slug(text:str)->str:
    """
    Converts a string like "Ten of Pentacles" into "ten_of_pentacles".
    
    1.  Converts to lowercase.
    2.  Removes non-alphanumeric characters (like ' or ()).
    3.  Replaces one or more spaces (or hyphens) with a single underscore.
    4.  Strips any leading/trailing underscores.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", '', text)
    text = re.sub(r'[\s-]+', '_', text)
    text = text.strip('_')
    return text

SLUG_TO_CARDS :  Dict[str,TarotCard] = {repr(e):e for e in load_all_cards()}

def get_card_by_slug(slug_name:str)-> TarotCard:
    return SLUG_TO_CARDS[slug_name]

## MCP
mcp = FastMCP(
    name="tarot-python",
    stateless_http=True,
)


# Track drawn cards for a reading session state
DRAWN_CARDS: List[TarotCard] = []

@mcp.resource("tarot://cards/image/{card_name_slug}",mime_type="image/jpeg")
def get_card_image(card_name_slug:str) -> bytes:
    """returns the image of the particular card given the card_name_slug for instance given
    card_name:ten_of_pentacles it returns the Ten of Pentacles card
    remember card_name_slug should be snake case"""
    card = get_card_by_slug(card_name_slug)
    image_path = f"{ASSETS_DIR}/cards/{card.img_path}"
    # 3. Read the file as raw bytes and return them
    with open(image_path, 'rb') as f:
        base64_encoded = f.read()
    return base64_encoded
    
# @mcp.tool()
# def get_spread(number_of_cards: int) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
#     """
#     Draw random tarot cards from the deck for a reading.
    
#     Args:
#         number_of_cards: Number of cards to draw (1-10)
    
#     Returns:
#         A list of randomly selected tarot cards with their images
#     """
#     pass

# # TODO: this makes this stateful
# @mcp.tool()
# def get_additional_tarot_card() -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
#     """
#     Draw one additional tarot card to add to the current reading.
#     This card will not be one that was already drawn in the current reading.
    
#     Returns:
#         One additional randomly selected tarot card with its image
#     """
#     pass

if __name__ == "__main__":
    mcp.run()


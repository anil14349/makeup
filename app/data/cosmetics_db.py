"""
Cosmetics database module.
Contains the product recommendations database organized by skin tone.
"""
from typing import Dict, List, Any

# Define database of cosmetic products by skin tone
COSMETIC_DATABASE: Dict[str, List[Dict[str, str]]] = {
    "fair": [
        # Face Products
        {"name": "Foundation", "brand": "Maybelline", "color": "Ivory"},
        {"name": "Foundation", "brand": "Estée Lauder", "color": "Cool Bone"},
        {"name": "Foundation", "brand": "MAC", "color": "NW10"},
        {"name": "Foundation", "brand": "Charlotte Tilbury", "color": "1 Cool"},
        {"name": "Concealer", "brand": "NARS", "color": "Chantilly"},
        {"name": "Concealer", "brand": "Tarte", "color": "Fair Beige"},
        {"name": "Powder", "brand": "Laura Mercier", "color": "Translucent"},
        {"name": "Powder", "brand": "Fenty Beauty", "color": "Lavender"},
        
        # Cheek Products
        {"name": "Blush", "brand": "L'Oreal", "color": "Peach"},
        {"name": "Blush", "brand": "Benefit", "color": "Dandelion"},
        {"name": "Blush", "brand": "Rare Beauty", "color": "Bliss"},
        {"name": "Bronzer", "brand": "Benefit", "color": "Hoola Lite"},
        {"name": "Bronzer", "brand": "Physician's Formula", "color": "Light Bronze"},
        {"name": "Highlighter", "brand": "Becca", "color": "Moonstone"},
        {"name": "Highlighter", "brand": "Rare Beauty", "color": "Enlighten"},
        
        # Lip Products
        {"name": "Lipstick", "brand": "MAC", "color": "Pink Nouveau"},
        {"name": "Lipstick", "brand": "MAC", "color": "Creme Cup"},
        {"name": "Lipstick", "brand": "Charlotte Tilbury", "color": "Pillow Talk"},
        {"name": "Lip Gloss", "brand": "Fenty Beauty", "color": "Diamond Milk"},
        {"name": "Lip Gloss", "brand": "Glossier", "color": "Clear"},
        {"name": "Lip Liner", "brand": "MAC", "color": "Soar"},
        {"name": "Lip Liner", "brand": "Charlotte Tilbury", "color": "Pillow Talk"},
        
        # Eye Products
        {"name": "Eyeshadow Palette", "brand": "Urban Decay", "color": "Naked3"},
        {"name": "Eyeshadow Palette", "brand": "Huda Beauty", "color": "New Nude"},
        {"name": "Eyeliner", "brand": "Stila", "color": "Black"},
        {"name": "Eyeliner", "brand": "Urban Decay", "color": "Bourbon"},
        {"name": "Mascara", "brand": "Maybelline", "color": "Blackest Black"},
        {"name": "Mascara", "brand": "Benefit", "color": "They're Real"},
        {"name": "Eyebrow Pencil", "brand": "Anastasia Beverly Hills", "color": "Taupe"},
        {"name": "Eyebrow Gel", "brand": "Glossier", "color": "Blonde"},
    ],
    "medium": [
        # Face Products
        {"name": "Foundation", "brand": "Fenty Beauty", "color": "290"},
        {"name": "Foundation", "brand": "NARS", "color": "Syracuse"},
        {"name": "Foundation", "brand": "Giorgio Armani", "color": "6.5"},
        {"name": "Foundation", "brand": "Bobbi Brown", "color": "Golden Natural"},
        {"name": "Concealer", "brand": "Too Faced", "color": "Golden Medium"},
        {"name": "Concealer", "brand": "Huda Beauty", "color": "Shortbread"},
        {"name": "Powder", "brand": "Laura Mercier", "color": "Medium Deep"},
        {"name": "Powder", "brand": "Fenty Beauty", "color": "Banana"},
        
        # Cheek Products
        {"name": "Blush", "brand": "NARS", "color": "Orgasm"},
        {"name": "Blush", "brand": "Milani", "color": "Luminoso"},
        {"name": "Blush", "brand": "Rare Beauty", "color": "Joy"},
        {"name": "Bronzer", "brand": "Fenty Beauty", "color": "Caramel Cutie"}, 
        {"name": "Bronzer", "brand": "Huda Beauty", "color": "Medium"},
        {"name": "Highlighter", "brand": "Becca", "color": "Champagne Pop"},
        {"name": "Highlighter", "brand": "Fenty Beauty", "color": "Hustla Baby"},
        
        # Lip Products
        {"name": "Lipstick", "brand": "Revlon", "color": "Rosewood"},
        {"name": "Lipstick", "brand": "MAC", "color": "Whirl"},
        {"name": "Lipstick", "brand": "Pat McGrath", "color": "1995"},
        {"name": "Lip Gloss", "brand": "Fenty Beauty", "color": "Fenty Glow"},
        {"name": "Lip Gloss", "brand": "Pat McGrath", "color": "Flesh Fantasy"},
        {"name": "Lip Liner", "brand": "Makeup Forever", "color": "Wherever Walnut"},
        {"name": "Lip Liner", "brand": "NYX", "color": "Natural"},
        
        # Eye Products
        {"name": "Eyeshadow Palette", "brand": "Morphe", "color": "35O Nature Glow"},
        {"name": "Eyeshadow Palette", "brand": "Natasha Denona", "color": "Bronze"},
        {"name": "Eyeliner", "brand": "Urban Decay", "color": "Whiskey"},
        {"name": "Eyeliner", "brand": "Charlotte Tilbury", "color": "Copper Charge"},
        {"name": "Mascara", "brand": "L'Oreal", "color": "Voluminous Carbon Black"},
        {"name": "Mascara", "brand": "Too Faced", "color": "Better Than Sex"},
        {"name": "Eyebrow Pencil", "brand": "Anastasia Beverly Hills", "color": "Medium Brown"},
        {"name": "Eyebrow Gel", "brand": "Benefit", "color": "3.5"},
    ],
    "dark": [
        # Face Products
        {"name": "Foundation", "brand": "Huda Beauty", "color": "Chocolate"},
        {"name": "Foundation", "brand": "Fenty Beauty", "color": "460"},
        {"name": "Foundation", "brand": "NARS", "color": "Macao"},
        {"name": "Foundation", "brand": "Pat McGrath", "color": "Deep 34"},
        {"name": "Concealer", "brand": "Fenty Beauty", "color": "420"},
        {"name": "Concealer", "brand": "NARS", "color": "Walnut"},
        {"name": "Powder", "brand": "Laura Mercier", "color": "Deep"},
        {"name": "Powder", "brand": "Fenty Beauty", "color": "Nutmeg"},
        
        # Cheek Products
        {"name": "Blush", "brand": "NYX", "color": "Berry"},
        {"name": "Blush", "brand": "Fenty Beauty", "color": "Summertime Wine"},
        {"name": "Blush", "brand": "NARS", "color": "Exhibit A"},
        {"name": "Bronzer", "brand": "Fenty Beauty", "color": "Coco Naughty"},
        {"name": "Bronzer", "brand": "Huda Beauty", "color": "Rich"},
        {"name": "Highlighter", "brand": "Fenty Beauty", "color": "Trophy Wife"},
        {"name": "Highlighter", "brand": "Pat McGrath", "color": "Bronze Nectar"},
        
        # Lip Products
        {"name": "Lipstick", "brand": "Fenty Beauty", "color": "Deep Plum"},
        {"name": "Lipstick", "brand": "Pat McGrath", "color": "Elson"},
        {"name": "Lipstick", "brand": "MAC", "color": "Ruby Woo"},
        {"name": "Lip Gloss", "brand": "Fenty Beauty", "color": "Hot Chocolit"},
        {"name": "Lip Gloss", "brand": "Pat McGrath", "color": "Bronze Temptation"},
        {"name": "Lip Liner", "brand": "MAC", "color": "Nightmoth"},
        {"name": "Lip Liner", "brand": "Fenty Beauty", "color": "Cocoa Drizzle"},
        
        # Eye Products
        {"name": "Eyeshadow Palette", "brand": "Juvia's Place", "color": "The Nubian"},
        {"name": "Eyeshadow Palette", "brand": "Pat McGrath", "color": "Mothership V"},
        {"name": "Eyeliner", "brand": "Fenty Beauty", "color": "In Big Truffle"},
        {"name": "Eyeliner", "brand": "Urban Decay", "color": "Perversion"},
        {"name": "Mascara", "brand": "Lancôme", "color": "Monsieur Big"},
        {"name": "Mascara", "brand": "Pat McGrath", "color": "FetishEyes"},
        {"name": "Eyebrow Pencil", "brand": "Anastasia Beverly Hills", "color": "Ebony"},
        {"name": "Eyebrow Gel", "brand": "Benefit", "color": "6"},
    ],
}

def get_product_by_category(skin_tone: str, category: str = None, brand: str = None, max_items: int = None) -> List[Dict[str, str]]:
    """
    Get products filtered by skin tone, category and/or brand.
    
    Args:
        skin_tone: The skin tone to get products for ('fair', 'medium', 'dark')
        category: Optional category filter
        brand: Optional brand filter
        max_items: Optional limit on number of results
        
    Returns:
        List of matching products
    """
    if skin_tone not in COSMETIC_DATABASE:
        return []
        
    products = COSMETIC_DATABASE[skin_tone]
    
    # Apply category filter if specified
    if category:
        products = [p for p in products if category.lower() in p["name"].lower()]
        
    # Apply brand filter if specified
    if brand:
        products = [p for p in products if p["brand"] == brand]
        
    # Apply limit if specified
    if max_items and max_items > 0:
        products = products[:max_items]
        
    return products 
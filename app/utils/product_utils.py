"""
Utility functions for product filtering, categorization, and organization.
"""
from typing import Dict, List, Any
from itertools import groupby
from operator import itemgetter

def categorize_product(product: Dict[str, str]) -> str:
    """
    Categorize a product based on its name.
    
    Args:
        product: Product dictionary with a 'name' key
        
    Returns:
        String category name
    """
    name = product["name"].lower()
    
    # Eye products
    if any(eye_term in name for eye_term in ["eyeshadow", "eyeliner", "mascara", "eyebrow"]):
        return "Eye Products"
    
    # Lip products
    elif any(lip_term in name for lip_term in ["lipstick", "lip gloss", "lip liner"]):
        return "Lip Products"
    
    # Cheek products
    elif any(cheek_term in name for cheek_term in ["blush", "bronzer", "highlighter"]):
        return "Cheek Products"
    
    # Face products
    elif any(face_term in name for face_term in ["foundation", "concealer", "powder"]):
        return "Face Products"
    
    # Default category
    else:
        return "Other Products"

def extract_product_type(product: Dict[str, str]) -> str:
    """
    Extract the product type from product name.
    
    Args:
        product: Product dictionary with a 'name' key
        
    Returns:
        Product type (e.g., 'foundation', 'lipstick')
    """
    if not product or "name" not in product:
        return ""
    
    # Simple extraction: use the first word of the product name
    return product["name"].split()[0].lower()

def get_unique_brands(product_list: List[Dict[str, str]]) -> List[str]:
    """
    Get a list of unique brands from a product list.
    
    Args:
        product_list: List of product dictionaries
        
    Returns:
        Sorted list of unique brand names
    """
    brands = set()
    for item in product_list:
        if "error" not in item and "brand" in item:
            brands.add(item["brand"])
    return sorted(list(brands))

def get_unique_product_types(product_list: List[Dict[str, str]]) -> List[str]:
    """
    Get a list of unique product types from a product list.
    
    Args:
        product_list: List of product dictionaries
        
    Returns:
        Sorted list of unique product types
    """
    types = set()
    for item in product_list:
        if "error" not in item and "name" in item:
            product_type = extract_product_type(item)
            if product_type:
                types.add(product_type)
    return sorted(list(types))

def group_products_by_category(
    product_list: List[Dict[str, str]], 
    max_per_category: int = 3, 
    brand_filter: str = None, 
    product_type_filter: str = None
) -> Dict[str, List[Dict[str, str]]]:
    """
    Group and filter products by category.
    
    Args:
        product_list: List of product dictionaries
        max_per_category: Maximum number of products per category
        brand_filter: Optional brand filter
        product_type_filter: Optional product type filter
        
    Returns:
        Dictionary of categorized and filtered products
    """
    # Apply filters first
    filtered_products = []
    for item in product_list:
        if "error" in item:
            filtered_products.append(item)
            continue
            
        # Apply brand filter if specified
        if brand_filter and item.get("brand") != brand_filter:
            continue
            
        # Apply product type filter if specified
        if product_type_filter and product_type_filter not in item.get("name", "").lower():
            continue
            
        # Add category to product
        product_with_category = item.copy()
        product_with_category["category"] = categorize_product(item)
        filtered_products.append(product_with_category)
    
    # Sort by category
    filtered_products.sort(key=itemgetter("category", "name"))
    
    # Group by category
    grouped = {}
    for key, group in groupby(filtered_products, key=itemgetter("category")):
        # Limit to max_per_category products per category
        grouped[key] = list(group)[:max_per_category]
    
    return grouped 
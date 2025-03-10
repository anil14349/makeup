"""
Reusable UI components for the application.
"""
import streamlit as st
from typing import Dict, List, Any, Optional, Callable
from app.ui.styles import LINKEDIN_PROFILE_HTML, SAMPLE_CATEGORIES

def display_sidebar_info() -> None:
    """Display about information in the sidebar."""
    st.sidebar.header("About")
    st.sidebar.write("""
    This app analyzes your skin tone from your selfie and recommends 
    makeup products that would complement your complexion.
    """)
    
    st.sidebar.subheader("How it works")
    st.sidebar.write("""
    1. Upload a clear photo of your face
    2. Our AI analyzes your skin tone
    3. Receive personalized makeup recommendations
    """)
    
    st.sidebar.write("---")
    st.sidebar.markdown(LINKEDIN_PROFILE_HTML, unsafe_allow_html=True)

def display_filter_sidebar(
    cosmetics: List[Dict[str, str]],
    get_brands_func: Callable[[List[Dict[str, str]]], List[str]],
    get_types_func: Callable[[List[Dict[str, str]]], List[str]],
    reset_func: Callable[[], None]
) -> Dict[str, Any]:
    """
    Display filter controls in the sidebar.
    
    Args:
        cosmetics: List of cosmetic products
        get_brands_func: Function to extract unique brands
        get_types_func: Function to extract unique product types
        reset_func: Function to reset filters
        
    Returns:
        Dictionary with filter parameters
    """
    st.sidebar.header("Filter Results")
    
    # Get unique values for filters
    unique_brands = get_brands_func(cosmetics)
    product_types = get_types_func(cosmetics)
    
    # Product count selector
    st.sidebar.subheader("Display Options")
    products_per_category = st.sidebar.slider(
        "Products per category", 
        min_value=1, 
        max_value=10, 
        value=st.session_state.get('products_per_category', 3),
        key="product_count_slider",
        help="Select how many products to show in each category"
    )
    st.session_state['products_per_category'] = products_per_category
    
    # Brand filter
    st.sidebar.subheader("Brand Filter")
    brands_list = ["All Brands"] + unique_brands
    brand_index = 0
    if st.session_state.get('selected_brand') != "All Brands" and st.session_state.get('selected_brand') in unique_brands:
        brand_index = brands_list.index(st.session_state.get('selected_brand'))
    
    selected_brand = st.sidebar.selectbox(
        "Select a brand",
        brands_list,
        index=brand_index,
        key="brand_selector"
    )
    st.session_state['selected_brand'] = selected_brand
    brand_filter = None if selected_brand == "All Brands" else selected_brand
    
    # Product type filter
    st.sidebar.subheader("Product Type")
    types_list = ["All Products"] + product_types
    type_index = 0
    if st.session_state.get('selected_product_type') != "All Products" and st.session_state.get('selected_product_type') in product_types:
        type_index = types_list.index(st.session_state.get('selected_product_type'))
        
    selected_product_type = st.sidebar.selectbox(
        "Select product type",
        types_list,
        index=type_index,
        key="product_type_selector"
    )
    st.session_state['selected_product_type'] = selected_product_type
    product_type_filter = None if selected_product_type == "All Products" else selected_product_type
    
    # Reset filters button
    if st.sidebar.button("Reset Filters", key="reset_button"):
        reset_func()
        st.rerun()
    
    st.sidebar.write("---")
    st.sidebar.markdown(LINKEDIN_PROFILE_HTML, unsafe_allow_html=True)
    
    return {
        "products_per_category": products_per_category,
        "brand_filter": brand_filter,
        "product_type_filter": product_type_filter
    }

def display_product_recommendations(grouped_products: Dict[str, List[Dict[str, str]]], filters: Dict[str, Any] = None) -> None:
    """
    Display the product recommendations grouped by category.
    
    Args:
        grouped_products: Dictionary of products grouped by category
        filters: Optional dictionary of applied filters to display
    """
    # Apply filters and show results
    filtered_count = sum(len(products) for products in grouped_products.values())
    
    # Display filter summary if filters were applied
    if filters:
        filter_summary = []
        if filters.get("brand_filter"):
            filter_summary.append(f"Brand: {filters['brand_filter']}")
        if filters.get("product_type_filter"):
            filter_summary.append(f"Type: {filters['product_type_filter']}")
            
        st.write("## Your Personalized Recommendations")
        
        if filter_summary:
            st.caption(f"Filtered by: {', '.join(filter_summary)}")
    else:
        st.write("## Your Personalized Recommendations")
    
    if filtered_count == 0:
        st.info("No products match your filter criteria. Try changing your filters.")
    else:
        # Display products by category
        for category, products in grouped_products.items():
            if products:  # Only show categories with products
                st.markdown(f"<div class='category-header'>{category}</div>", unsafe_allow_html=True)
                
                for product in products:
                    st.markdown(f"""
                    <div class='product-item'>
                        <div class='product-name'>{product['name']}</div>
                        <div class='product-brand'>{product['brand']}</div>
                        <div class='product-color'>{product['color']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.success("These products were selected to complement your skin tone. Happy shopping! 🛍️")

def display_welcome_screen() -> None:
    """Display the welcome screen with sample information."""
    st.info("👆 Please upload a selfie to get started")
    
    # Display sample recommendations
    st.write("### Sample Recommendations")
    st.write("Here are examples of the types of products we recommend based on skin tone:")
    
    for category in SAMPLE_CATEGORIES:
        st.write(f"- **{category}**")
    
    st.write("""
    Upload a photo to get personalized recommendations from top brands like:
    Fenty Beauty, MAC, Huda Beauty, Charlotte Tilbury, NARS, Pat McGrath, and many more!
    """) 
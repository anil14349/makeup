import streamlit as st
from PIL import Image
import io
import logging
import time
from suggest_cosmetics_ml import load_model, predict_cosmetics
from itertools import groupby
from operator import itemgetter


# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup page config
st.set_page_config(
    page_title="Makeup Recommender",
    page_icon="💄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #e83e8c;
    }
    .recommendation {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .category-header {
        background-color: #f1f3f5;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1.5rem 0 0.5rem 0;
        font-weight: bold;
        color: #e83e8c;
    }
    .product-item {
        display: flex;
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
    }
    .product-name {
        flex: 1;
        font-weight: bold;
    }
    .product-brand {
        flex: 1;
    }
    .product-color {
        flex: 1;
        color: #e83e8c;
    }
    .linkedin-link {
        margin-top: 1rem;
        text-align: center;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cache the model loading to avoid reloading on each interaction
@st.cache_resource
def get_model():
    """Load and cache the model for reuse."""
    logger.info("Loading model...")
    return load_model()

def suggest_cosmetics_with_timing(image):
    """Process image and suggest cosmetics with timing."""
    try:
        start_time = time.time()
        img = Image.open(io.BytesIO(image.read())).convert("RGB")
        
        model = get_model()  # Get cached model
        predictions = predict_cosmetics(model, img)
        
        processing_time = time.time() - start_time
        logger.info("Prediction completed in %.2f seconds", processing_time)
        
        return predictions, processing_time
    except Exception as e:
        logger.error("Error in cosmetic suggestion: {str(e)}")
        return [{"error": f"Processing failed: {str(e)}"}], 0

def group_products_by_category(product_list, max_per_category=3, brand_filter=None, product_type_filter=None):
    """
    Group products by their main category with filtering options.
    
    Args:
        product_list: List of product dictionaries
        max_per_category: Maximum number of products to show per category
        brand_filter: Brand to filter by (or None for all brands)
        product_type_filter: Product type to filter by (or None for all types)
    
    Returns:
        Dictionary of categorized and filtered products
    """
    # Extract category from product name (e.g., "Foundation" from "Foundation")
    def get_category(product):
        name = product["name"]
        # Handle special cases like "Eyeshadow Palette" -> "Eye Products"
        if "eyeshadow" in name.lower() or "eyeliner" in name.lower() or "mascara" in name.lower() or "eyebrow" in name.lower():
            return "Eye Products"
        elif "lipstick" in name.lower() or "lip gloss" in name.lower() or "lip liner" in name.lower():
            return "Lip Products"
        elif "blush" in name.lower() or "bronzer" in name.lower() or "highlighter" in name.lower():
            return "Cheek Products"
        elif "foundation" in name.lower() or "concealer" in name.lower() or "powder" in name.lower():
            return "Face Products"
        else:
            return "Other Products"
    
    # Apply filters first
    filtered_products = []
    for item in product_list:
        if "error" not in item:
            # Apply brand filter if specified
            if brand_filter and item["brand"] != brand_filter:
                continue
                
            # Apply product type filter if specified
            if product_type_filter and product_type_filter not in item["name"].lower():
                continue
                
            product_with_category = item.copy()
            product_with_category["category"] = get_category(item)
            filtered_products.append(product_with_category)
        else:
            filtered_products.append(item)
    
    # Sort by category
    filtered_products.sort(key=itemgetter("category", "name"))
    
    # Group by category
    grouped = {}
    for key, group in groupby(filtered_products, key=itemgetter("category")):
        # Limit to max_per_category products per category
        grouped[key] = list(group)[:max_per_category]
    
    return grouped

def get_unique_brands(product_list):
    """Extract unique brands from products."""
    brands = set()
    for item in product_list:
        if "error" not in item and "brand" in item:
            brands.add(item["brand"])
    return sorted(list(brands))

def get_product_types(product_list):
    """Extract unique product types from products."""
    types = set()
    for item in product_list:
        if "error" not in item and "name" in item:
            # Extract the product type (e.g., "Foundation" from "Foundation")
            product_type = item["name"].split()[0].lower()
            types.add(product_type)
    return sorted(list(types))

# Initialize session state for filters if they don't exist
if 'reset_filters' not in st.session_state:
    st.session_state.reset_filters = False
if 'selected_brand' not in st.session_state:
    st.session_state.selected_brand = "All Brands"
if 'selected_product_type' not in st.session_state:
    st.session_state.selected_product_type = "All Products"
if 'products_per_category' not in st.session_state:
    st.session_state.products_per_category = 3

# Function to reset all filters
def reset_all_filters():
    st.session_state.reset_filters = True
    st.session_state.selected_brand = "All Brands"
    st.session_state.selected_product_type = "All Products"
    st.session_state.products_per_category = 3

# App UI
st.title("✨ Makeup Recommender")
st.write("Upload a selfie and get personalized makeup recommendations based on your skin tone.")

# Main content
uploaded_file = st.file_uploader("Upload a face photo:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(uploaded_file, caption="Your Photo", use_container_width=True)
    
    with col2:
        with st.spinner("Analyzing your skin tone..."):
            cosmetics, proc_time = suggest_cosmetics_with_timing(uploaded_file)
        
        if proc_time > 0:
            st.caption(f"Analysis completed in {proc_time:.2f} seconds")
    
    has_error = False
    for product in cosmetics:
        if "error" in product:
            st.error(f"😕 {product['error']}")
            has_error = True
            break
    
    if not has_error:
        # Sidebar with filtering options
        with st.sidebar:
            st.header("Filter Results")
            
            # Get unique values for filters
            unique_brands = get_unique_brands(cosmetics)
            product_types = get_product_types(cosmetics)
            
            # Product count selector
            st.subheader("Display Options")
            products_per_category = st.slider(
                "Products per category", 
                min_value=1, 
                max_value=10, 
                value=st.session_state.products_per_category,
                key="product_count_slider",
                help="Select how many products to show in each category"
            )
            st.session_state.products_per_category = products_per_category
            
            # Brand filter
            st.subheader("Brand Filter")
            brands_list = ["All Brands"] + unique_brands
            brand_index = 0
            if st.session_state.selected_brand != "All Brands" and st.session_state.selected_brand in unique_brands:
                brand_index = brands_list.index(st.session_state.selected_brand)
            
            selected_brand = st.selectbox(
                "Select a brand",
                brands_list,
                index=brand_index,
                key="brand_selector"
            )
            st.session_state.selected_brand = selected_brand
            brand_filter = None if selected_brand == "All Brands" else selected_brand
            
            # Product type filter
            st.subheader("Product Type")
            types_list = ["All Products"] + product_types
            type_index = 0
            if st.session_state.selected_product_type != "All Products" and st.session_state.selected_product_type in product_types:
                type_index = types_list.index(st.session_state.selected_product_type)
                
            selected_product_type = st.selectbox(
                "Select product type",
                types_list,
                index=type_index,
                key="product_type_selector"
            )
            st.session_state.selected_product_type = selected_product_type
            product_type_filter = None if selected_product_type == "All Products" else selected_product_type
            
            # Reset filters button
            if st.button("Reset Filters", key="reset_button"):
                reset_all_filters()
                st.rerun()
            
            st.write("---")
            
            # Add LinkedIn profile link
            st.markdown("""
            <div class="linkedin-link">
                <a href="http://linkedin.com/in/etagowni/" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>
                    </svg>
                    Connect with AnilKumar Etagowni
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        # Group and filter products
        grouped_products = group_products_by_category(
            cosmetics, 
            max_per_category=products_per_category,
            brand_filter=brand_filter,
            product_type_filter=selected_product_type if selected_product_type != "All Products" else None
        )
        
        # Apply filters and show results
        filtered_count = sum(len(products) for products in grouped_products.values())
        
        # Display filter summary
        filter_summary = []
        if brand_filter:
            filter_summary.append(f"Brand: {brand_filter}")
        if product_type_filter:
            filter_summary.append(f"Type: {product_type_filter}")
            
        st.write("## Your Personalized Recommendations")
        
        if filter_summary:
            st.caption(f"Filtered by: {', '.join(filter_summary)}")
        
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
else:
    # Sidebar with info for initial view
    with st.sidebar:
        st.header("About")
        st.write("""
        This app analyzes your skin tone from your selfie and recommends 
        makeup products that would complement your complexion.
        """)
        st.subheader("How it works")
        st.write("""
        1. Upload a clear photo of your face
        2. Our AI analyzes your skin tone
        3. Receive personalized makeup recommendations
        """)
        st.write("---")
        
        # Add LinkedIn profile link
        st.markdown("""
        <div class="linkedin-link">
            <a href="http://linkedin.com/in/etagowni/" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>
                </svg>
                Connect with AnilKumar Etagowni
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("👆 Please upload a selfie to get started")
    
    # Display sample recommendations
    st.write("### Sample Recommendations")
    st.write("Here are examples of the types of products we recommend based on skin tone:")
    
    sample_categories = [
        "Face Products: Foundation, Concealer, Powder",
        "Cheek Products: Blush, Bronzer, Highlighter",
        "Lip Products: Lipstick, Lip Gloss, Lip Liner",
        "Eye Products: Eyeshadow, Eyeliner, Mascara, Eyebrow Products"
    ]
    
    for category in sample_categories:
        st.write(f"- **{category}**")
    
    st.write("""
    Upload a photo to get personalized recommendations from top brands like:
    Fenty Beauty, MAC, Huda Beauty, Charlotte Tilbury, NARS, Pat McGrath, and many more!
    """)

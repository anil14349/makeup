"""
Makeup Recommender - Main Application Entry Point.
"""
import io
import streamlit as st
from PIL import Image
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize models first to avoid timeouts
from app.models.init_models import initialize_models

# Import application modules
from app.models.cosmetics_model import analyze_image_with_timing
from app.utils.product_utils import (
    get_unique_brands, 
    get_unique_product_types,
    group_products_by_category
)
from app.ui.styles import MAIN_STYLES, APP_CONFIG
from app.ui.components import (
    display_sidebar_info,
    display_filter_sidebar,
    display_product_recommendations,
    display_welcome_screen
)

# Initialize session state for filters
def init_session_state():
    """Initialize session state variables if they don't exist."""
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
    """Reset all filter selections."""
    st.session_state.reset_filters = True
    st.session_state.selected_brand = "All Brands"
    st.session_state.selected_product_type = "All Products"
    st.session_state.products_per_category = 3

def main():
    """Main application function."""
    # Setup the application
    st.set_page_config(
        page_title=APP_CONFIG["title"],
        page_icon=APP_CONFIG["icon"],
        layout=APP_CONFIG["layout"],
        initial_sidebar_state=APP_CONFIG["sidebar_state"]
    )
    
    # Initialize DeepFace models
    models_ready = initialize_models()
    
    # Apply custom styles
    st.markdown(MAIN_STYLES, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # App header
    st.title(APP_CONFIG["title"])
    st.write("Upload a selfie and get personalized makeup recommendations based on your skin tone.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a face photo:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            # Process the image safely
            img_bytes = uploaded_file.getvalue()
            if not img_bytes:
                st.error("The uploaded file appears to be empty. Please try uploading a different image.")
                return
                
            # Read image for display
            try:
                # First, try to display the image directly
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.image(img_bytes, caption="Your Photo", width=None)
                
                with col2:
                    with st.spinner("Analyzing your skin tone..."):
                        # Open and convert the image for processing
                        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                        
                        # Analyze the image
                        cosmetics, proc_time = analyze_image_with_timing(img)
                    
                    if proc_time > 0:
                        st.caption(f"Analysis completed in {proc_time:.2f} seconds")
            
                # Check for errors in analysis
                has_error = False
                for product in cosmetics:
                    if "error" in product:
                        st.error(f"😕 {product['error']}")
                        has_error = True
                        break
                
                if not has_error:
                    # Display sidebar with filters
                    filters = display_filter_sidebar(
                        cosmetics,
                        get_unique_brands,
                        get_unique_product_types,
                        reset_all_filters
                    )
                    
                    # Group and filter products
                    grouped_products = group_products_by_category(
                        cosmetics, 
                        max_per_category=filters["products_per_category"],
                        brand_filter=filters["brand_filter"],
                        product_type_filter=filters["product_type_filter"]
                    )
                    
                    # Display product recommendations
                    display_product_recommendations(grouped_products, filters)
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Please try uploading a different image.")
                logger.error(f"Image processing error: {str(e)}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            logger.error(f"Unexpected error: {str(e)}")
    else:
        # Display the welcome screen and sidebar info
        display_sidebar_info()
        display_welcome_screen()

if __name__ == "__main__":
    main() 
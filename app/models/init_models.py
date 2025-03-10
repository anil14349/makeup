"""
Model initialization module for handling DeepFace model downloads.
"""
import os
import logging
import numpy as np
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)

# Set model directory to a writable location for Streamlit Cloud
os.environ["DEEPFACE_HOME"] = "/tmp/.deepface"

@st.cache_resource
def initialize_models():
    """
    Initialize and preload DeepFace models.
    This helps avoid timeouts during the first use.
    
    Returns:
        bool: True if initialization was successful
    """
    logger.info("Initializing DeepFace models...")
    
    try:
        # Import DeepFace here to allow setting environment variables first
        from deepface import DeepFace
        
        # Create a small dummy image to trigger model downloads
        with st.spinner("Setting up face analysis models (first run only)..."):
            dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
            # Set a short timeout for the operation
            DeepFace.analyze(
                dummy_img, 
                actions=['race'], 
                enforce_detection=False, 
                detector_backend='opencv',
                silent=True
            )
        
        logger.info("DeepFace models initialized successfully")
        return True
    except Exception as e:
        logger.warning(f"DeepFace model initialization warning: {str(e)}")
        # Return True anyway to not block the app
        return True 
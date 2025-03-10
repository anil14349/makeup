"""
Cosmetics prediction model handling.
This module manages loading and using the DeepFace model for skin tone analysis.
"""
import os
import time
import logging
import numpy as np
import random
from PIL import Image
from typing import Optional, Any, Dict, Tuple, List, Union

# Configure logging
logger = logging.getLogger(__name__)

# Type aliases for better code readability
CosmeticProduct = Dict[str, str]
CosmeticRecommendation = List[CosmeticProduct]
AnalysisResult = Union[CosmeticRecommendation, List[Dict[str, str]]]

# Set model directory to a writable location for Streamlit Cloud
os.environ["DEEPFACE_HOME"] = "/tmp/.deepface"

# Check if we're running on Streamlit Cloud
STREAMLIT_CLOUD = os.environ.get("IS_STREAMLIT_CLOUD", False)
if STREAMLIT_CLOUD:
    # Use mock implementation for Streamlit Cloud
    logger.info("Running on Streamlit Cloud, using mock implementation")
    DEEPFACE_AVAILABLE = False
else:
    # Try to import DeepFace for local development
    try:
        from deepface import DeepFace
        DEEPFACE_AVAILABLE = True
    except ImportError:
        logger.warning("DeepFace not available. Using mock implementation.")
        DEEPFACE_AVAILABLE = False

def load_model() -> Optional[Any]:
    """
    Load the skin tone analysis model.
    
    Returns:
        Optional[Any]: Model instance or None if no specific model is required
    """
    logger.info("Loading model...")
    return None  # DeepFace doesn't require pre-loading a model

def convert_pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """
    Convert a PIL Image to an OpenCV-compatible image format.
    
    Args:
        pil_image: PIL Image to convert
        
    Returns:
        OpenCV-compatible numpy array
    """
    # Convert PIL image to numpy array (RGB)
    rgb_image = np.array(pil_image)
    
    # Convert RGB to BGR (OpenCV format)
    if rgb_image.ndim == 3 and rgb_image.shape[2] == 3:  # Check if it's a color image
        bgr_image = rgb_image[:, :, ::-1].copy()  # Reverse the channels (RGB to BGR)
        return bgr_image
    
    # For grayscale images or other formats, return as is
    return rgb_image

def map_skin_tone(dominant_race: str) -> str:
    """
    Maps the DeepFace race category to our simplified skin tone categories.
    
    Args:
        dominant_race (str): Race category from DeepFace analysis
        
    Returns:
        str: Mapped skin tone category ('fair', 'medium', or 'dark')
    """
    # Mapping of race categories to skin tones
    RACE_TO_SKIN_TONE = {
        "white": "fair",
        "asian": "fair",
        "middle eastern": "medium",
        "latino hispanic": "medium",
        "indian": "medium",
        "black": "dark",
    }
    return RACE_TO_SKIN_TONE.get(dominant_race.lower(), "medium")

def mock_predict_cosmetics() -> CosmeticRecommendation:
    """
    Generate mock cosmetics recommendations for when DeepFace is unavailable.
    
    Returns:
        List of recommended cosmetic products
    """
    from app.data.cosmetics_db import COSMETIC_DATABASE
    
    # Choose a random skin tone for mock predictions
    skin_tones = ["fair", "medium", "dark"]
    selected_tone = random.choice(skin_tones)
    
    logger.info(f"Using mock predictions with skin tone: {selected_tone}")
    
    return COSMETIC_DATABASE[selected_tone]

def predict_cosmetics(model: Optional[Any], image: Image.Image) -> AnalysisResult:
    """
    Analyze skin tone and suggest cosmetics.
    
    Args:
        model: Unused in this implementation
        image: PIL Image containing a face
        
    Returns:
        List of recommended cosmetic products or error message
    """
    from app.data.cosmetics_db import COSMETIC_DATABASE
    
    # Use mock implementation if DeepFace is not available
    if not DEEPFACE_AVAILABLE:
        logger.info("DeepFace not available, using mock predictions")
        return mock_predict_cosmetics()
    
    try:
        # Convert PIL Image to OpenCV format
        image_cv = convert_pil_to_cv2(image)
        
        # Make sure image is not too large to avoid memory issues
        max_size = 800
        h, w = image_cv.shape[:2]
        if h > max_size or w > max_size:
            scale = max_size / max(h, w)
            new_size = (int(w * scale), int(h * scale))
            # Import OpenCV only when needed
            import cv2
            image_cv = cv2.resize(image_cv, new_size)  # type: ignore
            logger.info(f"Resized image from {w}x{h} to {new_size[0]}x{new_size[1]}")
        
        # Analyze face attributes with more robust error handling
        try:
            # First try with normal detection
            result = DeepFace.analyze(
                image_cv, 
                actions=['race'], 
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
        except Exception as inner_e:
            logger.warning(f"First analysis attempt failed: {str(inner_e)}")
            # Fall back to a different detector backend
            try:
                result = DeepFace.analyze(
                    image_cv, 
                    actions=['race'], 
                    enforce_detection=False,
                    detector_backend='ssd',
                    silent=True
                )
            except Exception as e2:
                logger.error(f"Second analysis attempt failed: {str(e2)}")
                # If still failing, use a default medium skin tone
                logger.info("Using default skin tone 'medium' as fallback")
                return COSMETIC_DATABASE["medium"]
        
        dominant_race = result[0]['dominant_race']
        skin_tone = map_skin_tone(dominant_race)
        
        # Free up memory
        import gc
        gc.collect()
        
        return COSMETIC_DATABASE[skin_tone]

    except Exception as e:
        logger.error(f"Face analysis failed: {str(e)}")
        # In case of error, return medium tone recommendations as fallback
        logger.info("Using default skin tone 'medium' as fallback due to error")
        return COSMETIC_DATABASE.get("medium", [{"error": f"Face analysis failed: {str(e)}"}])

def analyze_image_with_timing(image: Image.Image) -> Tuple[AnalysisResult, float]:
    """
    Process image and suggest cosmetics with timing.
    
    Args:
        image: PIL Image to analyze
        
    Returns:
        Tuple of (cosmetic recommendations, processing time in seconds)
    """
    try:
        start_time = time.time()
        
        # Call predict_cosmetics directly with None as model
        # since load_model() returns None anyway
        predictions = predict_cosmetics(None, image)
        
        processing_time = time.time() - start_time
        logger.info("Prediction completed in %.2f seconds", processing_time)
        
        return predictions, processing_time
    except Exception as e:
        logger.error("Error in cosmetic suggestion: %s", str(e))
        # In case of error, return medium tone recommendations as fallback
        from app.data.cosmetics_db import COSMETIC_DATABASE
        return COSMETIC_DATABASE.get("medium", [{"error": f"Processing failed: {str(e)}"}]), 0 
"""
Legacy module for makeup recommendations.

This file is maintained for backward compatibility with older code.
New code should import directly from the app packages.
"""

# Import functionality from the modular app structure
from app.models.cosmetics_model import load_model, predict_cosmetics

# Re-export the functions for backward compatibility
__all__ = ['load_model', 'predict_cosmetics'] 
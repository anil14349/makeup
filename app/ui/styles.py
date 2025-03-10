"""
Stylesheet definitions and UI constants for the application.
"""

# Main stylesheet for the application
MAIN_STYLES = """
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
    .app-header {
        margin-bottom: 2rem;
    }
    .app-footer {
        margin-top: 3rem;
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
    }
</style>
"""

# LinkedIn profile HTML
LINKEDIN_PROFILE_HTML = """
<div class="linkedin-link">
    <a href="http://linkedin.com/in/etagowni/" target="_blank">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>
        </svg>
        AnilKumar Etagowni
    </a>
</div>
"""

# Sample categories to display on the home page
SAMPLE_CATEGORIES = [
    "Face Products: Foundation, Concealer, Powder",
    "Cheek Products: Blush, Bronzer, Highlighter",
    "Lip Products: Lipstick, Lip Gloss, Lip Liner",
    "Eye Products: Eyeshadow, Eyeliner, Mascara, Eyebrow Products"
]

# App configuration
APP_CONFIG = {
    "title": "✨ Makeup Recommender",
    "icon": "💄",
    "layout": "centered",
    "sidebar_state": "expanded"
} 
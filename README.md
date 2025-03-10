# Makeup Recommender

A Streamlit application that uses AI to analyze skin tone from user-uploaded selfies and recommend suitable makeup products.

## Features

- Facial analysis using DeepFace
- Skin tone detection and classification
- Personalized cosmetic recommendations
- User-friendly web interface
- Advanced filtering by brand and product type

## Project Structure

The application follows a modular architecture for better maintainability and extensibility:

```
makeup/
├── app/                  # Main application package
│   ├── data/             # Data models and product database
│   ├── models/           # AI models and prediction logic
│   ├── ui/               # UI components and styling
│   └── utils/            # Utility functions
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
└── README.md             # This file
```

### Module Details

- **app/data/**: Contains the product database and functions for retrieving product information
- **app/models/**: Contains the DeepFace integration and skin tone analysis logic
- **app/ui/**: Contains UI components, styles, and layout definitions
- **app/utils/**: Contains utility functions for filtering and organizing products

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/makeup-recommender.git
   cd makeup-recommender
   ```

2. Create a virtual environment:

   ```
   python -m venv env
   ```

3. Activate the virtual environment:

   - On Windows:
     ```
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source env/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:

   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload a clear selfie image to receive personalized makeup recommendations

4. Use the filters in the sidebar to narrow down recommendations by brand, product type, or limit the number of products shown

## How It Works

1. The app uses DeepFace to analyze facial attributes, particularly skin tone
2. Based on the detected skin tone, it categorizes the user into fair, medium, or dark skin
3. The app then suggests appropriate makeup products from a predefined database
4. Users can filter recommendations by brand, product type, or the number of products shown per category

## Extending the Application

The modular structure makes it easy to extend the application:

- To add more products, edit the `COSMETIC_DATABASE` in `app/data/cosmetics_db.py`
- To change UI components, modify files in the `app/ui/` directory
- To improve the skin tone detection, update the `app/models/cosmetics_model.py` file

## Requirements

- Python 3.8+
- Internet connection (for first-time use - downloads DeepFace models)

## Development

For development:

```
# Install development dependencies
pip install -r requirements.txt

# Format code
black .
isort .

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Connect

Connect with the developer [AnilKumar Etagowni on LinkedIn](http://linkedin.com/in/etagowni/).

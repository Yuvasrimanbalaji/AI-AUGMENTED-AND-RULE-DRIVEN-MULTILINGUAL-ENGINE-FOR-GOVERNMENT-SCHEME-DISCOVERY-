# Scheme Finder - AI-Augmented Government Scheme Discovery Engine

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-purple.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent, multilingual web application that helps Indian citizens discover relevant government schemes using a hybrid rule-based and AI-powered search engine.

![Project Banner](https://img.shields.io/badge/Scheme-Finder-0b5e14?style=for-the-badge)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

### Core Functionality
- **Smart Scheme Search**: Filter government schemes by age, gender, occupation, income, caste, and region (state)
- **Keyword Search**: Fast text-based search with relevance scoring
- **AI-Powered Chatbot**: Multilingual conversational assistant powered by Google Gemini AI
- **Multilingual Support**: Supports 11 Indian languages (Hindi, Tamil, Telugu, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Kannada, Odia, and English)
- **Scheme Details**: Comprehensive information including description, benefits, eligibility, application steps, and required documents

### Advanced Features
- **Hybrid Search Engine**: Combines rule-based filtering with AI-augmented retrieval
- **Relevance Scoring**: Schemes ranked by match confidence (tags: 10pts, name: 5pts, description: 1pt)
- **Google Translate Integration**: Real-time language translation for accessibility
- **Responsive Design**: Mobile-friendly interface
- **Dark Theme**: Eye-friendly color scheme

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.9+, Flask |
| **AI/ML** | Google Generative AI (Gemini Flash) |
| **Data Processing** | Pandas |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Translation** | Google Translate Widget |
| **Database** | CSV (Indian Government Schemes Dataset) |
| **Version Control** | Git, GitHub |

---

## Project Structure

```
scheme-finder/
├── app.py                      # Flask application (main backend)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── templates/
│   ├── home.html              # Landing page
│   ├── index.html             # Search and filter page
│   └── scheme.html            # Scheme detail page
├── static/
│   ├── translate.png          # Translation icon
│   └── schemesfinder.jpg      # Project banner image
└── indianschemes.csv          # Government schemes dataset
```

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yuvasrimanbalaji/AI-AUGMENTED-AND-RULE-DRIVEN-MULTILINGUAL-ENGINE-FOR-GOVERNMENT-SCHEME-DISCOVERY-.git
   cd AI-AUGMENTED-AND-RULE-DRIVEN-MULTILINGUAL-ENGINE-FOR-GOVERNMENT-SCHEME-DISCOVERY-
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Google API Key**
   - Get a free API key from [Google AI Studio](https://aistudio.google.com)
   - Open `app.py` and replace the placeholder key with your actual API key

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

---

## Configuration

### API Key Setup
Edit `app.py` and set your Google Gemini API key:

```python
API_KEY = 'YOUR_ACTUAL_API_KEY_HERE'
```

### CSV Dataset
Place your government schemes CSV file (`indianschemes.csv`) in the project root directory. The CSV should contain the following columns (auto-detected):
- Scheme Name
- Age Group
- Gender
- Occupation Category
- Income Level
- Region/State
- Caste Category
- Description
- Benefits
- Eligibility
- Application Steps
- Documents Required
- Tags/Keywords

---

## Usage

### Search by Filters
1. Navigate to the Search page
2. Select your criteria from dropdown menus (Age, Gender, Occupation, Income, Region, Caste)
3. Click "Find Schemes by Filter"

### Keyword Search
1. Enter keywords related to your needs (e.g., "farmer", "student scholarship")
2. Click "Search by Keyword"
3. Results are ranked by relevance

### AI Chatbot
1. Click the chat icon in the bottom-right corner
2. Ask questions in any supported language
3. Get AI-powered responses about relevant schemes

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home/Landing page |
| `/search` | GET/POST | Search and filter schemes |
| `/scheme/<id>` | GET | View scheme details |
| `/chat` | POST | AI chatbot interaction (JSON) |

### Chat API Request Format
```json
{
  "message": "What schemes are available for farmers?"
}
```

### Chat API Response Format
```json
{
  "response": "Here are some government schemes for farmers..."
}
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

**Project Lead**: Yuvasri Manbalaji

- **Email**: rakeshreddy@gmail.com
- **Phone**: +91 8125413287
- **Location**: Chennai, Tamil Nadu, India
- **Institution**: Veltech, Avadi

---

## Acknowledgments

- **Data Source**: Indian Government Schemes Dataset (Open Data)
- **AI Model**: Google Gemini Flash API
- **Translation**: Google Translate Widget
- **Inspired by**: Digital India Initiative

---

<div align="center">

**Made with ❤️ for India**

[Back to Top](#scheme-finder---ai-augmented-government-scheme-discovery-engine)

</div>

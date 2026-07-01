# VenturePilot

> An intelligent, multi-model AI validation engine designed to systematically analyze, score, and evaluate startup ideas and pitch decks using machine learning and LLM integrations.

---

## Architecture Overview

VenturePilot operates on a decoupled architecture, integrating a high-performance Python backend with an interactive Streamlit frontend. The system leverages custom Scikit-Learn and TensorFlow models trained on synthetic startup datasets, alongside Google's Gemini API for deep semantic analysis.

### Tech Stack
- **Frontend Engine:** Streamlit, Plotly (for interactive data visualization)
- **Backend API:** Flask, RESTful endpoints
- **Machine Learning Core:** TensorFlow, Scikit-Learn, Pandas, NumPy
- **Generative AI:** Google Generative AI (Gemini Pro)
- **Database:** MongoDB (NoSQL)
- **Document Processing:** PDF2Image, ReportLab, OpenCV

---

## Key Capabilities

* **Startup Validation Engine:** Processes raw startup concepts through an ML pipeline (Random Forest & Neural Networks) to calculate a weighted "Success Score", Investor Readiness, and Risk level.
* **Pitch Deck Analyzer:** Extracts text and structural data from uploaded PDF pitch decks, passing the content through Gemini Pro for comprehensive critique and actionable feedback.
* **AI Chat Assistant:** A context-aware chatbot integrated directly into the validation interface, allowing founders to dynamically query the AI regarding their specific business model.
* **Automated PDF Reporting:** Dynamically generates downloadable, professional-grade PDF reports summarizing the ML analysis and AI recommendations.
* **Enterprise Dashboard:** A centralized, metric-driven dashboard tracking historical analysis data, aggregated success metrics, and industry trends.

---

## Local Development & Setup

### 1. Prerequisites
Ensure you have Python 3.9+ and `pip` installed on your local machine. You will also need a MongoDB cluster (local or Atlas) and a Google Gemini API Key.

### 2. Environment Configuration
Clone the repository and set up your local environment variables.

```bash
git clone https://github.com/Yashwanth070/VenturePilot.git
cd VenturePilot
```

Create a `.env` file in the root directory based on the provided `.env.example`:
```env
GOOGLE_API_KEY=your_gemini_api_key
MONGO_URI=your_mongodb_connection_string
FLASK_SECRET_KEY=your_secure_secret_key
```

### 3. Installation
It is highly recommended to isolate dependencies using a virtual environment.

```bash
# Create and activate virtual environment (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# Install core dependencies
pip install -r requirements.txt
```

### 4. Running the Application

VenturePilot requires both the backend API and the frontend client to be running concurrently.

**Start the Backend (Terminal 1):**
```bash
python backend/app.py
```
*The Flask API will initialize on `http://localhost:5000`.*

**Start the Frontend (Terminal 2):**
```bash
# Ensure your venv is activated
streamlit run frontend/app.py
```
*The Streamlit interface will initialize on `http://localhost:8501`.*

---

## Project Structure

```text
VenturePilot/
├── backend/
│   ├── app.py                     # Flask entry point
│   ├── routes/                    # API route definitions
│   ├── services/                  # Business logic (Gemini, ML orchestration)
│   ├── ml/                        # Model training scripts and pipelines
│   └── database/                  # MongoDB connection clients
├── frontend/
│   ├── app.py                     # Streamlit entry point (Auth/Routing)
│   ├── components/                # Reusable UI layouts and elements
│   ├── pages/                     # Application modules (Dashboard, Engine, Analyzer)
│   └── assets/                    # Static CSS and design systems
├── models/                        # Serialized .pkl and .keras model weights
├── data/                          # Synthetic dataset generators
└── requirements.txt               # Dependency lockfile
```

---

## Legal & Compliance

This software is provided "as is", without warranty of any kind. VenturePilot relies on third-party LLMs (Google Gemini) for subjective analysis; outputs should be independently verified before making financial or business decisions.

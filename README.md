# 🏛️ SchemeWise – Government Scheme Eligibility Checker

SchemeWise is a web-based application that helps users explore government welfare schemes and check their potential eligibility based on personal details such as age, income, category, and occupation. It also includes an ML-based chatbot to assist users with scheme-related questions.

## 🚀 Features

- 🔍 **Eligibility Checker**  
  Enter age, income, category, and occupation to find schemes matching the available eligibility criteria.

- 📋 **Detailed Scheme Information**  
  Explore scheme benefits, eligibility conditions, and other available details.

- 🔗 **Direct Apply Links**  
  Access official scheme portals through application links where available.

- ❤️ **Wishlist**  
  Save schemes for future reference.

- ✅ **Applied Tracker**  
  Keep track of schemes you have marked as applied for.

- 🕓 **Recent Activity**  
  View recently opened schemes.

- 💬 **ML-Based Chatbot Assistant**  
  Ask questions about government schemes, benefits, required documents, and application procedures.

- 🔐 **Login and Registration**  
  Frontend login and registration using browser `localStorage`. This is a demonstration feature and does not provide secure backend authentication.

- 🔌 **Flask REST API**  
  Provides endpoints for scheme eligibility checking and chatbot responses.

## 🛠️ Tech Stack

| Component | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Machine Learning | Trained chatbot model, Joblib |
| Data Processing | Pandas / CSV data, where implemented |
| Browser Storage | LocalStorage |
| API Communication | JSON, HTTP POST |

## 📂 Project Structure

```text
SchemeWise/
├── app.py
├── index.html
├── chatbot_model.py
├── chatbot_model.pkl
├── updated_data.csv
├── requirements.txt
└── README.md
```

*The files shown above should match the files you actually commit to the repository.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sathvikajeeviguntla-2427/SchemeWise.git
cd SchemeWise
```

### 2. Create and activate a virtual environment (recommended)

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by the application:

```bash
pip install flask joblib scikit-learn
```

### 4. Start the Flask backend

```bash
python app.py
```

The API should be available at:

```text
http://127.0.0.1:5000/
```

### 5. Open the frontend

Open `index.html` in your browser and use the eligibility checker and chatbot.

Ensure the frontend sends requests to the correct Flask API address.

## 🔌 API Endpoints

### `GET /`

Checks whether the Flask API is running and reports whether the chatbot model loaded successfully.

### `POST /check`

Checks scheme eligibility using the submitted age, income, category, and occupation.

Example request:

```json
{
  "age": 22,
  "income": 120000,
  "category": "General",
  "occupation": "student"
}
```

The endpoint returns a JSON list of schemes matching the criteria configured in the backend.

### `POST /chat`

Processes a chatbot message using the loaded ML model.

Example request:

```json
{
  "message": "Hello"
}
```

The response can include the chatbot reply, predicted intent, and confidence score when available.

## 🧪 How It Works

1. The user enters age, income, category, and occupation.
2. The Flask eligibility endpoint validates the input.
3. The backend compares the user's details against the configured scheme criteria.
4. Matching schemes are returned to the frontend.
5. The chatbot predicts an intent from the user's message and selects an appropriate predefined response.

## 🔒 Limitations and Notes

- Eligibility results depend on the scheme data and rules currently configured in the application.
- The backend currently uses sample scheme records; the CSV file must be integrated into the eligibility logic if it is intended to be the primary data source.
- Chatbot responses depend on the training data, model predictions, and configured intent responses.
- Login and registration use browser `localStorage` and should not be considered production-grade authentication.
- The Flask development server is intended for local development, not public production deployment.
- Verify scheme details and eligibility requirements on official government portals before applying.

## 🔮 Future Enhancements

- Integrate a larger, verified government scheme dataset.
- Add multilingual chatbot support.
- Improve intent classification with additional training examples and evaluation.
- Implement secure user authentication and persistent storage.
- Deploy the frontend and backend for public access.
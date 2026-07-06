# 🏦 Loan Approval RAG Chatbot

A conversational AI assistant that helps users check their loan eligibility and answers general loan-related questions — combining a trained Machine Learning model with Retrieval-Augmented Generation (RAG).

Built as part of an AI/ML Internship project at **MFSYS Tech**, Islamabad.

---

## 📖 Overview

This project is a two-in-one financial chatbot:

1. **Loan Eligibility Predictor** — collects an applicant's details through a guided, step-by-step conversation, then uses a trained **Random Forest** model to predict loan approval/rejection, with plain-language reasons and improvement suggestions.
2. **General Loan FAQ Assistant (RAG)** — answers general questions about loan policies, required documents, CIBIL scores, and eligibility criteria by retrieving relevant context from a knowledge base and generating a natural-language response via the **Mistral API**.

The chatbot is designed with a warm, empathetic "customer care" tone rather than a robotic Q&A style.

---

## ✨ Features

- 💬 **Conversational slot-filling flow** — asks one question at a time to collect applicant details (dependents, income, CIBIL score, assets, etc.)
- 🤖 **ML-based prediction** — Random Forest classifier trained on real loan approval data, with a Logistic Regression baseline for comparison
- 📊 **Explainable results** — approval/rejection reasons are generated based on the applicant's actual data and the model's decision (not generic text)
- 💡 **Actionable suggestions** — if an application is likely to be rejected, the bot suggests concrete steps to improve eligibility
- 📚 **RAG-based FAQ answering** — general questions are answered using a small knowledge base (FAISS + Sentence Embeddings) combined with the Mistral LLM
- 🧠 **Smart input parsing** — handles varied number formats (commas, "lakh"/"lac" multipliers, decimals) and validates ranges (e.g. CIBIL score 300–900)
- 🖥️ **Simple floating chat widget UI** — built with Flask, HTML, CSS, and vanilla JavaScript

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | Python 3.11, Flask |
| ML Model | scikit-learn (Random Forest, Logistic Regression), joblib |
| Embeddings | SentenceTransformers (`paraphrase-MiniLM-L3-v2`) |
| Vector Search | FAISS |
| LLM | Mistral API (`mistral-small-latest`) via `requests` |
| Config | python-dotenv |
| Frontend | HTML, CSS, JavaScript (vanilla) |

---

## 📁 Project Structure

```
loan_chatbot/
│
├── app.py                        # Main Flask application & chat route
├── conversation.py                # Slot-filling conversation logic
├── model_utils.py                 # Model loading, prediction, explanation logic
├── build_index.py                 # Builds the FAISS knowledge base index
├── knowledge_base.txt              # FAQ content used for RAG retrieval
├── loan_approval_rf_model.pkl      # Trained Random Forest model
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not committed)
├── faiss_index/                    # Auto-generated FAISS index + text chunks
│   ├── loan_faq.index
│   └── chunks.pkl
├── templates/
│   └── index.html                  # Chat widget HTML
└── static/
    ├── chat.css                    # Chat widget styling
    └── chat.js                     # Chat widget frontend logic
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd loan_chatbot
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 5. Add your trained model
Place your trained `loan_approval_rf_model.pkl` file in the project root (same level as `app.py`).

### 6. Build the FAISS knowledge base index
```bash
python build_index.py
```

### 7. Run the application
```bash
python app.py
```

Visit **http://127.0.0.1:5000** in your browser.

---

## 💬 Usage

**To check loan eligibility:**
> "I want to apply for a loan"

The bot will ask for details one at a time (dependents, education, income, CIBIL score, assets, etc.) and provide a prediction with explanation at the end.

**To ask a general question:**
> "What documents do I need for a loan?"
> "What is a CIBIL score?"

---

## 🧩 Model Details

The Random Forest classifier was trained on the [Loan-Approval-Prediction-Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset) (Kaggle), using the following features:

- Number of dependents
- Education level
- Employment status (self-employed or not)
- Annual income
- Requested loan amount
- Loan term
- CIBIL score
- Residential, commercial, luxury, and bank asset values

Evaluation metrics (accuracy, precision, recall, confusion matrix, and feature importance) were used to compare the Random Forest model against a Logistic Regression baseline.

---

## ⚠️ Known Limitations

- Explanation logic uses simplified rule-based heuristics (CIBIL threshold, income-to-loan ratio, asset coverage) rather than true model interpretability tools (e.g. SHAP/LIME) — it approximates *why* the model likely made its decision, but may not always perfectly match the model's internal reasoning.
- Intent detection for starting a loan application currently relies on keyword matching, which may miss some natural phrasings.
- Session data is stored in memory and will reset if the server restarts.
- This is a development-only setup (`Flask` debug server) and is not configured for production deployment.

---

## 🚀 Future Improvements

- Replace keyword-based intent detection with a proper intent classifier
- Add proper model explainability (SHAP values) instead of rule-based approximations
- Persist session/application data to a database
- Add multi-domain support (credit cards, general banking FAQ, financial literacy)
- Deploy with a production-ready WSGI server

---

## 📄 License

This project was built for educational purposes as part of an internship program.

---

## 🙏 Acknowledgements

- Dataset: [architsharma01 - Loan Approval Prediction Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset) (Kaggle)
- LLM: [Mistral AI](https://mistral.ai/)
=======
# loan-approval-rag-chatbot-v1
>>>>>>> 06400a7eb43107e27e0048c7e42fa12ceb95d069

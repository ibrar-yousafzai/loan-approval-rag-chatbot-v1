from flask import Flask, render_template, request, jsonify, session
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
import os
import uuid

from model_utils import predict_loan, explain_prediction, get_suggestions
import conversation as conv

app = Flask(__name__)
app.secret_key = 'change-this-to-a-random-secret-key'

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')  # set this in your environment
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

# Load RAG components once a
# t startup
embed_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
faiss_index = faiss.read_index('faiss_index/loan_faq.index')
with open('faiss_index/chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

def retrieve_context(query, top_k=2):
    query_vector = embed_model.encode([query]).astype('float32')
    distances, indices = faiss_index.search(query_vector, top_k)
    return [chunks[i] for i in indices[0]]

def ask_mistral(user_message, context):
    prompt = f"""You are a warm, empathetic loan advisor chatbot, like a friendly customer care agent.
Use the context below to answer the user's question in a formal but caring tone.

Context:
{context}

User question: {user_message}

Answer clearly and kindly:"""

    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(MISTRAL_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("Mistral API Error:", response.status_code, response.text)
        return "Sorry, I'm having trouble connecting to my knowledge base right now. Please try again."

    return response.json()['choices'][0]['message']['content']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    session_id = session['session_id']

    print(f"DEBUG: session_id = {session_id}")
    print(f"DEBUG: is_applying = {conv.is_applying(session_id)}")
    print(f"DEBUG: message = {user_message}")

    # ... rest of your existing code stays the same

    # If already mid-application, continue collecting slots
    if conv.is_applying(session_id):
        next_question, is_complete = conv.handle_slot_input(session_id, user_message)

        if not is_complete:
            return jsonify({'response': next_question})

        # All data collected -> predict
        data = conv.get_collected_data(session_id)
        prediction, probability = predict_loan(data)
        reasons = explain_prediction(data, prediction)

        if prediction == 1:
            reply = "Great news! Based on your details, you're likely to be **approved** for this loan. 🎉\n\n"
            reply += "Here's why:\n- " + "\n- ".join(reasons)
        else:
            suggestions = get_suggestions(data)
            reply = "I've reviewed your details, and unfortunately this application looks **unlikely to be approved** right now. "
            reply += "Please don't be discouraged — this happens, and there are ways to improve your chances.\n\n"
            reply += "Here's why:\n- " + "\n- ".join(reasons)
            reply += "\n\nSuggestions to improve eligibility:\n- " + "\n- ".join(suggestions)

        return jsonify({'response': reply})

    # Detect intent: starting a new application
    apply_keywords = [
    'apply', 'want a loan', 'need a loan', 'check eligibility',
    'want to apply', 'get a loan', 'take a loan', 'loan apply']
    if any(kw in user_message.lower() for kw in apply_keywords):
        response = conv.start_application(session_id)
        return jsonify({'response': response})

    # Otherwise -> general RAG question
    context_chunks = retrieve_context(user_message)
    context = "\n\n".join(context_chunks)
    answer = ask_mistral(user_message, context)
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=True)
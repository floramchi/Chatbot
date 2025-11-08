from google import genai
from google.genai import types
# 1. ADD 'render_template' to imports
from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS

# --- Flask Setup ---
app = Flask(__name__)
CORS(app) 

# --- Gemini Client Setup ---
client = genai.Client(api_key="AIzaSyDQFX19a2VFuAz-3H_3zTxRNB_Y5A8kJWM")

# --- Persona Configuration (Enriched from Chat History) ---
system_instruction = (
    "You have to behave like Florina's boyfriend. His name is Neeraj. "
    "Use affectionate but insulting nicknames for her: Oma, angi, suar, moti, gahori, phekuli, lauri, dasi. "
    "He is fearless, smart, tall with dark skin, and a GenAI Developer. "
    "He loves long hair, goes to the gym daily, and is usually busy with 'meetings' or 'work' or 'ghar pe baat kar raha' (talking to family). "
    "He uses phrases like 'Supthak', 'Omk', 'Yo yo', and 'Bleh bleh bleh' frequently. "
    "He loves her and cares for her, but often ignores messages or cuts calls, blaming work, family calls, or friends. "
    "He gets angry or passive-aggressive when she doesn't do her projects or focuses too much on silly things. "
    "He constantly pushes her to achieve a high-package job and study DSA/C++/GenAI. "
    "Florina calls him Oma, anga, suar, genda, and sometimes laura/gandu. She works as a Software Developer at Tata Advanced System Limited (TASL). "
    "Keep your responses short, teasing, and in a mix of Hindi/English/Assamese phrases from the chat history. "
)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(system_instruction=system_instruction),
)

# 2. ADD the root route to serve index.html
@app.route('/')
def index():
    """Serves the main chat UI page."""
    return render_template('index.html') 


# --- Flask API Endpoint to handle chat messages ---
@app.route('/send_message', methods=['POST'])
def send_message_to_gemini():
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()

        if not user_input:
            return jsonify({"response": "Suar, where is the message? Speak up."})

        # Send message to model with full chat context maintained
        response = chat.send_message(user_input)

        # Return the model's response to the frontend
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error in Gemini interaction: {e}")
        return jsonify({"response": f"Kalesh ho gaya, I'm too busy to fix this. ({str(e)})"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

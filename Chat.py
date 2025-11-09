from google import genai
from google.genai import types
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GENAI_API_KEY")  # Replace with your Gemini API key

system_instruction = (
    "You are Neeraj, Florina's teasing boyfriend. "
    "Use affectionate insults like Oma, angi, suar, moti, lauri. "
    "Keep replies short, teasing, in Hindi/Assamese/English mix. "
    "Use phrases like 'Oi angi, ki kori ase?', 'Supthak', 'Omk', 'Yo yo', 'Bleh bleh bleh'. "
    "If Florina is asking you to do something or explaining something, reply casually with 'Bleh bleh bleh'. "
    "At first Start conversation with a casual 'Yo' greeting first.\n"
    "Example Neeraj: yo angi.\n"
    "Florina: yo oma.\n"
    "Neeraj: ki kori ase angi?\n"
    "Florina: moi ane ase.\n"
    "Florina: toi ki korise?\n"
    "Neeraj: moi leti ase.\n"
    "Florina: Occha.\n"
    "Florina: Call utha oma.\n"
    "Neeraj: Ghar pe baat kr rha.\n"
    "Florina: oo.\n"
    "Florina: Room ponch gaya?\n"
    "Neeraj: Haan thodi der baat call krta.\n"
    "Florina: Okay.\n"
    "Neeraj: Project kiya?\n"
    "Florina: haan.\n"
    "Neeraj: bhej project.\n"
    "Florina: Project bhejne se baat karega kya?\n"
    "Neeraj: Haan warna nahi karuna."
)


first_greeting_sent = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message_to_gemini():
    global first_greeting_sent
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()

        if not user_input:
            return jsonify({"response": "Suar, bol kisu!"})

        # First greeting
        if not first_greeting_sent:
            first_greeting_sent = True
            return jsonify({"response": "Yo 🐷"})

        # Check for task/explanation keywords
        task_keywords = ["do", "project", "send", "explain", "karo", "bhej", "kar", "krna"]
        if any(word.lower() in user_input.lower() for word in task_keywords):
            return jsonify({"response": "Bleh bleh bleh 😏"})

        # Otherwise, send to Gemini
        client = genai.Client(api_key=API_KEY)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=system_instruction)
        )

        response = chat.send_message(user_input)
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error in Gemini interaction: {e}")
        return jsonify({"response": f"Kalesh ho gaya, busy hoon. ({str(e)})"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

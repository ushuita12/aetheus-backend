import nest_asyncio
nest_asyncio.apply()

from flask import Flask, request, jsonify
from g4f.client import Client
import g4f

app = Flask(__name__)
client = Client()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "AETHEUS AI Engine is Online!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400
            
        prompt = data.get('prompt', '')
        ui_model = data.get('model', 'ChatGPT')
        
        # Exact g4f string identifiers for latest models
        if ui_model == 'ChatGPT':
            target_model = 'gpt-4o'
        elif ui_model == 'Claude':
            target_model = 'claude-3.5-sonnet'
        else:
            target_model = 'llama-3.1-70b'
            
        response = client.chat.completions.create(
            model=target_model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
        
    except Exception as e:
        error_msg = str(e)
        print(f"🔥 SERVER CRASHED: {error_msg}")
        # Send exact error back to the mobile app
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "AETHEUS AI Engine is Online!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        ui_model = data.get('model', 'ChatGPT')
        
        # Pollinations models: 'openai' (GPT-4o), 'claude', 'llama'
        if ui_model == 'ChatGPT':
            target = 'openai'
        elif ui_model == 'Claude':
            target = 'claude'
        else:
            target = 'llama'
            
        # Direct HTTP POST call - Zero headless browsers needed
        url = "https://text.pollinations.ai/"
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": target
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return jsonify({"response": response.text})
        else:
            return jsonify({"error": f"API Blocked: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

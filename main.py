import nest_asyncio
nest_asyncio.apply()

from flask import Flask, request, jsonify
import g4f
from g4f.client import Client

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
        
        # 🚀 FORCE A STRICTLY FREE PROVIDER (Bypass g4f.dev Cake Credits)
        if ui_model == 'ChatGPT':
            target_model = 'gpt-4o'
            target_provider = g4f.Provider.Blackbox
        elif ui_model == 'Claude':
            target_model = 'claude-3.5-sonnet'
            target_provider = g4f.Provider.Blackbox
        else:
            target_model = 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo'
            target_provider = g4f.Provider.Blackbox
            
        response = client.chat.completions.create(
            model=target_model,
            provider=target_provider, # 🔥 THE MAGIC SHIELD: Blocks 402 errors!
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
        
    except Exception as e:
        error_msg = str(e)
        print(f"🔥 SERVER CRASHED: {error_msg}")
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

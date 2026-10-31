import nest_asyncio
nest_asyncio.apply()

from flask import Flask, request, jsonify
import g4f

app = Flask(__name__)

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
        
        if ui_model == 'ChatGPT':
            target_model = 'gpt-4o'
        elif ui_model == 'Claude':
            target_model = 'claude-3.5-sonnet'
        else:
            target_model = 'llama-3.1-70b'
            
        # Dynamically fetch an API-only provider that requires zero browser dependencies
        safe_provider = getattr(g4f.Provider, 'PollinationsAI', getattr(g4f.Provider, 'Blackbox', None))
            
        response = g4f.ChatCompletion.create(
            model=target_model,
            messages=[{"role": "user", "content": prompt}],
            provider=safe_provider
        )
        
        answer = response if isinstance(response, str) else "".join(response)
            
        return jsonify({"response": answer})
        
    except Exception as e:
        error_msg = str(e)
        print(f"🔥 SERVER ERROR: {error_msg}")
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

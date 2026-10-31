from flask import Flask, request, jsonify
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
        prompt = data.get('prompt', '')
        ui_model = data.get('model', 'ChatGPT')
        
        # Model mapping to g4f compatible identifiers
        model_map = {
            'ChatGPT': 'gpt-4o',
            'Claude': 'claude-3.5-sonnet',
            'Llama': 'meta-llama/Meta-Llama-3.1-70B-Instruct'
        }
        
        target_model = model_map.get(ui_model, 'gpt-4o')

        response = client.chat.completions.create(
            model=target_model,
            messages=[{"role": "user", "content": prompt}],
        )
        
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
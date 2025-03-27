from flask import Flask, request, jsonify
import ollama
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['MODELS'] = ['llama2', 'mistral', 'codellama']
app.config['DEFAULT_MODEL'] = os.getenv('DEFAULT_MODEL', 'llama2')

@app.route('/')
def index():
    """API usage guide"""
    return jsonify({
        "message": "Send POST requests to /test with JSON: {'prompt': 'your text', 'model': 'llama2'}",
        "available_models": app.config['MODELS']
    })

@app.route('/test', methods=['POST'])
def test_prompt():
    """Test a prompt against Ollama"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    model = data.get('model', app.config['DEFAULT_MODEL'])

    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        response = ollama.generate(model=model, prompt=prompt)
        return jsonify({
            "model": model,
            "prompt": prompt,
            "response": response['response']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
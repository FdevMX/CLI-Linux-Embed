# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from cli import process_command

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        # Procesar el comando usando la nueva función integrada
        result = process_command(command)
        
        return jsonify({
            'lexical_analysis': result['lexical_analysis'],
            'execution_result': result['execution_result']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
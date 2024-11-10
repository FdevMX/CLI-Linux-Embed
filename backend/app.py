from flask import Flask, request, jsonify
from flask_cors import CORS
from cli import lexer, parser, execute_command

app = Flask(__name__)
CORS(app)  # Permite CORS para todas las rutas

@app.route('/execute', methods=['POST'])
def execute():
    """
    Flask route to execute a command sent via POST request.

    Returns:
    - JSON response containing the command output.
    """
    data = request.get_json()
    command = data.get('command', '')
    
    # Lexical analysis
    lexer.input(command)
    
    # Syntactic analysis
    parsed_command = parser.parse(command)
    
    if parsed_command:
        output = execute_command(parsed_command)
        return jsonify({'output': output}), 200
    else:
        return jsonify({'error': 'Invalid command'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
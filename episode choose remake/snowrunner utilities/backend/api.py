from flask import Flask, jsonify, request
from flask_cors import CORS
import session_names_builder
import description_builder

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

@app.route("/api/get-names", methods=['GET'])
def get_names():
    names = session_names_builder.get_names()
    return jsonify({
        'names': names
    })

@app.route("/api/convert-names", methods=['POST'])
def convert_names():
    data = request.get_json()
    names = data.get('names')
    region = data.get('region')
    converted_names = description_builder.convert_names(names, region=region)

    return jsonify({
        'converted': converted_names
    })

    print(names)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
from flask import Flask, render_template, request, jsonify
import data_manager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    # reload data to be sure
    contacts = data_manager.laden()
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_contact = request.json
    contacts = data_manager.laden()
    contacts.append(new_contact)
    data_manager.speichern(contacts)
    return jsonify({"status": "success", "message": "Contact added"}), 201

@app.route('/api/contacts/<int:index>', methods=['PUT'])
def update_contact(index):
    updated_data = request.json
    contacts = data_manager.laden()
    if 0 <= index < len(contacts):
        contacts[index] = updated_data
        data_manager.speichern(contacts)
        return jsonify({"status": "success", "message": "Contact updated"})
    return jsonify({"status": "error", "message": "Index out of range"}), 404

@app.route('/api/contacts/<int:index>', methods=['DELETE'])
def delete_contact(index):
    contacts = data_manager.laden()
    if 0 <= index < len(contacts):
        contacts.pop(index)
        data_manager.speichern(contacts)
        return jsonify({"status": "success", "message": "Contact deleted"})
    return jsonify({"status": "error", "message": "Index out of range"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

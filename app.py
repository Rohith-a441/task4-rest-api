from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user data storage
users = []

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the User Management REST API!'})

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# POST - Create new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Accept both capitalized and lowercase keys
    name = data.get('name') or data.get('Name')
    email = data.get('email') or data.get('Email')

    if not name or not email:
        return jsonify({'error': 'Missing name or email'}), 400

    new_user = {
        'id': len(users) + 1,
        'name': name,
        'email': email
    }
    users.append(new_user)
    return jsonify(new_user), 201

# PUT - Update user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    for user in users:
        if user['id'] == user_id:
            user['name'] = data.get('name') or data.get('Name') or user['name']
            user['email'] = data.get('email') or data.get('Email') or user['email']
            return jsonify(user), 200

    return jsonify({'error': 'User not found'}), 404

# DELETE - Remove user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for index, user in enumerate(users):
        if user['id'] == user_id:
            deleted_user = users.pop(index)
            return jsonify({'message': 'User deleted', 'user': deleted_user}), 200
    return jsonify({'error': 'User not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

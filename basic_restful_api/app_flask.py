from flask import Flask, jsonify
from flask import request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row # Return row as dictionaries
    return conn

@app.route('/users',methods=['GET'])
def get_users(): # Get ALL users
    conn = get_db_connection()
    users = conn.execute('SELECT * from users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])


@app.route('/user/<int:user_id>',methods=['GET'])
def get_user(user_id): # Get a specific user based on condition
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

@app.route('/users',methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error':'Name and email are required'}), 400
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name,email) VALUES (?,?)',(name,email))
        conn.commit()
        conn.close()
        return jsonify({'message':'User created successfully'}),201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}),409

@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM users WHERE id = ?',(user_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error':'User not found'}),404
    return jsonify({'message':'User deleted successfully'})

# Run this to POST the data 

# curl -X POST http://127.0.0.1:5000/users \
#      -H "Content-Type: application/json" \
#      -d '{"name": "John Doe", "email": "johndoe@example.com"}'

# ------
# Day 1: Create a Flask and Web UI
# Day 2: update the app_flask.py file and add POST request, and understand the bash command line with -X -H -d
# Day 3: Add PUT and Error Handling

@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email =  data.get('email')
    if not name or not email:
        return jsonify({'error':'Name and email '}),400
    try:
        conn = get_db_connection()
        cursor = conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({'error':'User not found'}),404
        return jsonify({'message':'User updated successfully'})
    except  sqlite3.IntegrityError:
        return jsonify({'error':'Email already exists'}),409


# Add Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'Not found'}),404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error':'Internal server error'}),500


# ### Update user_id = 1 from "Alice" to "Charlie Updated"
# curl    -X PUT -H "Content-Type: application/json"\
#         -d '{"name":"Charlie Updated","email":"charlie.new@example.com"}' \
#         http://127.0.0.1:5000/users/1







if __name__ == '__main__':
    app.run(debug=True)
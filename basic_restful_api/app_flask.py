from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
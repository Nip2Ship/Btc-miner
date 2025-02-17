from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)


# Create Database
with app.app_context():
    db.create_all()


# Register User
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username taken'}), 400
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered', 'username': username})


# Simulated Mining
@app.route('/mine', methods=['POST'])
def mine():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    mined_btc = round(random.uniform(0.00001, 0.00005), 8)  # Simulated mining
    user.balance += mined_btc
    db.session.commit()

    return jsonify({
        'message': 'Mining successful',
        'mined_btc': mined_btc,
        'balance': user.balance
    })


# Check Balance
@app.route('/balance', methods=['GET'])
def balance():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'username': username, 'balance': user.balance})


# Withdraw BTC (Send Transaction)
@app.route('/withdraw', methods=['POST'])
def withdraw():
    username = request.form.get('username')
    btc_address = request.form.get('btc_address')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

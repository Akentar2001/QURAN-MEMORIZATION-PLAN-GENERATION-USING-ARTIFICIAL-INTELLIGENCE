from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db
from app.models import users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = users.query.filter_by(username=data['username']).first()

    if user:
        # Temporary fallback check for plain text passwords
        if user.password_hash == data['password']:
            print("Warning: Password stored in plain text - this is insecure!")
            # Generate proper hash and update user
            # user.password_hash = generate_password_hash(data['password'])
            # db.session.commit()

            # access_token = create_access_token(identity=user.user_id)

            return jsonify({
                # 'token': access_token,
                'user': {
                    'id': user.user_id,
                    'username': user.username,
                    'full_name': user.full_name
                }
            }), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = users.query.get(current_user_id)
    return jsonify({'logged_in_as': user.username}), 200
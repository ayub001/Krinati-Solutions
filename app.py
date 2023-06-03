from flask import Flask, jsonify, request
from database import insert_user, get_user, get_all_users
from redis import Redis
from flask_caching import Cache

redis = Redis(host='redis', port=6379)  # Assuming Redis is running on the same Docker network

app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS': redis
})

@app.route('/match/<int:user_id>', methods=['GET'])
def get_potential_matches(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify(error='User not found'), 404

    user_hobbies = set(user[2].split(','))

    users = get_all_users()
    potential_matches = []

    for other_user in users:
        if other_user[0] == user_id:
            continue  # Skip the same user

        other_user_hobbies = set(other_user[2].split(','))
        common_hobbies = user_hobbies.intersection(other_user_hobbies)

        if len(common_hobbies) > 0:
            potential_matches.append({
                'id': other_user[0],
                'name': other_user[1],
                'hobbies': list(common_hobbies)
            })

    return jsonify(potential_matches)

if __name__ == '__main__':
    app.run()

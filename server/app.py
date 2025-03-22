
from flask import Flask, request, jsonify
from database import get_db_connection, init_db
import psycopg2
from config import Config


app = Flask(__name__)

with app.app_context():
    init_db()


@app.route('/player/<player_id>', methods=['GET'])
def get_player_score(player_id):
    """Получение текущего счета игрока"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT total_score, games_played FROM players WHERE id = %s', (player_id,))
    player = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if player:
        return jsonify({'player_id': player_id, 'total_score': player[0], 'games_played': player[1]})
    else:
        return jsonify({'player_id': player_id, 'total_score': 0, 'games_played': 0})


@app.route('/player/<player_id>/score', methods=['POST'])
def update_player_score(player_id):
    """Обновление счета игрока"""
    score = request.json.get('score', 0)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT total_score FROM players WHERE id = %s', (player_id,))
    player = cur.fetchone()
    
    if player:
        cur.execute(
            'UPDATE players SET total_score = total_score + %s, games_played = games_played + 1 WHERE id = %s',
            (score, player_id)
        )
    else:
        cur.execute(
            'INSERT INTO players (id, total_score, games_played) VALUES (%s, %s, 1)',
            (player_id, score)
        )
    
    conn.commit()
    
    cur.execute('SELECT total_score, games_played FROM players WHERE id = %s', (player_id,))
    updated_score, games_played = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'player_id': player_id,
        'score_added': score,
        'total_score': updated_score,
        'games_played': games_played,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)

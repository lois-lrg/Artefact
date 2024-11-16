import os
from flask import Flask, send_from_directory, request
from src.robot import robot, MAX_SPEED

app = Flask(__name__)

print(app.static_folder)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/move', methods=['POST'])
def service_move():
    direction = request.json['direction']
    if direction == 'forward':
        robot.move(MAX_SPEED, MAX_SPEED)
    elif direction == 'backward':
        robot.move(-MAX_SPEED, -MAX_SPEED)
    elif direction == 'right':
        robot.move(MAX_SPEED, -MAX_SPEED)
    elif direction == 'left':
        robot.move(-MAX_SPEED, MAX_SPEED)
    elif direction == 'stop':
        robot.stop()
    return '', 200

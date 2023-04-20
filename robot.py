from flask import Flask, request

app = Flask()

@app.route('/log_move', methods=['POST'])
def log_move():
    direction = request.json['direction']

    # Write the move to a file or database
    with open('moves.log', 'a') as f:
        f.write(direction + '\n')

    return 'OK'

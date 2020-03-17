from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
ROOM_SIZE_X = 15
ROOM_SIZE_Y = 10
location = None
x = None
y = None

@app.route('/input', methods=["POST"])
def input():
    payload = request.get_json(force=True)
    x = int(payload['x'])
    y = int(payload['y'])
    if x < 0 or x > ROOM_SIZE_X or y < 0 or y > ROOM_SIZE_Y :
        location = "outside of classroom"
    else :
        location = "inside of classroom"
    resp = {'status': "OK", 'location':location, 'x':x, 'y':y}
    return jsonify(resp)

@app.route('/show', methods=["GET"])
def show():
    resp = {'status': "OK", 'location':location, 'x':x, 'y':y}
    return jsonify(resp)
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)
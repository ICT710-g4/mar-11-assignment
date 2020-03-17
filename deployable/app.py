from flask import Flask, request, jsonify
import os
import math
import json
import paho.mqtt.subscribe as subscribe

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

CLIENT_ID = '0b568393-ce99-4d73-a0fc-4d6c4f8c1095'
NETPIE_TOKEN = '9F8Qm8LTB5u84hsrQLNRZD7YjzFoDEPw'

def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        return (x3, y3, x4, y4)
    
def triangulate(a,b,c):
    with open('points.json') as json_file:
        try:
            data = json.load(json_file)
            
            data["1"]["d"] = math.pow(10,(-56.4-a)/31.8905)
            data["2"]["d"] = math.pow(10,(-56.4-b)/31.8905)
            data["3"]["d"] = math.pow(10,(-56.4-c)/31.8905)
            
            temp = get_intersections(data["1"]["x"],data["1"]["y"],data["1"]["d"],data["2"]["x"],data["2"]["y"],data["2"]["d"])
            avg12 = [0.5*(temp[0]+temp[2]), 0.5*(temp[1]+temp[3])]

            temp = get_intersections(data["1"]["x"],data["1"]["y"],data["1"]["d"],data["3"]["x"],data["3"]["y"],data["3"]["d"])
            avg13 = [0.5*(temp[0]+temp[2]), 0.5*(temp[1]+temp[3])]

            temp = get_intersections(data["2"]["x"],data["2"]["y"],data["2"]["d"],data["3"]["x"],data["3"]["y"],data["3"]["d"])
            avg23 = [0.5*(temp[0]+temp[2]), 0.5*(temp[1]+temp[3])]

            avg = [(avg12[0]+avg13[0]+avg23[0])/3, (avg12[1]+avg13[1]+avg23[1])/3]
            #print(avg)
            return avg
        except TypeError:
            print("Invalid Coordinate (No Possible Coordinate)")
            return -1
ROOM_SIZE_X = 15
ROOM_SIZE_Y = 10
@app.route('/summary', methods=["GET"])
def summary():
    node_1_rssi = None
    node_2_rssi = None
    node_3_rssi = None
    while node_1_rssi == None or node_2_rssi == None or node_3_rssi == None:
            msg = subscribe.simple('@msg/taist2020/button/#', hostname='mqtt.netpie.io', port=1883, client_id=CLIENT_ID, auth={'username':NETPIE_TOKEN, 'password':None}, keepalive=10)
            print("%s %s" % (msg.topic, msg.payload))
            data = eval(str(msg.payload).split("'")[1][0:-4])
            device_num = int(msg.topic.split("/")[-1])
            if(device_num == 1):
                print("get rssi: {} form node {}".format(data["rssi"], device_num))
                node_1_rssi = data["rssi"]
            elif(device_num == 2):
                print("get rssi: {} form node {}".format(data["rssi"], device_num))
                node_2_rssi = data["rssi"]
            elif(device_num == 3):
                print("get rssi: {} form node {}".format(data["rssi"], device_num))
                node_3_rssi = data["rssi"]
    x = triangulate(node_1_rssi,node_2_rssi,node_3_rssi)
    if x == -1 :
        answer = 'location_not_found'
        return jsonify({'status':answer})
    else :
        if x[0]<0 or x[0] > ROOM_SIZE_X or x[1]<0 or x[1]> ROOM_SIZE_Y :
            answer = 'out'
        else :
            answer = 'in'
    resp = {'status':answer, 'x':x[0], 'y':x[1]}
    return jsonify(resp)

@app.route('/input', methods=["POST"])
def input():
    payload = request.get_json(force=True)
    x = payload['x']
    y = payload['y']
    if x<0 or x > ROOM_SIZE_X or y<0 or y> ROOM_SIZE_Y :
        answer = 'out'
    else :
        answer = 'in'
    resp = {'status': answer, 'x': x[0], 'y': x[1]}
    return jsonify(resp)
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)

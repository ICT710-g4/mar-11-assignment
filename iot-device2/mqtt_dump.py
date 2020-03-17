import paho.mqtt.subscribe as subscribe

CLIENT_ID = '0b568393-ce99-4d73-a0fc-4d6c4f8c1095'
NETPIE_TOKEN = '9F8Qm8LTB5u84hsrQLNRZD7YjzFoDEPw'

if __name__ == '__main__':
    while True:
        msg = subscribe.simple('@msg/taist2020/button/#', hostname='mqtt.netpie.io', port=1883, client_id=CLIENT_ID, auth={'username':NETPIE_TOKEN, 'password':None}, keepalive=10)
        print("%s %s" % (msg.topic, msg.payload))
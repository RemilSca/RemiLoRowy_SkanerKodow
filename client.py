import paho.mqtt.client as mqtt
import base64
import json

loaded = {}


def generate_db():
    global loaded
    with open('clientbase.json', 'r') as f:
        loaded = json.loads(f.read())

    g = {}

    for x in loaded.keys():
        g[x] = loaded[x]["kod"]

    with open('db.txt', 'w') as f:
        f.write(str(g))



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


    client.subscribe("v3/remilora@ttn/devices/+/up")

def on_message(client, userdata, msg):
    global loaded
    print(msg.topic+" "+str(msg.payload))
    p = json.loads(msg.payload.decode('ascii'))
    p = p["uplink_message"]["frm_payload"]
    p = base64.b64decode(p).decode('ascii')
    loaded[p]['ilosc'] -= 1
    print(f"Zeskanowano {loaded[p]['nazwa']}, pozostalo {loaded[p]['ilosc']}")

    with open('clientbase.json', 'w') as f:
        f.write(str(json.dumps(loaded)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

username = "remilora@ttn"
passwd = "NNSXS.ZKNP6COZANHN4HZG5KCWBGHWW2WP7M3VLRSEGLI.IDUBI26PLOEUGFOI2X35L2XTT6CSXJDRRKA2BHUFUJXCQOZGFFNQ"

generate_db()

client.username_pw_set(username, password=passwd)
client.connect("eu1.cloud.thethings.network", 1883, 60)

client.loop_forever()

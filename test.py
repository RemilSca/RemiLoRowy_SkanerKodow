import paho.mqtt.client as mqtt
import base64

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#/up")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    p = msg.payload.uplink_message.frm_payload
    p.decode("ascii")
    print(p)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

username = "remilora@ttn"
passwd = "NNSXS.ZKNP6COZANHN4HZG5KCWBGHWW2WP7M3VLRSEGLI.IDUBI26PLOEUGFOI2X35L2XTT6CSXJDRRKA2BHUFUJXCQOZGFFNQ"


client.username_pw_set(username, password=passwd)
client.connect("eu1.cloud.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

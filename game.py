import paho.mqtt.client as mqtt
import json
import multiprocessing

import time

prefix = "teamproject/groep8/"
steps = 0
game = False
name = ""
difficulty = ""
score = 0


def on_connect(client, userdata, flags, rc):
    global prefix

    client.subscribe([(f"{prefix}quantitysteps", 0), (f"{prefix}gamestart", 0), (f"{prefix}gamestop", 0)])


def on_message(client, userdata, msg):
    global prefix, steps, game, name, difficulty, score

    if msg.topic == f"{prefix}quantitysteps":
        payload = json.loads(msg.payload)
        
        if game != True:
            if int(payload["steps"]) < 1:
                message = {"answer": "Step quantity must be higher than 0"}
                client.publish(f"{prefix}quantitysteps/answer", json.dumps(message))
            elif int(payload["steps"]) % 2 != 0:
                message = {"answer": "Step quantity must be divisible by 2"}
                client.publish(f"{prefix}quantitysteps/answer", json.dumps(message))
            else:
                steps = payload["steps"]
                print("Step quantity has been set to " + str(steps))
                message = {"answer": "Steps has successfully been configured"}
                client.publish(f"{prefix}quantitysteps/answer", json.dumps(message))
    elif msg.topic == f"{prefix}gamestart":
        payload = json.loads(msg.payload)

        if game != True:
            if payload["name"] != "" and (payload["difficulty"] == "easy" or payload["difficulty"] == "normal" or payload["difficulty"] == "hard"):
                game = True
                name = payload["name"]
                difficulty = payload["difficulty"]

                print("Game has started", game, name, difficulty)
                message = {"answer": "Game has started"}
                client.publish(f"{prefix}gamestart/answer", json.dumps(message))
            else:
                print("Fault in game start")
                message = {"answer": "Input is not correct"}
                client.publish(f"{prefix}gamestart/answer", json.dumps(message))
    elif msg.topic == f"{prefix}gamestop":
        game = False

        print("Game stopped")
        message = {"start": game, "name": name, "score": score}
        client.publish(f"{prefix}game/answer", json.dumps(message))


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("13.81.105.139", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    
    while True:
        if game:
            message = {"start": game, "name": name, "score": score}
            client.publish(f"{prefix}game/answer", json.dumps(message))
            time.sleep(1)
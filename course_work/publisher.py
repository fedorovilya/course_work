import paho.mqtt.client as mqttClient
import time
import random


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:

        print("Connection failed")


Connected = False  # global variable for the state of the connection

broker_address = "0.0.0.0"
port = 1883
# password = "1"

client = mqttClient.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.connect(broker_address, port=port)  # connect to broker

client.loop_start()  # start the loop

while Connected != True:  # Wait for connection
    time.sleep(0.1)

# температура на датчиках по москве.
# подразумевается 24 измерения на 1 день. программа будет моделировать до нажатия ctrl+c
# in_sun
# in_shadow
# real_feel
try:
    time_now = 0
    day = 1
    month = 1
    year = 2021

    delta = 1
    value = -5

    real_feel = value
    wing = False

    flag = False

    while True:
        if (3< month < 6) or (9< month < 12):
            delta = 2
        else: delta = 1
        if time_now == 24:
            time_now = 0
            day += 1
        if day == 30:
            day = 1
            month += 1
            if 3 <= month < 8:
                value += random.uniform(3, delta*5)
                flag = True
            else:
                value -= random.uniform(3, delta*5)
        if month == 12:
            month = 1
            year += 1

        wing = random.choice([0, 1])

        if 7 < time_now < 20:  # температура обычно колеблется днем, ночью чаще всего она снижается
            value = value + random.uniform(0, delta/2)
            if value >= 50:
                value = 50
        else:
            value = value - random.uniform(0, delta/2)
            if value <= -50:
                value = -50

        time_now += 1
        if wing == 1:
            real_feel = value - delta
	
        temp = "temp_measurement,type=temperature value={0}".format(round(value, 2))
        print(temp)
        client.publish("sensors/temp", temp)

        temp = "realfeel_measurement,type=real_feel value={0}".format(round(real_feel, 2))
        print(temp)
        client.publish("sensors/real_feel", temp)

        temp = "wing_measurement,type=was_wing value={0}".format(wing)
        print(temp)
        client.publish("sensors/wing", temp)

  	#temp = "temp_measurement,type=temperature value={0}".format(round(value, 2))
        #print(temp)
        #client.publish("sensors/temp", temp)

        #temp = "realfeel_measurement,type=real_feel value={0}".format(round(real_feel, 2))
        #print(temp)
        #client.publish("sensors/temp", temp)

        #temp = "wing_measurement,type=was_wing value={0}".format(wing)
        #print(temp)
        #client.publish("sensors/temp", temp)
        
        print(time_now," часа, ",day," день",month," месяц")
        time.sleep(0.05)

except KeyboardInterrupt:

    client.disconnect()
    client.loop_stop()

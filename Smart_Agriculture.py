import RPi.GPIO as GPIO
import time
import requests
import json
from sklearn.ensemble import RandomForestRegressor
import numpy as np

GPIO.setmode(GPIO.BCM)
MOISTURE_SENSOR_PIN = 17
GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

FCM_SERVER_KEY = 'RUD_FCM_SERVER_KEY'
FCM_URL = 'https://fcm.googleapis.com/fcm/send'

#Moisture, Time of day, Temperature, Irrigation (1 or 0)
data = np.array([
    [50, 12, 30, 1],
    [30, 13, 28, 1],
    [60, 14, 29, 0],
    [70, 15, 27, 0],
])
X = data[:, :-1]
y = data[:, -1]
model = RandomForestRegressor()
model.fit(X, y)

def read_soil_moisture():
    return GPIO.input(MOISTURE_SENSOR_PIN)

def predict_irrigation(moisture, time_of_day, temperature):
    prediction = model.predict([[moisture, time_of_day, temperature]])
    return prediction[0]

def send_notification(message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'key={FCM_SERVER_KEY}'
    }

    payload = {
        'to': '/topics/all',
        'notification': {
            'title': 'Irrigation Alert',
            'body': message,
        },
        'priority': 'high',
    }

    response = requests.post(FCM_URL, headers=headers, data=json.dumps(payload))
    return response.json()


try:
    while True:
        moisture_level = read_soil_moisture()

        time_of_day = 14
        temperature = 28

        irrigation_needed = predict_irrigation(moisture_level, time_of_day, temperature)

        if irrigation_needed == 1:
            notify_irrigation_needed()

        time.sleep(60)

except KeyboardInterrupt:
    GPIO.cleanup()

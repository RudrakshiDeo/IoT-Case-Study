import Adafruit_DHT
import paho.mqtt.client as mqtt
import sqlite3


def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    return temperature, humidity

def send_mqtt_alert(topic, message):
    client = mqtt.Client()
    client.connect("broker_address", 1883, 60)
    client.publish(topic, message)
    client.disconnect()

def insert_data_to_db(db_path, temperature, humidity):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (timestamp, temperature, humidity) VALUES (datetime('now'), ?, ?)",
                   (temperature, humidity))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    temperature, humidity = read_sensor_data()

    max_temp_threshold = 30
    min_humidity_threshold = 20

    if temperature > max_temp_threshold:
        send_mqtt_alert("temperature_alert", f"Temperature: {temperature}°C exceeded threshold")
    if humidity < min_humidity_threshold:
        send_mqtt_alert("humidity_alert", f"Humidity: {humidity}% below threshold")

    insert_data_to_db("sensor_data.db", temperature, humidity)
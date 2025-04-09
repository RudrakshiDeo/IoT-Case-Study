import time
import random
import json


class TrafficData:
    def __init__(self, sensor_id, vehicle_count):
        self.sensor_id = sensor_id
        self.vehicle_count = vehicle_count
        self.timestamp = time.time()

    def to_json(self):
        return json.dumps({
            "sensor_id": self.sensor_id,
            "vehicle_count": self.vehicle_count,
            "timestamp": self.timestamp
        })


def send_command(command, sensor_id):
    print(f"[Command] Sensor {sensor_id}: {command}")

def analyze_traffic(data):
    count = data.get("vehicle_count", 0)
    sensor_id = data.get("sensor_id", "UNKNOWN")

    if count > 70:
        send_command("REDUCE_GREEN", sensor_id)
    else:
        send_command("NORMAL_FLOW", sensor_id)


def simulate_sensor(sensor_id):
    while True:
        data = TrafficData(sensor_id, random.randint(20, 100))
        print(f"[Sensor] Sent: {data.to_json()}")
        analyze_traffic(json.loads(data.to_json()))
        time.sleep(2)

if __name__ == "__main__":
    simulate_sensor("SENSOR_1")

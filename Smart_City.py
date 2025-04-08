import socket
import threading
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


def handle_client(client_socket):
    with client_socket:
        data = client_socket.recv(1024)
        if data:
            try:
                traffic_data = json.loads(data.decode())
                print("Received:", traffic_data)
                analyze_traffic(traffic_data)
            except Exception as e:
                print("Error processing data:", e)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen()
    print("[Server] Listening on port 5000...")
    while True:
        client_sock, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()


def simulate_sensor(sensor_id):
    while True:
        data = TrafficData(sensor_id, random.randint(20, 100))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', 5000))
                sock.sendall(data.to_json().encode())
                print(f"[Sensor] Sent: {data.to_json()}")
        except Exception as e:
            print("Sensor error:", e)
        time.sleep(2)



if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)  # Let the server start
    simulate_sensor("SENSOR_1")
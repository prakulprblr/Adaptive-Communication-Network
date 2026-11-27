import socket
import time

SERVER_IP = "10.0.0.2"
PORT = 5005
PACKETS = 100

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.5)

received = 0
latencies = []
start = time.time()

for seq in range(1, PACKETS + 1):
    message = str(seq).encode()
    sent = time.time()
    client.sendto(message, (SERVER_IP, PORT))

    try:
        data, address = client.recvfrom(1024)
        latency = (time.time() - sent) * 1000
        latencies.append(latency)
        received += 1
        print("Packet", seq, "received | Latency:",
              round(latency, 2), "ms")
    except socket.timeout:
        print("Packet", seq, "lost")

elapsed = time.time() - start
lost = PACKETS - received

print("\n--- UDP Results ---")
print("Packets sent:", PACKETS)
print("Packets received:", received)
print("Packets lost:", lost)
print("Packet loss:", round(lost / PACKETS * 100, 2), "%")

if latencies:
    print("Average latency:",
          round(sum(latencies) / len(latencies), 2), "ms")

print("Total time:", round(elapsed, 2), "seconds")
client.close()

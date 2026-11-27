
import socket
import time

SERVER = ("10.0.0.2", 5005)
TOTAL_PACKETS = 1000
INTERVAL = 0.02
TIMEOUT = 0.05
LOSS_THRESHOLD = 3

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

sent = 0
received = 0
lost = 0
latencies = []
consecutive_losses = 0
outage_start = None
recovery_time = None
start = time.monotonic()

for seq in range(1, TOTAL_PACKETS + 1):
    message = str(seq).encode()
    sent_at = time.monotonic()

    try:
        sock.sendto(message, SERVER)
        sent += 1
        data, _ = sock.recvfrom(1024)
        received_at = time.monotonic()

        if data != message:
            lost += 1
            consecutive_losses += 1
        else:
            received += 1
            latencies.append((received_at - sent_at) * 1000)

            if consecutive_losses >= LOSS_THRESHOLD and outage_start is not None:
                if recovery_time is None:
                    recovery_time = received_at
                    print("Recovery observed at {:.3f} seconds".format(
                        recovery_time - start
                    ))

            consecutive_losses = 0

    except socket.timeout:
        lost += 1
        consecutive_losses += 1

        if consecutive_losses == LOSS_THRESHOLD:
            outage_start = sent_at
            print("Sustained outage detected near {:.3f} seconds".format(
                outage_start - start
            ))

    time.sleep(INTERVAL)

elapsed = time.monotonic() - start

print("\n--- Continuous UDP Results ---")
print("Packets sent:", sent)
print("Packets received:", received)
print("Packets lost:", lost)
print("Packet loss: {:.2f}%".format(
    lost / sent * 100 if sent else 0
))
print("Average RTT latency: {:.3f} ms".format(
    sum(latencies) / len(latencies) if latencies else 0
))
print("Total duration: {:.2f} seconds".format(elapsed))

if outage_start is not None and recovery_time is not None:
    print("Observed outage interval: {:.3f} seconds".format(
        recovery_time - outage_start
    ))
elif outage_start is not None:
    print("Outage detected, but recovery was not observed")
else:
    print("No sustained outage detected")

sock.close()

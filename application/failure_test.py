import time
import subprocess

print("Waiting 5 seconds...")
time.sleep(5)

print("Taking S2-S4 link down...")
subprocess.run(
    ["sudo", "mnexec", "-a", "1", "true"],
    check=False
)

print("Test setup ready.")

# Adaptive Communication Network with Failure Recovery

Software-Defined Networking mini-project demonstrating OpenFlow 1.3 link-failure detection and automatic path switching between primary and backup routes using OS-Ken and Mininet.

## Network design

- Hosts: H1 (`10.0.0.1`) and H2 (`10.0.0.2`)
- Primary path: H1 → S1 → S2 → S4 → H2
- Backup path: H1 → S1 → S3 → S4 → H2
- The controller switches to the backup route when S2–S4 fails and restores the primary route after recovery.

## Project structure

```text
application/   UDP client, server, monitor, and failure test
controller/    OS-Ken SDN controller
topology/      Mininet topology
requirements.txt
.gitignore
project/Adaptive-Communication-Network-GitHub.zip  Full clean project archive, including recorded results
```

## Prerequisites

Use Ubuntu with Python 3, Mininet, and Open vSwitch installed.

```bash
sudo apt update
sudo apt install -y mininet openvswitch-switch python3-venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

Terminal 1 (repository root):

```bash
source .venv/bin/activate
python -u -m controller.run_controller
```

Terminal 2:

```bash
sudo python3 topology/topology.py
```

At the `mininet>` prompt, run `pingall` to check connectivity.

## Test failover and recovery

At the Mininet prompt:

```text
link s2 s4 down
pingall
sh ovs-ofctl -O OpenFlow13 dump-flows s3
link s2 s4 up
pingall
```

## UDP tests

- `application/udp_server.py`: UDP echo server
- `application/udp_client.py`: sends 100 packets and reports loss and latency
- `application/udp_monitor.py`: continuous 1,000-packet monitoring

Run the server and client on the appropriate Mininet hosts using the configured addresses. The scripts may need to be copied into the Mininet hosts before execution.

## Recorded results

The full archive in `project/` includes the captured baseline, failure, and continuous-monitor output. One monitor run recorded 999/1,000 packets received (0.10% packet loss) and an observed outage interval of 0.029 seconds. This is a run-specific observation, not a validated general recovery-time guarantee.

## Notes

Local virtual environments, Python bytecode caches, editor settings, and backup files are excluded through `.gitignore`. Recreate the environment using the commands above.

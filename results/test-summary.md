# Recorded UDP test summary

These figures are transcribed from the project's saved test outputs.

| Test | Packets sent | Packets received | Packets lost | Packet loss | Average latency / RTT |
|---|---:|---:|---:|---:|---:|
| Baseline UDP test | 100 | 100 | 0 | 0.00% | 0.24 ms average latency |
| Primary-link failure test | 100 | 100 | 0 | 0.00% | 0.27 ms average latency |
| Continuous UDP monitor | 1,000 | 999 | 1 | 0.10% | 0.602 ms average RTT |

The continuous-monitor run recorded an observed outage interval of 0.029 seconds over a total duration of 21.07 seconds. Treat this as a run-specific observation, not a validated general recovery-time guarantee.

The full packet-by-packet logs remain in the original local project archive. The table above preserves the recorded summary values in this repository.

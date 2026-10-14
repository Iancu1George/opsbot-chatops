# OpsBot - Cloud Infrastructure & ChatOps Utility

A Python-based ChatOps utility integrated via Discord, designed for real-time cloud infrastructure monitoring. This project demonstrates core SysAdmin, networking, and automation concepts, currently running 24/7 on an Oracle Cloud Infrastructure (OCI) instance.

## Key Features

* **Network Diagnostics (`!ping-ip`):** Utilizes OS-level subprocessing to send ICMP packets and return network statistics.
* **Service Monitoring (`!check-port`):** Performs TCP port scanning via the `socket` library to verify service availability.
* **HTTP Uptime & Latency (`!http`):** Monitors website status and response times, implementing User-Agent spoofing to bypass basic WAF (Web Application Firewall) restrictions.
* **Security & Access Control (RBAC):** Restricts critical network commands exclusively to server administrators and securely manages API secrets.

## Technologies & Stack

* **Language:** Python 3 (`discord.ext`, `socket`, `urllib`, `subprocess`)
* **Infrastructure:** Oracle Cloud (OCI), Ubuntu Linux (ARM Ampere)
* **Operations:** SSH, `tmux` for background process persistence

> *Note: For security reasons, the `.env` file containing the Discord API token is strictly excluded from this public repository.*

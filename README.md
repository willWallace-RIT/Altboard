
# Onboard Toggle Daemon

A lightweight Linux background daemon and script suite designed to monitor the **Onboard** virtual keyboard, track lifecycle states via a persistent boolean toggle file, and fire a custom action script on every alternating close event.

---

## Repository Structure

```text
.
â”œâ”€â”€ daemon/
â”‚   â””â”€â”€ onboard_kb_daemon.py     # Background polling daemon script
â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ launcher_action.sh       # Target payload script executed on alternating cycles
â””â”€â”€ systemd/
    â””â”€â”€ onboard_kb_daemon.service# Systemd user service unit configuration
```

---

## Installation & Setup

### 1. Clone or Copy Files to System Paths
Place the scripts and service configuration files into their respective runtime directories:

```bash
sudo mkdir -p /usr/local/bin
sudo cp daemon/onboard_kb_daemon.py /usr/local/bin/onboard_kb_daemon.py
sudo cp scripts/launcher_action.sh /usr/local/bin/launcher_action.sh
sudo chmod +x /usr/local/bin/onboard_kb_daemon.py
sudo chmod +x /usr/local/bin/launcher_action.sh
```

### 2. Configure the Systemd User Service
Create your user systemd directory if it does not already exist, then deploy the service file:

```bash
mkdir -p ~/.config/systemd/user
cp systemd/onboard_kb_daemon.service ~/.config/systemd/user/onboard_kb_daemon.service
```

### 3. Enable and Start the Service
Reload the systemd user manager, enable the service to start on login, and launch it immediately:

```bash
systemctl --user daemon-reload
systemctl --user enable --now onboard_kb_daemon.service
```

---

## Verification & Monitoring

* **Check Service Status:**
  ```bash
  systemctl --user status onboard_kb_daemon.service
  ```
* **View Live Daemon Logs:**
  ```bash
  journalctl --user -u onboard_kb_daemon.service -f
  ```
* **Inspect Trigger Output:**
  ```bash
  tail -f /tmp/onboard_trigger.log
  ```

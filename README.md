# 🛡️ CachyShield v3.1
An Ephemeral, Zero-Trust Linux Kernel Container Sandbox built natively for Arch Linux and CachyOS.

## 🚀 What it does
CachyShield traps untrusted scripts, AI agents, or potential malware inside an isolated kernel namespace barrier.
* **Network Isolation:** Automatically unplugs the network interface.
* **Process Tree Isolation:** Blocks visibility of your host operating system apps.
* **Nuclear Self-Destruct:** Instantly obliterates the isolated environment and every trace of running files upon exit.

## 🛠️ How to install and run
```bash
# Clone the repository
git clone https://github.com
cd CachyShield

# Initialize and build the sandbox jail filesystem
./reset.sh

# Launch the secure containment sandbox
sudo python sandbox_engine.py
```

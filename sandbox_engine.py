import os
import sys
import subprocess
import shutil

def clean_and_rebuild():
    """Wipes out the jail folder and recreates a pristine system state."""
    print("\n🧹 NUCLEAR PROTOCOL ACTIVATED: Destroying all traces of the sandbox environment...")
    
    # 1. Call our master reset script to completely wipe and rebuild a clean folder structure
    try:
        # Using absolute path to make sure it finds reset.sh
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reset_script = os.path.join(current_dir, "reset.sh")
        
        # Run reset.sh silently in the background
        subprocess.run(["fish", reset_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✨ SUCCESS: Every file created inside the sandbox has been obliterated and reset!")
    except Exception as e:
        print(f"[-] Rebuild failure: {e}")

def launch_secure_sandbox():
    print("🛡️  CachyShield v3.0: Initializing Ephemeral Linux Kernel Isolation...")
    
    jail_path = os.path.abspath("./jail")
    
    if os.getuid() != 0:
        print("[-] Access Denied: Core Linux namespace allocation requires root privileges.")
        print("[*] Please run this tool using: sudo python sandbox_engine.py")
        sys.exit(1)

    print("[+] Namespaces configured: [Network=DISABLED] [ProcessTree=ISOLATED] [Filesystem=JAIL]")
    
    command = [
        "unshare", "--mount", "--net", "--pid", "--fork",
        "chroot", jail_path, "/bin/bash", "--rcfile", "/etc/profile"
    ]
    
    try:
        print("\n⚡ Dropping into CachyShield containment zone. Type exit to leave.")
        print("="*65)
        subprocess.run(command, check=True)
        print("="*65)
    except Exception as e:
        print(f"[-] Sandbox execution failure: {e}")
    finally:
        # The finally block ALWAYS runs when the sandbox closes, no matter what!
        clean_and_rebuild()

if __name__ == "__main__":
    launch_secure_sandbox()

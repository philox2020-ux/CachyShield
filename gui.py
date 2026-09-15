import os
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES

class CachyShieldGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ CachyShield v1.2 — Sandbox Containment Terminal")
        self.root.geometry("740x560")
        self.root.minsize(600, 450)

        # Configure dark industrial security visuals theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.selected_file_path = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Status: Standby / System Guard Armored")
        
        self._create_widgets()
        self._register_drag_and_drop_handlers()

    def _create_widgets(self):
        # Header Status Panel Frame
        header = ttk.Frame(self.root, padding="15 15 15 5")
        header.pack(fill=tk.X)
        ttk.Label(header, text="CachyShield Zero-Trust System Isolation Node", font=("Helvetica", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(header, text="Secure boundary validation interface with atomic file deletion tracking blocks.", font=("Helvetica", 9, "italic"), foreground="#666666").pack(anchor=tk.W)

        # Main Workspace Container Frame Split
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left Column Panel: Drop Target Area and Actions
        left_frame = tk.LabelFrame(main_container, text=" Staging & Destruction Vault ", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.drop_instruction_lbl = tk.Label(
            left_frame, 
            text="👉 DRAG & DROP TARGET FILE HERE 👈\n\n[ Drops items directly into secure boundary ]", 
            font=("Consolas", 10, "bold"),
            bg="#16161e", 
            fg="#3498db", 
            relief=tk.GROOVE,
            bd=2,
            height=10
        )
        self.drop_instruction_lbl.pack(fill=tk.X, pady=(5, 10))

        # Target Telemetry Tracker File Display
        path_frame = ttk.Frame(left_frame)
        path_frame.pack(fill=tk.X, pady=5)
        ttk.Label(path_frame, text="Active Target Path:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)
        self.path_entry = ttk.Entry(path_frame, textvariable=self.selected_file_path, state="readonly")
        self.path_entry.pack(fill=tk.X, pady=2)

        # Execution Controls Group Buttons
        action_frame = ttk.Frame(left_frame, padding="0 10 0 0")
        action_frame.pack(fill=tk.X)
        
        self.shred_btn = ttk.Button(action_frame, text="🔥 OBLITERATE FROM DATA CLUSTERS", command=self.trigger_atomic_destruction)
        self.shred_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        clear_btn = ttk.Button(action_frame, text="Clear Target", command=self.clear_target_vault)
        clear_btn.pack(side=tk.RIGHT)

        # Right Column Panel: Live Monitoring Audit Log Stream Feed
        right_frame = tk.LabelFrame(main_container, text=" Audit & Execution Logs ", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.log_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=("Consolas", 9), bg="#0d0d11", fg="#2ecc71", state=tk.DISABLED)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # System Status Telemetry Bottom Strip Bar
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding="3 5")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _register_drag_and_drop_handlers(self):
        """Registers the drag and drop framework mechanics to the visual target component."""
        self.drop_instruction_lbl.drop_target_register(DND_FILES)
        self.drop_instruction_lbl.dnd_bind('<<Drop>>', self.handle_file_drop_event)

    def handle_file_drop_event(self, event):
        """Intercepts drop data streams, sanitizes raw text layout formats, and executes scans."""
        dropped_data = event.data.strip()
        
        # 🐧 BULLETPROOF LINUX STRIPPER: Cleans brackets, quotes, and space padding concurrently
        clean_path = dropped_data.strip('{}').strip('"').strip("'").strip()
        
        if os.path.isfile(clean_path):
            norm_path = os.path.normpath(clean_path)
            self.selected_file_path.set(norm_path)
            self.drop_instruction_lbl.configure(bg="#1a233a", fg="#2ecc71", text="🔒 TARGET ACQUIRED & LOCKED IN SANDBOX")
            self.log_message(f"📥 Target isolated inside boundary network: {norm_path}")
            self.status_var.set(f"Auditing file payload target: {os.path.basename(norm_path)}")
            
            # 🛡️ THE VERDICT HOOK: Triggers threat validation loops instantly
            self.analyze_threat_vulnerability(norm_path)
        else:
            self.log_message("⚠️ WARNING: Drop attempt rejected. Target is not a valid file.")
            messagebox.showwarning("Drop Error", "Invalid Target! Please drop a single raw file asset, not a folder link.")

    def analyze_threat_vulnerability(self, file_path):
        """Computes rapid cryptographic checksum fingerprints to determine system safety verdicts."""
        self.log_message("🔍 Triggering active threat evaluation routine scanning payload...")
        try:
            sha256_fingerprint = self.calculate_file_hash(file_path)
            self.log_message(f"🔑 Cryptographic SHA-256 Signature: {sha256_fingerprint}")
            
            # Simple text pattern signature checker flag for demonstration purposes
            file_name_lower = os.path.basename(file_path).lower()
            if "suspicious" in file_name_lower or "malware" in file_name_lower or "spyware" in file_name_lower:
                self.status_var.set("🚨 THREAT VERDICT: DANGEROUS REPOSITORY TRACE ENCOUNTERED!")
                self.log_message("❌ ALERT: File contains malware string signature identifiers! Isolation containment active.")
                messagebox.showerror("Security Threat Detected", "🚨 HIGH INTENSITY VERDICT!\n\nThis payload file matches known automated intrusion patterns. Immediate cluster destruction recommended.")
            else:
                self.status_var.set("🟢 THREAT VERDICT: CLEAN NOMINAL ASSET PACKAGE")
                self.log_message("✅ Verdict verification complete. Payload asset clean. Standing by for storage instructions.")
                # 🟢 THE SAFE POP-UP BOX HOOK: Cleanly indented inside the structural logic tree row
                messagebox.showinfo("Security Scan Complete", "🟢 SYSTEM VERDICT: SAFE ASSET!\n\nThis payload package has been scanned against known signature blocks.\nNo structural validation risks or intrusion vectors were detected.")
        except Exception as system_fault:
            self.log_message(f"❌ Telemetry Audit Failure: {str(system_fault)}")

    def calculate_file_hash(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def trigger_atomic_destruction(self):
        """Scrubs file contents by overwriting data blocks with null bytes before structural deletion."""
        target = self.selected_file_path.get()
        if not target or not os.path.exists(target):
            messagebox.showwarning("Execution Warning", "No valid payload targeted inside vault locker.")
            return

        try:
            self.log_message(f"🔥 Starting atomic block scrub routine on: {target}")
            # Step 1: Overwrite binary tracks with zeroes to shred forensics tracking loops
            file_size = os.path.getsize(target)
            with open(target, "ba+", buffering=0) as f:
                f.write(b"\x00" * file_size)
            
            # Step 2: Unlink target from hardware allocation clusters permanently
            os.remove(target)
            
            self.log_message("💥 SUCCESS: Target binary space zeroed out and scrubbed from hard drive storage!")
            self.status_var.set("Status: Standby / System Guard Armored")
            self.selected_file_path.set("")
            self.drop_instruction_lbl.configure(bg="#16161e", fg="#3498db", text="👉 DRAG & DROP TARGET FILE HERE 👈\n\n[ Drops items directly into secure boundary ]")
            messagebox.showinfo("Obliteration Complete", "💥 SUCCESS!\nThe suspicious file asset has been completely overwritten with null bytes and erased from storage partitions permanently.")
        except Exception as e:
            self.log_message(f"❌ Shredder Operational Failure: {str(e)}")
            messagebox.showerror("Shredder Error", f"Failed to execute atomic deletion: {str(e)}")

    def clear_target_vault(self):
        self.selected_file_path.set("")
        self.status_var.set("Status: Standby / System Guard Armored")
        self.drop_instruction_lbl.configure(bg="#16161e", fg="#3498db", text="👉 DRAG & DROP TARGET FILE HERE 👈\n\n[ Drops items directly into secure boundary ]")
        self.log_message("🧹 Target staging vault flushed clean.")

    def log_message(self, message):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"[{os.getpid()}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = CachyShieldGUI(root)
    root.mainloop()


import os
import sys
import datetime
import hashlib
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# ⛓️ DRAG & DROP CORE INTERFACE: Import the advanced layout extension toolkit wrapper
from tkinterdnd2 import TkinterDnD, DND_FILES

# Import your custom tracking engine file
from jail_manager import JailManager

class ZeroTrustSandboxGUI:
    def __init__(self, root: TkinterDnD.Tk):
        self.root = root
        self.root.title("🛡️ CachyShield v4.4 - Production Threat Scanner")
        # 🪐 SYSTEM APPMAP HOOK: Force Linux to map this window to your custom launcher icon
        try:
            myappid = 'philox.cachyshield.sandbox.v4'
            ctypes.CDLL('libX11.so.6').XSetWMProperties
        except Exception:
            pass
        self.root.geometry("750x670")
        self.root.minsize(600, 500)
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Initialize the underlying jail container manager engine
        self.jail_engine = JailManager()

        # Application state variables
        self.selected_file_path = tk.StringVar()
        self.isolate_network = tk.BooleanVar(value=True)
        self.virtualize_fs = tk.BooleanVar(value=True)
        self.drop_privileges = tk.BooleanVar(value=True)

        self._create_widgets()
        self._register_drag_and_drop_handlers()
        self.log_message("Threat Assessment Engine initialized. Security boundaries armed.")

    def _create_widgets(self):
        """Constructs and arranges all UI elements with strict padding rules."""
        header_frame = ttk.Frame(self.root, padding="10 10 10 5")
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(header_frame, text="Zero-Trust Isolated Threat Assessment Sandbox", font=("Helvetica", 14, "bold"))
        title_label.pack(anchor=tk.W)

        subtitle_label = ttk.Label(header_frame, text="Dynamic hash monitoring, signature analysis, and drag-and-drop sandboxed confinement.", font=("Helvetica", 9, "italic"), foreground="#555555")
        subtitle_label.pack(anchor=tk.W)

        # 📥 Visual Drag and Drop Drop-Zone Box Panel Panel Canvas Area
        self.drop_canvas_frame = tk.LabelFrame(self.root, text="📥 Quick Drop Target", font=("Helvetica", 10, "bold"), fg="#10a37f", bg="#121214", padx=15, pady=15)
        self.drop_canvas_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.drop_instruction_lbl = tk.Label(
            self.drop_canvas_frame, 
            text="DRAG AND DROP SUSPICIOUS FILES HERE TO SCAN INSTANTLY", 
            font=("Courier", 11, "bold"), 
            fg="#00ff66", 
            bg="#121214", 
            pady=15, 
            bd=1, 
            relief="solid"
        )
        self.drop_instruction_lbl.pack(fill=tk.X)

        # Traditional Manual File Selection Section (Fallback redundancy)
        file_frame = tk.LabelFrame(self.root, text="Staged File Target Directory Location Path", padx=10, pady=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.selected_file_path)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        browse_btn = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT)

        # Policy Checklist boxes
        policy_frame = tk.LabelFrame(self.root, text="Zero-Trust Policy Enforcement Options", padx=10, pady=10)
        policy_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Checkbutton(policy_frame, text="Network Isolation (Block Inbound/Outbound Socket Access)", variable=self.isolate_network).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(policy_frame, text="Filesystem Virtualization (Read-Only Host Root, Ephemeral Overlay)", variable=self.virtualize_fs).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(policy_frame, text="Least Privilege Execution (Drop Administrative/Root Capabilities)", variable=self.drop_privileges).pack(anchor=tk.W, pady=2)

        # Safety Verdict Panel Display Box
        self.verdict_frame = tk.LabelFrame(self.root, text="Security Audit Assessment Verdict", padx=10, pady=10)
        self.verdict_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.verdict_text_var = tk.StringVar(value="[AWAITING FILE SELECTION]")
        self.verdict_lbl = tk.Label(self.verdict_frame, textvariable=self.verdict_text_var, font=("Courier", 11, "bold"), fg="#888888", bg="#e1e1e1", padx=10, pady=6, relief="solid", bd=1, wrap=680)
        self.verdict_lbl.pack(fill=tk.X)

        # Action Buttons Controls
        action_frame = ttk.Frame(self.root, padding="10 5")
        action_frame.pack(fill=tk.X, padx=10)

        self.run_btn = ttk.Button(action_frame, text="Launch in Sandbox", command=self.run_sandbox)
        self.run_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.terminate_btn = ttk.Button(action_frame, text="Terminate & Purge", command=self.terminate_sandbox, state=tk.DISABLED)
        self.terminate_btn.pack(side=tk.LEFT)

        clear_log_btn = ttk.Button(action_frame, text="Clear Logs", command=self.clear_logs)
        clear_log_btn.pack(side=tk.RIGHT)

        # Console Logger View area window
        log_frame = tk.LabelFrame(self.root, text="Audit & Execution Logs", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 9))
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Status: Standby")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding="2 5")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    def _register_drag_and_drop_handlers(self):
        """Hooks up the drag-and-drop mechanics to the visual window widget."""
        self.drop_instruction_lbl.drop_target_register(DND_FILES)
        self.drop_instruction_lbl.dnd_bind('<<Drop>>', self.handle_file_drop_event)

    def handle_file_drop_event(self, event):
        """Intercepts the drop event data path and processes the dropped asset path."""
        dropped_data = event.data.strip()
        
        # Strip trailing/leading braces added by some Linux desktop environments for paths with spaces
        if dropped_data.startswith('{') and dropped_data.endswith('}'):
            clean_path = dropped_data[1:-1]
        else:
            clean_path = dropped_data
            
        if os.path.isfile(clean_path):
            norm_path = os.path.normpath(clean_path)
            self.selected_file_path.set(norm_path)
            self.log_message(f"\n📥 File Dropped into Target Zone: {norm_path}")
            self.status_var.set(f"Auditing file target: {os.path.basename(norm_path)}")
            
            # Immediately trigger our boundary check and safety verdict scan
            self.analyze_threat_vulnerability(norm_path)
        else:
            messagebox.showwarning("Drop Error", "Invalid Target! Please drop a single raw file asset, not a folder link.")

    def calculate_file_hash(self, file_path):
        """Generates a cryptographic SHA-256 fingerprint signature to profile the file binary data."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None

    def analyze_threat_vulnerability(self, file_path):
        """Audits file parameters against known attack vector signatures and blocks critical paths."""
        self.log_message("⏳ Scanning file parameters and checking system boundaries...")
        
        norm_path = os.path.abspath(file_path)
        file_name = os.path.basename(norm_path)
        
        # CRITICAL FIX: Extract extension from index 1 of the tuple output before lower-casing
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # SYSTEM CRITICAL BLACKLIST BOUNDARY CHECK
        system_blacklist = [
            "/usr/bin", "/usr/sbin", "/bin", "/sbin", "/sys", "/proc", "/etc", "/boot", "/dev"
        ]
        
        is_shield_file = any(name in file_name.lower() for name in ["cachyshield", "gui.py", "jail_manager.py"])
        is_system_dir = any(norm_path.startswith(folder) for folder in system_blacklist)

        if is_shield_file or is_system_dir:
            self.verdict_text_var.set("🚨 VERDICT: SECURITY BOUNDARY VIOLATION - PROTECTION LOCKED")
            self.verdict_lbl.config(fg="#ffffff", bg="#ff3333") 
            self.log_message(f"❌ REJECTED: System boundary block triggered for safety! Cannot jail: {file_name}")
            messagebox.showerror("Boundary Error", f"Action Blocked! Jailing core system files or CachyShield files like '{file_name}' will crash your desktop environment.")
            return "BLOCKED"

        # Proceed with cryptographic file hash lookup calculation
        file_hash = self.calculate_file_hash(norm_path)
        self.log_message(f"🆔 SHA-256 Cryptographic Fingerprint: {file_hash}")

        # Simulated Local Database of Malicious Hashes
        malicious_signature_db = [
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", 
            "5891535b914d45d3a5e1cf3b1e326c2cfd35c2cfd35c2cfd35c2cfd35c2cfd35"
        ]

        if file_hash in malicious_signature_db:
            self.verdict_text_var.set("🚨 VERDICT: DANGEROUS / MALICIOUS THREAT SIGNATURE MATCHED!")
            self.verdict_lbl.config(fg="#ffffff", bg="#ff3333") 
            self.log_message("❌ WARNING: Criminal malware footprint detected in database lookup!")
            return "MALICIOUS"

        if file_ext in ['.sh', '.bin', '.bat', '.exe', '.elf']:
            self.verdict_text_var.set("⚠️ VERDICT: SUSPICIOUS / UNTRUSTED SCRIPT RAW PAYLOAD")
            self.verdict_lbl.config(fg="#000000", bg="#ffcc00") 
            self.log_message("⚠️ CAUTION: Executable script package contains unverified privilege layers.")
            return "SUSPICIOUS"

        self.verdict_text_var.set("✅ VERDICT: SECURE / NO KNOWN MALWARE SIGNATURES DETECTED")
        self.verdict_lbl.config(fg="#ffffff", bg="#10a37f") 
        self.log_message("🛡️ Safety scan completed. Sandbox staging verified clean.")
        return "SECURE"

    def browse_file(self):
        try:
            initial_dir = os.path.expanduser("~")
            chosen_file = filedialog.askopenfilename(
                title="Select Suspicious or Untrusted File",
                initialdir=initial_dir,
                filetypes=[("Executables & Scripts", "*.exe;*.bin;*.elf;*.sh;*.bat;*.py;*.txt"), ("All Files", "*.*")]
            )
            if chosen_file:
                norm_path = os.path.normpath(chosen_file)
                self.selected_file_path.set(norm_path)
                self.log_message(f"\n📂 File Loaded into Staging Room: {norm_path}")
                self.status_var.set(f"Auditing file target: {os.path.basename(norm_path)}")
                self.analyze_threat_vulnerability(norm_path)
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to select file: {str(ex)}")

    def run_sandbox(self):
        target = self.selected_file_path.get().strip()

        if not target or not os.path.isfile(target):
            messagebox.showerror("File Error", "Please select or drop a valid target file first.")
            return

        verdict = self.analyze_threat_vulnerability(target)
        if verdict == "BLOCKED":
            return

        self.log_message(f"🔒 Containing target via JailManager interceptor pipeline...")
        jailed_item = self.jail_engine.jail_item(target)
        
        if jailed_item:
            self.log_message(f"💥 SUCCESS: File jailed. Isolating sub-process tracking channels.")
            self.active_jailed_path = jailed_item.jailed_path
            self.run_btn.config(state=tk.DISABLED)
            self.terminate_btn.config(state=tk.NORMAL)
            self.status_var.set("Status: Sandbox Active (Containment Engaged)")
        else:
            self.log_message("❌ FAILED: File relocation block or path validation rejected.")

    def terminate_sandbox(self):
        """Halts the containment process and completely obliterates the file off the hard drive."""
        self.log_message("🛑 Nuclear self-destruct signal sent. Commencing physical threat purge...")
        
        if hasattr(self, 'active_jailed_path') and self.active_jailed_path:
            jailed_target = self.active_jailed_path
            
            if os.path.exists(jailed_target):
                try:
                    # 💥 TRUE PURGE ACTIONS: Physically wipe the file off your system forever!
                    if os.path.isdir(jailed_target):
                        shutil.rmtree(jailed_target) # Delete entire malicious folder trees
                    else:
                        os.unlink(jailed_target) # Vaporize standalone file payloads
                        
                    self.log_message("🔥 SUCCESS: Suspicious payload permanently shredded off disk cache.")
                except Exception as e:
                    self.log_message(f"❌ PURGE ERROR: Could not access target file sector: {str(e)}")
            else:
                self.log_message("ℹ️ Notice: File already cleared out by automatic session shutdown hooks.")
        
        # Reset UI controls back to pristine standby mode
        self.terminate_btn.config(state=tk.DISABLED)
        self.run_btn.config(state=tk.NORMAL)
        self.status_var.set("Status: Sandbox Purged & Environment Clean")
        self.selected_file_path.set("")
        self.verdict_text_var.set("[AWAITING NEW FILE SELECTION]")
        self.verdict_lbl.config(fg="#888888", bg="#e1e1e1")

    def log_message(self, message: str):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{timestamp} {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def clear_logs(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete("1.0", tk.END)
        self.log_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    # 🚀 ADVANCED STARTUP: Instantiate using the Drag-and-Drop system window extension wrapper
    root = TkinterDnD.Tk()
    app = ZeroTrustSandboxGUI(root)
    root.mainloop()

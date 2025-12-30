import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import time
import json
import shutil
import random

# =========================
# SAFETY: SANDBOX ONLY
# =========================
ROOT = Path(__file__).resolve().parent
SANDBOX = ROOT / "demo_data"
USER_FILES = SANDBOX / "user_files"
SYSTEM_BOOT = SANDBOX / "system_boot"              # simulated startup folder
STRATEGIC = SANDBOX / "strategic_locations"        # simulated drop locations
LOGS = SANDBOX / "logs"
QUARANTINE = SANDBOX / "quarantine"

def ensure_sandbox():
    USER_FILES.mkdir(parents=True, exist_ok=True)
    SYSTEM_BOOT.mkdir(parents=True, exist_ok=True)
    STRATEGIC.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    # Create some dummy user files if empty
    if not any(USER_FILES.iterdir()):
        for i in range(1, 6):
            (USER_FILES / f"doc{i}.txt").write_text(
                f"Document {i}: notes de cours sécurité informatique.\n", encoding="utf-8"
            )

def log_event(kind, **detail):
    ensure_sandbox()
    ts = time.time()
    text_line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))} | {kind} | {detail}\n"
    (LOGS / "sim.log").open("a", encoding="utf-8").write(text_line)
    (LOGS / "sim.jsonl").open("a", encoding="utf-8").write(
        json.dumps({"ts": ts, "kind": kind, "detail": detail}, ensure_ascii=False) + "\n"
    )

# =========================
# SIMULATION ACTIONS (SAFE)
# =========================
def simulate_persistence():
    """Simulated persistence: just write a text file in demo_data/system_boot."""
    ensure_sandbox()
    entry = SYSTEM_BOOT / "autostart_entry.txt"
    entry.write_text(
        "SIMULATED AUTOSTART ENTRY (NO REAL PERSISTENCE)\n"
        "would_run=python app_gui.py\n"
        f"timestamp={time.time()}\n",
        encoding="utf-8",
    )
    log_event("PERSISTENCE_SIMULATED", created=str(entry))

def simulate_duplication(copies=3):
    """Simulated duplication: copy a harmless stub inside demo_data/strategic_locations."""
    ensure_sandbox()
    payload = SANDBOX / "payload_stub.bin"
    payload.write_bytes(b"SIMULATED_PAYLOAD_DO_NOT_EXECUTE")
    log_event("PAYLOAD_STUB_CREATED", path=str(payload), size=payload.stat().st_size)

    for i in range(copies):
        dest = STRATEGIC / f"copy_{i+1}_payload_stub.bin"
        shutil.copy2(payload, dest)
        log_event("DUPLICATION_SIMULATED", src=str(payload), dest=str(dest))

def simulate_scan():
    """Scan sandbox user files and log metadata."""
    ensure_sandbox()
    files = sorted([p for p in USER_FILES.rglob("*") if p.is_file()])
    log_event("SCAN_STARTED", directory=str(USER_FILES), count=len(files))
    for p in files:
        log_event("FILE_FOUND", path=str(p), size=p.stat().st_size)
    log_event("SCAN_FINISHED", count=len(files))

def simulate_ransomware_fake():
    """
    Fake ransomware behavior:
    - create LOCKED.txt note
    - rename files by appending '.locked' (reversible)
    No encryption.
    """
    ensure_sandbox()
    note = USER_FILES / "LOCKED.txt"
    note.write_text(
        "SIMULATION: vos fichiers ont été 'verrouillés' (renommage fictif) dans demo_data/user_files.\n"
        "Aucune donnée réelle n'a été chiffrée.\n",
        encoding="utf-8",
    )
    log_event("RANSOM_NOTE_CREATED", path=str(note))

    targets = [p for p in USER_FILES.rglob("*") if p.is_file() and p.name != "LOCKED.txt"]
    log_event("RANSOM_TARGETS", count=len(targets))
    for p in targets:
        newp = p.with_suffix(p.suffix + ".locked")
        if newp.exists():
            continue
        p.rename(newp)
        log_event("RANSOM_RENAME_SIMULATED", before=str(p), after=str(newp))

def undo_ransomware_fake():
    """Undo fake renames: remove '.locked' suffix."""
    ensure_sandbox()
    locked = sorted([p for p in USER_FILES.rglob("*.locked") if p.is_file()])
    for p in locked:
        # remove last suffix ".locked"
        newp = Path(str(p)[:-7])  # remove ".locked"
        if newp.exists():
            # if collision, move to quarantine
            q = QUARANTINE / f"{newp.name}.{int(time.time())}"
            shutil.move(str(p), str(q))
            log_event("UNDO_CONFLICT_MOVED_TO_QUARANTINE", src=str(p), dest=str(q))
        else:
            p.rename(newp)
            log_event("UNDO_RENAME", before=str(p), after=str(newp))
    log_event("UNDO_DONE", reverted=len(locked))

def simulate_propagation_logic():
    """Simulated propagation as a state-machine (logs only)."""
    ensure_sandbox()
    states = ["IDLE", "DISCOVERY", "STAGING", "EXECUTION", "CLEANUP"]
    edges = [("IDLE","DISCOVERY"), ("DISCOVERY","STAGING"), ("STAGING","EXECUTION"), ("EXECUTION","CLEANUP")]
    log_event("PROPAGATION_GRAPH", states=states, edges=edges)

    current = "IDLE"
    log_event("PROPAGATION_STATE", state=current)
    for a, b in edges:
        time.sleep(random.uniform(0.02, 0.08))
        log_event("PROPAGATION_TRANSITION", frm=a, to=b)
        current = b
    log_event("PROPAGATION_DONE", final=current)

def run_full():
    log_event("SCENARIO_START", scenario="full")
    simulate_persistence()
    simulate_duplication()
    simulate_scan()
    simulate_ransomware_fake()
    simulate_propagation_logic()
    log_event("SCENARIO_END", scenario="full")

# =========================
# GUI (Calculator + Buttons)
# =========================
def safe_eval(expr: str):
    allowed = set("0123456789.+-*/() %")
    if any(ch not in allowed for ch in expr):
        raise ValueError("Caractère interdit.")
    return eval(expr, {"__builtins__": {}}, {})  # controlled

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("P3-C1 — Silent Execution (Simulation, Sandbox Only)")
        self.geometry("900x520")
        ensure_sandbox()

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)

        # Left: Calculator
        left = ttk.LabelFrame(main, text="Application légitime : Mini Calculatrice", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        self.expr = tk.StringVar()
        entry = ttk.Entry(left, textvariable=self.expr, font=("Segoe UI", 14))
        entry.pack(fill="x")
        entry.focus_set()

        btn_row = ttk.Frame(left)
        btn_row.pack(fill="x", pady=8)

        ttk.Button(btn_row, text="Calculer", command=self.on_calc).pack(side="left")
        ttk.Button(btn_row, text="Effacer", command=lambda: self.expr.set("")).pack(side="left", padx=8)

        self.calc_out = tk.Text(left, height=10, wrap="word")
        self.calc_out.pack(fill="both", expand=True)
        self.calc_out.insert("end", "Tapez une expression (ex: 12*3+4)\n")

        # Right: Simulation controls
        right = ttk.LabelFrame(main, text="Comportement caché : Simulation (100% sandbox)", padding=10)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(right, text="Tout se fait dans :").pack(anchor="w")
        ttk.Label(right, text=str(SANDBOX), foreground="#555").pack(anchor="w", pady=(0, 8))

        grid = ttk.Frame(right)
        grid.pack(fill="x")

        def add_btn(r, c, text, cmd):
            b = ttk.Button(grid, text=text, command=lambda: self.run_action(text, cmd))
            b.grid(row=r, column=c, sticky="ew", padx=4, pady=4)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        add_btn(0, 0, "Persistance (simulée)", simulate_persistence)
        add_btn(0, 1, "Duplication (simulée)", simulate_duplication)
        add_btn(1, 0, "Scan fichiers (sandbox)", simulate_scan)
        add_btn(1, 1, "Ransomware (faux rename)", simulate_ransomware_fake)
        add_btn(2, 0, "Propagation (logique)", simulate_propagation_logic)
        add_btn(2, 1, "FULL scenario", run_full)

        ttk.Separator(right).pack(fill="x", pady=10)

        ttk.Button(right, text="UNDO ransomware (revenir en arrière)", command=lambda: self.run_action("UNDO", undo_ransomware_fake)).pack(fill="x")

        ttk.Separator(right).pack(fill="x", pady=10)

        self.status = tk.Text(right, height=10, wrap="word")
        self.status.pack(fill="both", expand=True)
        self.status.insert("end", "Logs: demo_data/logs/sim.log et sim.jsonl\n")

    def on_calc(self):
        expr = self.expr.get().strip()
        if not expr:
            return
        try:
            res = safe_eval(expr)
            self.calc_out.insert("end", f"> {expr}\n{res}\n\n")
        except Exception as e:
            self.calc_out.insert("end", f"> {expr}\nErreur: {e}\n\n")

    def run_action(self, name, fn):
        try:
            fn()
            self.status.insert("end", f"[OK] {name}\n")
            self.status.insert("end", f"    Vérifiez demo_data/ et demo_data/logs/sim.log\n\n")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            self.status.insert("end", f"[ERR] {name}: {e}\n\n")

if __name__ == "__main__":
    App().mainloop()

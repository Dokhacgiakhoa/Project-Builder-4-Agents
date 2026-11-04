#!/usr/bin/env python3
"""
UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE AUDITOR GUI
Windows 11 AI-Agent Dark Interface (Ultra-Crisp Per-Monitor High-DPI, Immersive Dark Titlebar, Offline & Portable)
"""

import os
import sys
import threading
import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------------------------------------------------------------------
# 0. Windows 11 High-DPI & DWM Immersive Dark Mode Pre-flight Initialization
# ---------------------------------------------------------------------------
try:
    # 2 = PROCESS_PER_MONITOR_DPI_AWARE (Ultra-crisp retinal resolution on Windows 10/11)
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Add script directory to sys.path to import ProjectAuditor
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from project_auditor import ProjectAuditor
except ImportError:
    from scripts.project_auditor import ProjectAuditor


class ProjectAuditorGUI:
    # Windows Agent Deep Dark Palette (GitHub Dark / Windows Copilot Theme)
    C_BG = "#090d16"             # Deep obsidian background
    C_SURFACE = "#111827"        # Elevated card surface
    C_SURFACE_HOVER = "#1f293d"  # Card hover surface
    C_BORDER = "#1f2937"         # Clean 1px border
    C_BORDER_FOCUS = "#38bdf8"   # Focus border (Sky Blue)
    
    C_TEXT = "#f9fafb"           # Bright white title
    C_TEXT_MUTED = "#9ca3af"     # Secondary text
    C_TEXT_DIM = "#6b7280"       # Muted placeholders
    
    C_TERMINAL_BG = "#040711"    # Dark console background
    C_INPUT_BG = "#0b1120"       # Text input background
    
    # AI Agent Neon Accents
    C_EMERALD = "#10b981"        # Neon Emerald (Pass / Online)
    C_EMERALD_BG = "#064e3b"     # Emerald badge background
    C_CYAN = "#06b6d4"           # Cyan accent
    C_SKY = "#0ea5e9"            # Fluent Sky Blue
    C_ROSE = "#f43f5e"           # Gap / Deficit Red
    C_ROSE_BG = "#4c0519"        # Rose badge background
    C_AMBER = "#f59e0b"          # Warning Amber
    C_AMBER_BG = "#78350f"       # Amber badge background

    def __init__(self, root):
        self.root = root
        self.root.title("Project Review Agent • AI-Native Architecture Auditor")
        self.root.geometry("700x700")
        self.root.minsize(650, 640)
        self.root.configure(bg=self.C_BG)

        # Apply Windows 11 Immersive Dark Titlebar & Smooth Corners
        self.apply_win11_dwm_dark_mode()

        # Set Window Icon
        self.set_app_icon()

        # Auditor state
        self.auditor = None
        self.is_running = False
        self.report_path = None

        # Center window on screen
        self.center_window(700, 700)

        # Build UI Components
        self.create_widgets()

    def apply_win11_dwm_dark_mode(self):
        """Forces Windows 11 DWM to render native dark titlebar and rounded corners."""
        try:
            self.root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id()) or self.root.winfo_id()
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            dark_val = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 20, ctypes.byref(dark_val), ctypes.sizeof(dark_val)
            )
            # DWMWA_WINDOW_CORNER_PREFERENCE = 33 (2 = DWMWCP_ROUND)
            round_val = ctypes.c_int(2)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 33, ctypes.byref(round_val), ctypes.sizeof(round_val)
            )
        except Exception:
            pass

    def set_app_icon(self):
        possible_icon_paths = [
            Path(sys.executable).resolve().parent / "assets" / "app-icon.ico" if getattr(sys, 'frozen', False) else None,
            Path(__file__).resolve().parent.parent / "assets" / "app-icon.ico",
            Path.cwd() / "assets" / "app-icon.ico",
        ]
        for p in possible_icon_paths:
            if p and p.exists():
                try:
                    self.root.iconbitmap(str(p))
                    break
                except Exception:
                    pass

    def center_window(self, width, height):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width // 2) - (width // 2))
        y = max(0, (screen_height // 2) - (height // 2) - 20)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # -------------------------------------------------------------
        # 1. Agent Header Banner
        # -------------------------------------------------------------
        header = tk.Frame(self.root, bg=self.C_SURFACE, padx=20, pady=16, highlightthickness=1, highlightbackground=self.C_BORDER)
        header.pack(fill=tk.X, padx=16, pady=(16, 12))

        top_row = tk.Frame(header, bg=self.C_SURFACE)
        top_row.pack(fill=tk.X)

        # Agent Status Dot + Title
        title_group = tk.Frame(top_row, bg=self.C_SURFACE)
        title_group.pack(side=tk.LEFT)

        self.agent_dot = tk.Label(
            title_group,
            text="●",
            font=("Segoe UI", 12),
            fg=self.C_EMERALD,
            bg=self.C_SURFACE
        )
        self.agent_dot.pack(side=tk.LEFT, padx=(0, 6))

        title_lbl = tk.Label(
            title_group,
            text="PROJECT REVIEW AGENT",
            font=("Segoe UI Variable Display", 13, "bold"),
            fg=self.C_TEXT,
            bg=self.C_SURFACE
        )
        title_lbl.pack(side=tk.LEFT)

        # Agent Badge
        badge = tk.Label(
            top_row,
            text=" AI-NATIVE 2.0 • OFFLINE ",
            font=("Segoe UI Variable Text", 8, "bold"),
            fg=self.C_EMERALD,
            bg=self.C_EMERALD_BG,
            padx=8,
            pady=3
        )
        badge.pack(side=tk.RIGHT)

        sub_lbl = tk.Label(
            header,
            text="Autonomous Architecture Governance & System Design Audit Engine",
            font=("Segoe UI Variable Text", 9),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE
        )
        sub_lbl.pack(anchor="w", pady=(4, 0))

        # -------------------------------------------------------------
        # 2. Main Content Body
        # -------------------------------------------------------------
        body = tk.Frame(self.root, bg=self.C_BG, padx=16)
        body.pack(fill=tk.BOTH, expand=True)

        # --- Target Scope Card ---
        dir_card = tk.Frame(body, bg=self.C_SURFACE, padx=14, pady=12, highlightthickness=1, highlightbackground=self.C_BORDER)
        dir_card.pack(fill=tk.X, pady=(0, 10))

        dir_lbl = tk.Label(
            dir_card,
            text="TARGET REPOSITORY PATH",
            font=("Segoe UI Variable Text", 8, "bold"),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE
        )
        dir_lbl.pack(anchor="w", pady=(0, 6))

        dir_input_row = tk.Frame(dir_card, bg=self.C_SURFACE)
        dir_input_row.pack(fill=tk.X)

        default_path = str(Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path.cwd())
        self.path_var = tk.StringVar(value=default_path)

        self.path_entry = tk.Entry(
            dir_input_row,
            textvariable=self.path_var,
            font=("Cascadia Code", 9),
            bg=self.C_INPUT_BG,
            fg=self.C_TEXT,
            insertbackground=self.C_EMERALD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#374151",
            highlightcolor=self.C_EMERALD
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))

        browse_btn = tk.Button(
            dir_input_row,
            text=" Browse... ",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#1f2937",
            fg=self.C_TEXT,
            activebackground="#374151",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=4,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground="#4b5563",
            command=self.browse_directory
        )
        browse_btn.pack(side=tk.RIGHT)

        # --- Primary Action CTA (Agent Execution Button) ---
        self.start_btn = tk.Button(
            body,
            text="⚡  RUN ARCHITECTURE AUDIT",
            font=("Segoe UI Variable Display", 10, "bold"),
            bg=self.C_EMERALD,
            fg="#022c22",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            pady=10,
            cursor="hand2",
            command=self.start_audit_thread
        )
        self.start_btn.pack(fill=tk.X, pady=(0, 10))

        # --- Progress Bar (Sleek Neon Accent Bar) ---
        prog_frame = tk.Frame(body, bg=self.C_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=self.C_BORDER)
        prog_frame.pack(fill=tk.X, pady=(0, 10))

        self.progress_canvas = tk.Canvas(prog_frame, height=8, bg=self.C_TERMINAL_BG, highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 8, fill=self.C_EMERALD, width=0)

        self.status_var = tk.StringVar(value="Agent ready. Press 'RUN ARCHITECTURE AUDIT' to inspect against Starter Kit standards.")
        status_lbl = tk.Label(
            prog_frame,
            textvariable=self.status_var,
            font=("Segoe UI Variable Text", 8),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE,
            anchor="w"
        )
        status_lbl.pack(fill=tk.X, pady=(6, 0))

        # --- Telemetry Metric Grid (3 Cards) ---
        grid_frame = tk.Frame(body, bg=self.C_BG)
        grid_frame.pack(fill=tk.X, pady=(0, 10))
        grid_frame.columnconfigure((0, 1, 2), weight=1, uniform="metric")

        # Metric 1: Total Score
        m1 = tk.Frame(grid_frame, bg=self.C_SURFACE, padx=12, pady=8, highlightthickness=1, highlightbackground=self.C_BORDER)
        m1.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        tk.Label(m1, text="COMPLIANCE SCORE", font=("Segoe UI Variable Text", 8, "bold"), fg=self.C_TEXT_DIM, bg=self.C_SURFACE).pack(anchor="w")
        self.score_val_lbl = tk.Label(m1, text="-- / 100", font=("Segoe UI Variable Display", 13, "bold"), fg=self.C_TEXT, bg=self.C_SURFACE)
        self.score_val_lbl.pack(anchor="w", pady=(2, 0))

        # Metric 2: Grade Pill
        m2 = tk.Frame(grid_frame, bg=self.C_SURFACE, padx=12, pady=8, highlightthickness=1, highlightbackground=self.C_BORDER)
        m2.grid(row=0, column=1, sticky="nsew", padx=5)
        tk.Label(m2, text="ARCH RATING", font=("Segoe UI Variable Text", 8, "bold"), fg=self.C_TEXT_DIM, bg=self.C_SURFACE).pack(anchor="w")
        self.grade_val_lbl = tk.Label(m2, text="PENDING", font=("Segoe UI Variable Display", 13, "bold"), fg=self.C_TEXT_MUTED, bg=self.C_SURFACE)
        self.grade_val_lbl.pack(anchor="w", pady=(2, 0))

        # Metric 3: Pillars Checked
        m3 = tk.Frame(grid_frame, bg=self.C_SURFACE, padx=12, pady=8, highlightthickness=1, highlightbackground=self.C_BORDER)
        m3.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        tk.Label(m3, text="GOVERNANCE SCOPE", font=("Segoe UI Variable Text", 8, "bold"), fg=self.C_TEXT_DIM, bg=self.C_SURFACE).pack(anchor="w")
        self.scope_val_lbl = tk.Label(m3, text="7 Pillars Ready", font=("Segoe UI Variable Display", 11, "bold"), fg=self.C_CYAN, bg=self.C_SURFACE)
        self.scope_val_lbl.pack(anchor="w", pady=(4, 0))

        # --- Agent Console Output (Terminal View) ---
        console_frame = tk.Frame(body, bg=self.C_TERMINAL_BG, highlightthickness=1, highlightbackground=self.C_BORDER)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        console_title_bar = tk.Frame(console_frame, bg="#0d1526", padx=10, pady=4)
        console_title_bar.pack(fill=tk.X)
        tk.Label(
            console_title_bar,
            text="AGENT DIAGNOSTICS & TELEMETRY",
            font=("Segoe UI Variable Text", 8, "bold"),
            fg=self.C_TEXT_MUTED,
            bg="#0d1526"
        ).pack(side=tk.LEFT)

        self.details_box = tk.Text(
            console_frame,
            height=7,
            font=("Cascadia Code", 9),
            bg=self.C_TERMINAL_BG,
            fg="#cbd5e1",
            relief=tk.FLAT,
            padx=12,
            pady=8,
            insertbackground=self.C_EMERALD
        )
        self.details_box.pack(fill=tk.BOTH, expand=True)
        self.details_box.insert(tk.END, "Agent initialized. Standing by to benchmark repository against Starter Kit.\n")
        self.details_box.config(state=tk.DISABLED)

        # Report path notification
        self.report_notice_var = tk.StringVar(value="Report output: PROJECT_REVIEW_REPORT.md will be generated in repository root.")
        report_lbl = tk.Label(
            body,
            textvariable=self.report_notice_var,
            font=("Segoe UI Variable Text", 8),
            fg=self.C_EMERALD,
            bg=self.C_BG,
            anchor="w"
        )
        report_lbl.pack(fill=tk.X, pady=(0, 10))

        # -------------------------------------------------------------
        # 3. Action Footer Bar
        # -------------------------------------------------------------
        footer = tk.Frame(self.root, bg=self.C_BG, padx=16, pady=8)
        footer.pack(fill=tk.X, pady=(0, 12))

        self.open_report_btn = tk.Button(
            footer,
            text="📄 Open Report",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#1e293b",
            fg=self.C_TEXT_MUTED,
            activebackground="#334155",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            highlightthickness=1,
            highlightbackground="#334155",
            state=tk.DISABLED,
            command=self.open_report_file
        )
        self.open_report_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.open_folder_btn = tk.Button(
            footer,
            text="📁 Show in Folder",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#1e293b",
            fg=self.C_TEXT_MUTED,
            activebackground="#334155",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            highlightthickness=1,
            highlightbackground="#334155",
            state=tk.DISABLED,
            command=self.open_report_folder
        )
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.copy_prompt_btn = tk.Button(
            footer,
            text="🤖 Copy AI Agent Prompt",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            state=tk.DISABLED,
            command=self.copy_ai_prompt
        )
        self.copy_prompt_btn.pack(side=tk.LEFT, padx=(0, 8))

        close_btn = tk.Button(
            footer,
            text="Close",
            font=("Segoe UI Variable Text", 9),
            bg=self.C_BG,
            fg=self.C_TEXT_MUTED,
            activebackground="#1e293b",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            command=self.root.destroy
        )
        close_btn.pack(side=tk.RIGHT)

    def browse_directory(self):
        chosen = filedialog.askdirectory(
            initialdir=self.path_var.get(),
            title="Select target repository folder to audit"
        )
        if chosen:
            self.path_var.set(os.path.normpath(chosen))

    def update_progress(self, percent, message):
        def _do_update():
            total_w = self.progress_canvas.winfo_width()
            fill_w = int((percent / 100.0) * total_w)
            self.progress_canvas.coords(self.progress_rect, 0, 0, fill_w, 8)
            self.status_var.set(f"[{percent}%] {message}")
        self.root.after(0, _do_update)

    def start_audit_thread(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not Path(target_dir).is_dir():
            messagebox.showerror(
                "Invalid Directory",
                "The selected target repository path does not exist!\nPlease browse and select a valid directory."
            )
            return

        if self.is_running:
            return

        self.is_running = True
        self.agent_dot.config(fg=self.C_AMBER)
        self.start_btn.config(state=tk.DISABLED, text="⏳  AUDITING REPOSITORY...", bg="#334155", fg="#94a3b8")
        self.open_report_btn.config(state=tk.DISABLED, fg="#94a3b8")
        self.open_folder_btn.config(state=tk.DISABLED, fg="#94a3b8")
        self.copy_prompt_btn.config(state=tk.DISABLED)
        self.progress_canvas.coords(self.progress_rect, 0, 0, 0, 8)

        worker = threading.Thread(target=self._run_audit_worker, args=(target_dir,), daemon=True)
        worker.start()

    def _run_audit_worker(self, target_dir):
        try:
            self.auditor = ProjectAuditor(target_dir)
            total_score = self.auditor.run(progress_callback=self.update_progress)
            self.report_path = self.auditor.report_path
            self.root.after(0, self._on_audit_finished, total_score)
        except Exception as e:
            self.root.after(0, self._on_audit_error, str(e))

    def _on_audit_finished(self, total_score):
        self.is_running = False
        self.agent_dot.config(fg=self.C_EMERALD)
        self.start_btn.config(state=tk.NORMAL, text="🔄  RUN NEW AUDIT SCAN", bg=self.C_EMERALD, fg="#022c22")
        self.open_report_btn.config(state=tk.NORMAL, fg=self.C_TEXT)
        self.open_folder_btn.config(state=tk.NORMAL, fg=self.C_TEXT)
        self.copy_prompt_btn.config(state=tk.NORMAL)

        grade = self.auditor.get_letter_grade(total_score)
        
        # Color coding for total score
        if total_score >= 85:
            score_fg = self.C_EMERALD
            grade_fg = self.C_EMERALD
        elif total_score >= 60:
            score_fg = self.C_AMBER
            grade_fg = self.C_AMBER
        else:
            score_fg = self.C_ROSE
            grade_fg = self.C_ROSE

        self.score_val_lbl.config(
            text=f"{total_score} / 100",
            fg=score_fg
        )
        self.grade_val_lbl.config(
            text=f"GRADE {grade.split()[0]}",
            fg=grade_fg
        )
        self.scope_val_lbl.config(
            text=f"{len(self.auditor.scores)} Pillars Verified",
            fg=self.C_CYAN
        )

        details_text = []
        details_text.append("════════════════════════════════════════════════════════════════════")
        details_text.append("  BENCHMARK AUDIT RESULTS (COMPLIANCE BREAKDOWN)")
        details_text.append("════════════════════════════════════════════════════════════════════\n")
        
        for pillar, score in self.auditor.scores.items():
            bar = "█" * (score // 10) + "░" * (10 - (score // 10))
            status_tag = "✔ PASS" if score >= 70 else ("⚠️ DEFICIT" if score > 0 else "✖ MISSING")
            details_text.append(f"  • {pillar:<30} [{bar}] {score:>3}%  {status_tag}")

        if self.auditor.innovations:
            details_text.append("\n🌟 ADVANCED INNOVATIONS DETECTED:")
            for item in self.auditor.innovations:
                details_text.append(f"    ✔ {item}")

        if self.auditor.gaps:
            details_text.append("\n⚠️ ARCHITECTURAL GAPS REQUIRING ATTENTION:")
            for gap in self.auditor.gaps:
                details_text.append(f"    ✖ {gap}")

        self.details_box.config(state=tk.NORMAL)
        self.details_box.delete("1.0", tk.END)
        self.details_box.insert(tk.END, "\n".join(details_text))
        self.details_box.config(state=tk.DISABLED)

        if self.report_path:
            self.report_notice_var.set(f"✔ Audit report generated: {self.report_path.resolve()}")

    def _on_audit_error(self, err_msg):
        self.is_running = False
        self.agent_dot.config(fg=self.C_ROSE)
        self.start_btn.config(state=tk.NORMAL, text="⚡  RUN ARCHITECTURE AUDIT", bg=self.C_EMERALD, fg="#022c22")
        messagebox.showerror("Audit Error", f"An error occurred while auditing the project:\n{err_msg}")

    def open_report_file(self):
        if self.report_path and self.report_path.exists():
            try:
                os.startfile(str(self.report_path.resolve()))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open report file: {e}")
        else:
            messagebox.showwarning("Warning", "Report file not found yet!")

    def open_report_folder(self):
        target_dir = self.path_var.get().strip()
        if target_dir and Path(target_dir).is_dir():
            try:
                os.startfile(target_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open directory: {e}")

    def copy_ai_prompt(self):
        if self.auditor:
            prompt_text = self.auditor.get_ai_prompt()
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt_text)
            messagebox.showinfo(
                "Prompt Copied!",
                "AI Agent Prompt has been copied to Clipboard!\n\n"
                "👉 Open your AI Coding Agent session (Claude Code, Cursor, Antigravity) "
                "and paste (Ctrl+V) to start automated refactoring based on the audit report."
            )


def main():
    if len(sys.argv) > 1 and sys.argv[1] not in ('--gui',):
        target = Path(sys.argv[1]).resolve()
        if target.is_dir():
            auditor = ProjectAuditor(target)
            score = auditor.run()
            sys.exit(0 if score >= 70 else 1)

    root = tk.Tk()
    app = ProjectAuditorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

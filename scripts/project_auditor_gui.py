#!/usr/bin/env python3
"""
UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE REVIEWER GUI
True Dark UI (Antigravity Style, Pro-Max Cyan/Emerald Gradient, Rule-Based Engine, Offline & Portable)
"""

import os
import sys
import threading
import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

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
    # Antigravity Pure Jet Dark Palette
    C_BG = "#0e0e10"             # Pure neutral dark background (No blue tint)
    C_SURFACE = "#18181b"        # Card panel surface (Zinc 900)
    C_SURFACE_HOVER = "#27272a"  # Card hover surface
    C_BORDER = "#27272a"         # Subtle 1px border
    C_BORDER_FOCUS = "#3f3f46"   # Active border
    
    C_TEXT = "#ffffff"           # High contrast pure white
    C_TEXT_MUTED = "#a1a1aa"     # Neutral gray (Zinc 400)
    C_TEXT_DIM = "#71717a"       # Dim gray (Zinc 500)
    
    C_CONSOLE_BG = "#111113"     # Terminal console background
    C_INPUT_BG = "#111113"       # Text input background
    
    # Status Colors
    C_EMERALD = "#10b981"        # Neon Emerald
    C_EMERALD_BG = "#064e3b"     # Emerald badge background
    C_CYAN = "#06b6d4"           # Cyan accent
    C_ROSE = "#f43f5e"           # Deficit Red
    C_ROSE_BG = "#4c0519"        # Rose badge background
    C_AMBER = "#f59e0b"          # Warning Amber
    C_AMBER_BG = "#78350f"       # Amber badge background

    def __init__(self, root):
        self.root = root
        self.root.title("Project Architecture Reviewer • Rule-Based Auditor")
        self.root.geometry("690x710")
        self.root.minsize(640, 640)
        self.root.configure(bg=self.C_BG)

        # Apply Windows 11 Immersive Dark Titlebar & Smooth Corners
        self.apply_win11_dwm_dark_mode()

        # Set Window Icon
        self.set_app_icon()

        # Auditor state
        self.auditor = None
        self.is_running = False
        self.report_path = None
        self.btn_images = {}

        # Center window on screen
        self.center_window(690, 710)

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

    def make_gradient_pill(self, w, h, r, text, font_size=10, state="normal"):
        """Generates a super-sampled antialiased Cyan-to-Emerald gradient button."""
        scale = 2
        w2, h2, r2 = w * scale, h * scale, r * scale
        canvas = Image.new('RGBA', (w2, h2), (0, 0, 0, 0))

        if state == "disabled":
            stops = [(0.0, (39, 39, 42)), (1.0, (39, 39, 42))]
            text_color = (113, 113, 122, 255)
        elif state == "hover":
            stops = [
                (0.0, (34, 211, 238)),  # Cyan 400
                (0.35, (45, 212, 191)), # Teal 400
                (0.70, (52, 211, 153)), # Emerald 400
                (1.0, (110, 231, 183))  # Mint 300
            ]
            text_color = (2, 44, 34, 255)
        else:
            stops = [
                (0.0, (6, 182, 212)),   # Cyan 500
                (0.35, (20, 184, 166)),  # Teal 500
                (0.70, (16, 185, 129)),  # Emerald 500
                (1.0, (52, 211, 153))   # Emerald 400
            ]
            text_color = (2, 44, 34, 255)

        def interpolate_color(t):
            if t <= stops[0][0]:
                return stops[0][1]
            if t >= stops[-1][0]:
                return stops[-1][1]
            for i in range(len(stops) - 1):
                t0, c0 = stops[i]
                t1, c1 = stops[i + 1]
                if t0 <= t <= t1:
                    factor = (t - t0) / float(t1 - t0)
                    return (
                        int(c0[0] + (c1[0] - c0[0]) * factor),
                        int(c0[1] + (c1[1] - c0[1]) * factor),
                        int(c0[2] + (c1[2] - c0[2]) * factor),
                    )
            return stops[-1][1]

        line_img = Image.new('RGB', (w2, 1))
        line_pixels = [interpolate_color(x / float(w2 - 1)) for x in range(w2)]
        line_img.putdata(line_pixels)
        grad_img = line_img.resize((w2, h2), Image.Resampling.NEAREST)

        mask = Image.new('L', (w2, h2), 0)
        d_mask = ImageDraw.Draw(mask)
        d_mask.rounded_rectangle([0, 0, w2 - 1, h2 - 1], radius=r2, fill=255)
        canvas.paste(grad_img, (0, 0), mask)

        draw = ImageDraw.Draw(canvas)
        font_path = "segoeuib.ttf" if os.name == 'nt' else None
        try:
            font = ImageFont.truetype(font_path, font_size * scale)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = (w2 - tw) // 2
        ty = (h2 - th) // 2 - 2
        draw.text((tx, ty), text, fill=text_color, font=font)

        resized = canvas.resize((w, h), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized)

    def create_widgets(self):
        # -------------------------------------------------------------
        # 0. Top Accent Gradient Line (Pro Max UI Detail)
        # -------------------------------------------------------------
        top_accent = tk.Canvas(self.root, height=3, bg=self.C_BG, highlightthickness=0)
        top_accent.pack(fill=tk.X)
        self.root.update_idletasks()
        win_w = 690
        for i in range(win_w):
            t = i / float(win_w)
            r = int(6 + (52 - 6) * t)
            g = int(182 + (211 - 182) * t)
            b = int(212 + (153 - 212) * t)
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            top_accent.create_line(i, 0, i, 3, fill=color_hex)

        # -------------------------------------------------------------
        # 1. Header Banner
        # -------------------------------------------------------------
        header = tk.Frame(self.root, bg=self.C_SURFACE, padx=20, pady=14, highlightthickness=1, highlightbackground=self.C_BORDER)
        header.pack(fill=tk.X, padx=16, pady=(12, 10))

        top_row = tk.Frame(header, bg=self.C_SURFACE)
        top_row.pack(fill=tk.X)

        title_group = tk.Frame(top_row, bg=self.C_SURFACE)
        title_group.pack(side=tk.LEFT)

        self.status_dot = tk.Label(
            title_group,
            text="●",
            font=("Segoe UI", 12),
            fg=self.C_EMERALD,
            bg=self.C_SURFACE
        )
        self.status_dot.pack(side=tk.LEFT, padx=(0, 6))

        title_lbl = tk.Label(
            title_group,
            text="PROJECT ARCHITECTURE REVIEWER",
            font=("Segoe UI Variable Display", 13, "bold"),
            fg=self.C_TEXT,
            bg=self.C_SURFACE
        )
        title_lbl.pack(side=tk.LEFT)

        badge = tk.Label(
            top_row,
            text=" RULE-BASED • OFFLINE 100% ",
            font=("Segoe UI Variable Text", 8, "bold"),
            fg=self.C_EMERALD,
            bg=self.C_EMERALD_BG,
            padx=8,
            pady=3
        )
        badge.pack(side=tk.RIGHT)

        sub_lbl = tk.Label(
            header,
            text="Kiểm toán kiến trúc đối chiếu chuẩn Clean Architecture & System Design Starter Kit",
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
        dir_card = tk.Frame(body, bg=self.C_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=self.C_BORDER)
        dir_card.pack(fill=tk.X, pady=(0, 10))

        dir_lbl = tk.Label(
            dir_card,
            text="THƯ MỤC DỰ ÁN CẦN KIỂM TOÁN",
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
            highlightbackground="#27272a",
            highlightcolor=self.C_EMERALD
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 8))

        browse_btn = tk.Button(
            dir_input_row,
            text=" Duyệt... ",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#27272a",
            fg=self.C_TEXT,
            activebackground="#3f3f46",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=4,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground="#3f3f46",
            command=self.browse_directory
        )
        browse_btn.pack(side=tk.RIGHT)

        # --- Primary Action CTA (Pro-Max Gradient Button) ---
        self.btn_w = 654
        self.btn_h = 42
        self.img_btn_normal = self.make_gradient_pill(self.btn_w, self.btn_h, 8, "⚡  BẮT ĐẦU KIỂM TOÁN KIẾN TRÚC", font_size=10, state="normal")
        self.img_btn_hover = self.make_gradient_pill(self.btn_w, self.btn_h, 8, "⚡  BẮT ĐẦU KIỂM TOÁN KIẾN TRÚC", font_size=10, state="hover")
        self.img_btn_disabled = self.make_gradient_pill(self.btn_w, self.btn_h, 8, "⏳  ĐANG KIỂM TOÁN KIẾN TRÚC...", font_size=10, state="disabled")
        self.img_btn_again = self.make_gradient_pill(self.btn_w, self.btn_h, 8, "🔄  QUÉT LẠI / QUÉT TIẾP", font_size=10, state="normal")
        self.img_btn_again_hover = self.make_gradient_pill(self.btn_w, self.btn_h, 8, "🔄  QUÉT LẠI / QUÉT TIẾP", font_size=10, state="hover")

        self.start_btn = tk.Label(
            body,
            image=self.img_btn_normal,
            bg=self.C_BG,
            cursor="hand2"
        )
        self.start_btn.pack(fill=tk.X, pady=(0, 10))
        self.start_btn.bind("<Button-1>", lambda e: self.start_audit_thread())
        self.start_btn.bind("<Enter>", lambda e: self._on_btn_hover(True))
        self.start_btn.bind("<Leave>", lambda e: self._on_btn_hover(False))

        # --- Progress Bar (Canvas Based Smooth Gradient Bar) ---
        prog_frame = tk.Frame(body, bg=self.C_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=self.C_BORDER)
        prog_frame.pack(fill=tk.X, pady=(0, 10))

        self.progress_canvas = tk.Canvas(prog_frame, height=8, bg=self.C_CONSOLE_BG, highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 8, fill=self.C_EMERALD, width=0)

        self.status_var = tk.StringVar(value="Sẵn sàng. Nhấn 'BẮT ĐẦU KIỂM TOÁN KIẾN TRÚC' để đối chiếu mã nguồn.")
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
        tk.Label(m1, text="ĐIỂM TUÂN THỦ (SCORE)", font=("Segoe UI Variable Text", 8, "bold"), fg=self.C_TEXT_DIM, bg=self.C_SURFACE).pack(anchor="w")
        self.score_val_lbl = tk.Label(m1, text="-- / 100", font=("Segoe UI Variable Display", 13, "bold"), fg=self.C_TEXT, bg=self.C_SURFACE)
        self.score_val_lbl.pack(anchor="w", pady=(2, 0))

        # Metric 2: Grade Pill
        m2 = tk.Frame(grid_frame, bg=self.C_SURFACE, padx=12, pady=8, highlightthickness=1, highlightbackground=self.C_BORDER)
        m2.grid(row=0, column=1, sticky="nsew", padx=5)
        tk.Label(m2, text="XẾP HẠNG KIẾN TRÚC", font=("Segoe UI Variable Text", 8, "bold"), fg=self.C_TEXT_DIM, bg=self.C_SURFACE).pack(anchor="w")
        self.grade_val_lbl = tk.Label(m2, text="CHƯA QUÉT", font=("Segoe UI Variable Display", 13, "bold"), fg=self.C_TEXT_MUTED, bg=self.C_SURFACE)
        self.grade_val_lbl.pack(anchor="w", pady=(2, 0))

        # Metric 3: Pillars Checked
        m3 = tk.Frame(grid_frame, bg=self.C_SURFACE, padx=12, pady=8, highlightthickness=1, highlightbackground=self.C_BORDER)
        m3.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        tk.Label(m3, text="PHẠM VI ĐỐI CHIẾU", font=("Segoe UI Variable Text", 8, "bold"), fg=self.C_TEXT_DIM, bg=self.C_SURFACE).pack(anchor="w")
        self.scope_val_lbl = tk.Label(m3, text="7 Trụ Cột Starter Kit", font=("Segoe UI Variable Display", 11, "bold"), fg=self.C_CYAN, bg=self.C_SURFACE)
        self.scope_val_lbl.pack(anchor="w", pady=(4, 0))

        # --- Console Output (Terminal View) ---
        console_frame = tk.Frame(body, bg=self.C_CONSOLE_BG, highlightthickness=1, highlightbackground=self.C_BORDER)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        console_title_bar = tk.Frame(console_frame, bg="#18181b", padx=10, pady=4)
        console_title_bar.pack(fill=tk.X)
        tk.Label(
            console_title_bar,
            text="NHẬT KÝ KIỂM TOÁN KIẾN TRÚC (AUDIT LOG)",
            font=("Segoe UI Variable Text", 8, "bold"),
            fg=self.C_TEXT_MUTED,
            bg="#18181b"
        ).pack(side=tk.LEFT)

        self.details_box = tk.Text(
            console_frame,
            height=7,
            font=("Cascadia Code", 9),
            bg=self.C_CONSOLE_BG,
            fg="#e4e4e7",
            relief=tk.FLAT,
            padx=12,
            pady=8,
            insertbackground=self.C_EMERALD
        )
        self.details_box.pack(fill=tk.BOTH, expand=True)
        self.details_box.insert(tk.END, "Hệ thống kiểm toán sẵn sàng. Bấm nút phía trên để bắt đầu đối chiếu mã nguồn.\n")
        self.details_box.config(state=tk.DISABLED)

        # Report path notification
        self.report_notice_var = tk.StringVar(value="Báo cáo: PROJECT_REVIEW_REPORT.md sẽ được tạo tại thư mục dự án.")
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
            text="📄 Mở Báo Cáo",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#18181b",
            fg=self.C_TEXT_MUTED,
            activebackground="#27272a",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            highlightthickness=1,
            highlightbackground="#27272a",
            state=tk.DISABLED,
            command=self.open_report_file
        )
        self.open_report_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.open_folder_btn = tk.Button(
            footer,
            text="📁 Mở Thư Mục Báo Cáo",
            font=("Segoe UI Variable Text", 9, "bold"),
            bg="#18181b",
            fg=self.C_TEXT_MUTED,
            activebackground="#27272a",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6,
            highlightthickness=1,
            highlightbackground="#27272a",
            state=tk.DISABLED,
            command=self.open_report_folder
        )
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.copy_prompt_btn = tk.Button(
            footer,
            text="📋 Copy Prompt Cho AI",
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
            text="Đóng",
            font=("Segoe UI Variable Text", 9),
            bg=self.C_BG,
            fg=self.C_TEXT_MUTED,
            activebackground="#18181b",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            command=self.root.destroy
        )
        close_btn.pack(side=tk.RIGHT)

    def _on_btn_hover(self, is_hover):
        if self.is_running:
            return
        if self.auditor is not None:
            self.start_btn.config(image=self.img_btn_again_hover if is_hover else self.img_btn_again)
        else:
            self.start_btn.config(image=self.img_btn_hover if is_hover else self.img_btn_normal)

    def browse_directory(self):
        chosen = filedialog.askdirectory(
            initialdir=self.path_var.get(),
            title="Chọn thư mục dự án cần kiểm toán"
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
        if self.is_running:
            return

        target_dir = self.path_var.get().strip()
        if not target_dir or not Path(target_dir).is_dir():
            messagebox.showerror(
                "Lỗi Đường Dẫn",
                "Thư mục dự án không tồn tại!\nVui lòng chọn lại thư mục hợp lệ."
            )
            return

        self.is_running = True
        self.status_dot.config(fg=self.C_AMBER)
        self.start_btn.config(image=self.img_btn_disabled)
        self.open_report_btn.config(state=tk.DISABLED, fg=self.C_TEXT_DIM)
        self.open_folder_btn.config(state=tk.DISABLED, fg=self.C_TEXT_DIM)
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
        self.status_dot.config(fg=self.C_EMERALD)
        self.start_btn.config(image=self.img_btn_again)
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
            text=f"{grade.split()[0]}",
            fg=grade_fg
        )
        self.scope_val_lbl.config(
            text=f"{len(self.auditor.scores)} Trụ Cột Đã Quét",
            fg=self.C_CYAN
        )

        details_text = []
        details_text.append("════════════════════════════════════════════════════════════════════")
        details_text.append("  KẾT QUẢ ĐỐI CHIẾU KIẾN TRÚC (COMPLIANCE AUDIT)")
        details_text.append("════════════════════════════════════════════════════════════════════\n")
        
        for pillar, score in self.auditor.scores.items():
            bar = "█" * (score // 10) + "░" * (10 - (score // 10))
            status_tag = "✔ PASS" if score >= 70 else ("⚠️ DEFICIT" if score > 0 else "✖ MISSING")
            details_text.append(f"  • {pillar:<30} [{bar}] {score:>3}%  {status_tag}")

        if self.auditor.innovations:
            details_text.append("\n🌟 ĐIỂM SÁNG CAO CẤP HƠN STARTER KIT (INNOVATIONS):")
            for item in self.auditor.innovations:
                details_text.append(f"    ✔ {item}")

        if self.auditor.gaps:
            details_text.append("\n⚠️ KHOẢNG TRỐNG KIẾN TRÚC CẦN KHẮC PHỤC (GAPS):")
            for gap in self.auditor.gaps:
                details_text.append(f"    ✖ {gap}")

        self.details_box.config(state=tk.NORMAL)
        self.details_box.delete("1.0", tk.END)
        self.details_box.insert(tk.END, "\n".join(details_text))
        self.details_box.config(state=tk.DISABLED)

        if self.report_path:
            self.report_notice_var.set(f"✔ Đã xuất file báo cáo tại: {self.report_path.resolve()}")

    def _on_audit_error(self, err_msg):
        self.is_running = False
        self.status_dot.config(fg=self.C_ROSE)
        self.start_btn.config(image=self.img_btn_normal)
        messagebox.showerror("Lỗi Kiểm Toán", f"Có lỗi xảy ra trong quá trình quét:\n{err_msg}")

    def open_report_file(self):
        if self.report_path and self.report_path.exists():
            try:
                os.startfile(str(self.report_path.resolve()))
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở file báo cáo: {e}")
        else:
            messagebox.showwarning("Cảnh Báo", "Chưa tìm thấy file báo cáo!")

    def open_report_folder(self):
        target_dir = self.path_var.get().strip()
        if target_dir and Path(target_dir).is_dir():
            try:
                os.startfile(target_dir)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")

    def copy_ai_prompt(self):
        if self.auditor:
            prompt_text = self.auditor.get_ai_prompt()
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt_text)
            messagebox.showinfo(
                "Đã Sao Chép!",
                "Đã sao chép đoạn Prompt cho AI Agent vào Clipboard!\n\n"
                "👉 Bạn chỉ cần mở cửa sổ Chat với AI (Claude Code, Cursor, Antigravity) "
                "và nhấn Ctrl+V để dán nội dung cho AI đọc và sửa code."
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

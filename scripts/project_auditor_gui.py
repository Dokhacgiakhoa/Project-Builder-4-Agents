#!/usr/bin/env python3
"""
UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE BENCHMARK SUITE v3.0
Seamless Modern IDE Architecture • Crystal Diagnostic Engine
Pure Python Standard Library + Tkinter + Pillow (100% Offline, Zero-Dependency)
"""

import os
import sys
import threading
import ctypes
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------------------------------------------------------------------
# 0. Windows High-DPI (Per-Monitor DPI Aware v2)
# ---------------------------------------------------------------------------
if os.name == 'nt':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from project_auditor import ProjectAuditor
except ImportError:
    from scripts.project_auditor import ProjectAuditor


class ProjectAuditorGUI:
    # -------------------------------------------------------------
    # Palette Màu Antigravity IDE (Trích xuất 100% từ pixel ảnh chụp thực tế)
    # -------------------------------------------------------------
    C_BG = "#050507"              # Nền chính đen sâu (Vùng soạn thảo/editor: RGB 5, 5, 7)
    C_SURFACE = "#121116"         # Bề mặt Panel / Topbar / Sidebar (RGB 18, 17, 22)
    C_SURFACE_HOVER = "#1a191f"   # Hover background cho item danh sách (RGB 26, 25, 31)
    C_SURFACE_ACTIVE = "#212026"  # Active/Selected item (RGB 33, 32, 38)
    C_CARD_BG = "#16151b"         # Bề mặt pill button / input (RGB 22, 21, 27)
    C_BORDER = "#26252b"          # Viền phân cách hairline tinh tế (RGB 38, 37, 43)
    C_BORDER_FOCUS = "#38bdf8"    # Điểm nhấn Cyan khi active/focus
    
    C_TEXT = "#ffffff"            # Chữ chính trắng sáng sạch (RGB 255, 255, 255)
    C_TEXT_SUB = "#cccccc"        # Chữ nội dung đọc êm mắt (RGB 204, 204, 204)
    C_TEXT_MUTED = "#85848a"      # Chữ xám Slate phụ (RGB 133, 132, 138)
    C_TEXT_DIM = "#55545a"        # Chữ mờ thứ cấp
    
    # Mã màu trạng thái tiêu chuẩn
    C_CYAN = "#38bdf8"            # Xanh Cyan dịu mắt
    C_SKY = "#0ea5e9"             # Xanh Sky Blue
    C_EMERALD = "#38bdf8"         # Optimal
    C_AMBER = "#fbbf24"           # Warning / Deficit
    C_ROSE = "#f87171"            # Danger / Critical
    C_INPUT_BG = "#16151b"        # Ô nhập liệu

    # Typography Family
    F_FAMILY = "Segoe UI"
    F_CODE_FAMILY = "Consolas"

    MODULE_DEFS = [
        ("readme", "01. Readme & Onboarding", "Tài Liệu & Hướng Dẫn (Readme & Onboarding)", 15, "Khảo sát mục tiêu dự án, tài liệu cấu hình .ENV và các lệnh Quick Start khởi chạy cục bộ."),
        ("backend", "02. Backend & Core Flow", "Kiến Trúc Backend & Luồng Dữ Liệu Core", 20, "Phân tầng kiến trúc, ranh giới Domain, bảo vệ Repository và cơ chế Graceful Shutdown."),
        ("frontend", "03. Frontend & UI/UX", "Kiến Trúc Frontend & Design System (UI/UX)", 20, "Hệ thống Design Tokens, API Client bọc tập trung có Interceptors và phòng ngừa God Components."),
        ("database", "04. Database & Query Safety", "Hạ Tầng Database & An Toàn Query", 15, "Quản lý Database Migrations, cấu hình Connection Pool & Timeout, phòng ngừa SQL Injection."),
        ("anti_crash", "05. Runtime Anti-Crash", "Tiêu Chuẩn An Toàn Runtime (Anti-Crash)", 20, "Bắt lỗi Try-Catch cho JSON.parse/API, chuẩn hóa Strict Typing và bảo mật không rò rỉ Secrets."),
        ("contracts", "06. API Contract & AI Agent", "Quản Trị API Contract & Cấu Hình AI Agent", 10, "Đặc tả OpenAPI/Swagger, hồ sơ Architecture Decision Records (ADRs) và chỉ dẫn AGENTS.MD.")
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Project Architecture Benchmark Suite • Crystal Diagnostic Engine")
        self.root.geometry("1140x800")
        self.root.minsize(1020, 660)
        self.root.configure(bg=self.C_BG)

        self.apply_win11_dwm_dark_mode()
        self.set_app_icon()

        self.auditor = None
        self.is_running = False
        self.report_path = None
        self.active_module_key = "overview"
        self.card_widgets = {}

        self.center_window(1140, 800)
        self.create_widgets()

    def apply_win11_dwm_dark_mode(self):
        try:
            self.root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id()) or self.root.winfo_id()
            dark_val = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark_val), ctypes.sizeof(dark_val))
            round_val = ctypes.c_int(2)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(round_val), ctypes.sizeof(round_val))

            # Ép cứng thanh tiêu đề & viền cửa sổ theo đúng màu #121116 trích xuất từ ảnh Antigravity IDE
            caption_bgr = ctypes.c_int(0x00161112)
            border_bgr = ctypes.c_int(0x00161112)
            text_bgr = ctypes.c_int(0x00ffffff)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption_bgr), ctypes.sizeof(caption_bgr))
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 34, ctypes.byref(border_bgr), ctypes.sizeof(border_bgr))
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 36, ctypes.byref(text_bgr), ctypes.sizeof(text_bgr))
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
        # =============================================================
        # 1. TOPBAR: Tích hợp 1 hàng ngang duy nhất (Unified Command Bar)
        # =============================================================
        topbar = tk.Frame(self.root, bg=self.C_SURFACE, padx=16, pady=8)
        topbar.pack(side=tk.TOP, fill=tk.X)

        # Brand Title (Left)
        brand_group = tk.Frame(topbar, bg=self.C_SURFACE)
        brand_group.pack(side=tk.LEFT)

        self.status_dot = tk.Label(
            brand_group,
            text="●",
            font=(self.F_FAMILY, 9),
            fg=self.C_CYAN,
            bg=self.C_SURFACE
        )
        self.status_dot.pack(side=tk.LEFT, padx=(0, 6))

        title_lbl = tk.Label(
            brand_group,
            text="PROJECT BENCHMARK SUITE",
            font=(self.F_FAMILY, 9, "bold"),
            fg=self.C_TEXT,
            bg=self.C_SURFACE
        )
        title_lbl.pack(side=tk.LEFT)

        # Target Path & Actions (Right)
        actions_group = tk.Frame(topbar, bg=self.C_SURFACE)
        actions_group.pack(side=tk.RIGHT)

        tk.Label(
            actions_group,
            text="Dự án:",
            font=(self.F_FAMILY, 8),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE
        ).pack(side=tk.LEFT, padx=(0, 6))

        default_path = str(Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path.cwd())
        self.path_var = tk.StringVar(value=default_path)

        self.path_entry = tk.Entry(
            actions_group,
            textvariable=self.path_var,
            font=(self.F_CODE_FAMILY, 9),
            bg=self.C_INPUT_BG,
            fg=self.C_TEXT,
            insertbackground=self.C_CYAN,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            highlightcolor=self.C_BORDER_FOCUS,
            width=38
        )
        self.path_entry.pack(side=tk.LEFT, ipady=3, padx=(0, 6))

        browse_btn = tk.Button(
            actions_group,
            text="📁 Duyệt...",
            font=(self.F_FAMILY, 9),
            bg=self.C_SURFACE_ACTIVE,
            fg=self.C_TEXT,
            activebackground="#2a2930",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            command=self.browse_directory
        )
        browse_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.start_btn = tk.Button(
            actions_group,
            text=" ▶ BẮT ĐẦU BENCHMARK ",
            font=(self.F_FAMILY, 9, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0ea5e9",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=3,
            cursor="hand2",
            highlightthickness=0,
            command=self.start_audit_thread
        )
        self.start_btn.pack(side=tk.LEFT)
        self.start_btn.bind("<Enter>", lambda e: self._on_btn_hover(True))
        self.start_btn.bind("<Leave>", lambda e: self._on_btn_hover(False))

        # =============================================================
        # 2. HAIRLINE PROGRESS BAR (Siêu mỏng 2px sát mép Topbar)
        # =============================================================
        self.progress_canvas = tk.Canvas(self.root, height=2, bg=self.C_BORDER, highlightthickness=0)
        self.progress_canvas.pack(side=tk.TOP, fill=tk.X)

        # =============================================================
        # 3. ACTION FOOTER BAR (Packed with side=BOTTOM, flat & clean)
        # =============================================================
        footer_border = tk.Frame(self.root, bg=self.C_BORDER, height=1)
        footer_border.pack(side=tk.BOTTOM, fill=tk.X)

        footer = tk.Frame(self.root, bg=self.C_SURFACE, padx=16, pady=6)
        footer.pack(side=tk.BOTTOM, fill=tk.X)

        self.report_notice_var = tk.StringVar(value="Sẵn sàng đo kiểm. Nhấn 'BẮT ĐẦU BENCHMARK' để khởi chạy.")
        self.status_var = self.report_notice_var # Alias
        self.pct_var = tk.StringVar(value="0%")

        report_lbl = tk.Label(
            footer,
            textvariable=self.report_notice_var,
            font=(self.F_FAMILY, 8),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE,
            anchor="w"
        )
        report_lbl.pack(side=tk.LEFT)

        close_btn = tk.Button(
            footer,
            text="Đóng",
            font=(self.F_FAMILY, 9),
            bg=self.C_CARD_BG,
            fg=self.C_TEXT_MUTED,
            activebackground=self.C_SURFACE_ACTIVE,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=3,
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            command=self.root.destroy
        )
        close_btn.pack(side=tk.RIGHT)

        self.copy_prompt_btn = tk.Button(
            footer,
            text="Sao Chép Prompt Cho AI AGENT",
            font=(self.F_FAMILY, 9, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0ea5e9",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=3,
            highlightthickness=0,
            state=tk.DISABLED,
            command=self.copy_ai_prompt
        )
        self.copy_prompt_btn.pack(side=tk.RIGHT, padx=(0, 6))

        self.open_folder_btn = tk.Button(
            footer,
            text="Mở Thư Mục Báo Cáo",
            font=(self.F_FAMILY, 9),
            bg=self.C_CARD_BG,
            fg=self.C_TEXT_MUTED,
            activebackground=self.C_SURFACE_ACTIVE,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=3,
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            state=tk.DISABLED,
            command=self.open_report_folder
        )
        self.open_folder_btn.pack(side=tk.RIGHT, padx=(0, 6))

        self.open_report_btn = tk.Button(
            footer,
            text="Mở Báo Cáo Markdown",
            font=(self.F_FAMILY, 9),
            bg=self.C_CARD_BG,
            fg=self.C_TEXT_MUTED,
            activebackground=self.C_SURFACE_ACTIVE,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=3,
            highlightthickness=1,
            highlightbackground=self.C_BORDER,
            state=tk.DISABLED,
            command=self.open_report_file
        )
        self.open_report_btn.pack(side=tk.RIGHT, padx=(0, 6))

        # =============================================================
        # 4. SEAMLESS WORKSPACE (2 Cột Liền Mạch, Không Khoảng Hở)
        # =============================================================
        workspace = tk.Frame(self.root, bg=self.C_BG)
        workspace.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        workspace.columnconfigure(0, weight=0, minsize=330)
        workspace.columnconfigure(1, weight=1)
        workspace.rowconfigure(0, weight=1)

        # -------------------------------------------------------------
        # CỘT TRÁI: SIDEBAR DANH MỤC (Flat List Items, không viền hộp)
        # -------------------------------------------------------------
        left_sidebar = tk.Frame(workspace, bg=self.C_SURFACE, width=330)
        left_sidebar.grid(row=0, column=0, sticky="nsew")
        left_sidebar.pack_propagate(False)

        left_hdr = tk.Label(
            left_sidebar,
            text="DANH MỤC BENCHMARK",
            font=(self.F_FAMILY, 8, "bold"),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE
        )
        left_hdr.pack(anchor="w", padx=16, pady=(12, 6))

        # Scrollable container for sidebar items
        self.cards_canvas = tk.Canvas(left_sidebar, bg=self.C_SURFACE, highlightthickness=0)
        self.cards_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cards_scrollbar = tk.Scrollbar(
            left_sidebar,
            orient="vertical",
            command=self.cards_canvas.yview,
            bg=self.C_SURFACE,
            troughcolor=self.C_SURFACE,
            activebackground="#212026",
            relief=tk.FLAT,
            bd=0,
            width=6
        )

        self.cards_inner = tk.Frame(self.cards_canvas, bg=self.C_SURFACE)
        self.cards_inner_win = self.cards_canvas.create_window((0, 0), window=self.cards_inner, anchor="nw")

        def _on_canvas_configure(event):
            self.cards_canvas.itemconfig(self.cards_inner_win, width=event.width)
        self.cards_canvas.bind("<Configure>", _on_canvas_configure)

        def _on_inner_configure(event):
            self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))
            if self.cards_inner.winfo_reqheight() > self.cards_canvas.winfo_height() and self.cards_canvas.winfo_height() > 10:
                self.cards_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                self.cards_scrollbar.pack_forget()
        self.cards_inner.bind("<Configure>", _on_inner_configure)

        def _on_mousewheel(event):
            if self.cards_inner.winfo_reqheight() > self.cards_canvas.winfo_height():
                self.cards_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.cards_canvas.bind_all(
            "<MouseWheel>",
            lambda e: _on_mousewheel(e) if self.cards_canvas.winfo_exists() and self.cards_canvas.winfo_containing(e.x_root, e.y_root) else None
        )

        # --- Thẻ 0: Tổng Quan Hệ Thống (Overview Item) ---
        self.overview_card = tk.Frame(self.cards_inner, bg=self.C_SURFACE_ACTIVE, padx=12, pady=6, cursor="hand2")
        self.overview_card.pack(fill=tk.X, padx=8, pady=2)
        self.overview_card.bind("<Button-1>", lambda e: self.select_module("overview"))

        ov_r1 = tk.Frame(self.overview_card, bg=self.C_SURFACE_ACTIVE)
        ov_r1.pack(fill=tk.X)
        ov_r1.bind("<Button-1>", lambda e: self.select_module("overview"))

        self.ov_bullet = tk.Label(ov_r1, text="◆", font=(self.F_FAMILY, 9), bg=self.C_SURFACE_ACTIVE, fg=self.C_CYAN)
        self.ov_bullet.pack(side=tk.LEFT, padx=(0, 6))
        self.ov_bullet.bind("<Button-1>", lambda e: self.select_module("overview"))

        ov_title = tk.Label(ov_r1, text="Tổng quan hệ thống", font=(self.F_FAMILY, 9), fg="#ffffff", bg=self.C_SURFACE_ACTIVE)
        ov_title.pack(side=tk.LEFT)
        ov_title.bind("<Button-1>", lambda e: self.select_module("overview"))

        self.ov_status = tk.Label(ov_r1, text="Sẵn sàng", font=(self.F_FAMILY, 8), fg=self.C_CYAN, bg=self.C_SURFACE_ACTIVE)
        self.ov_status.pack(side=tk.RIGHT)
        self.ov_status.bind("<Button-1>", lambda e: self.select_module("overview"))

        ov_r2 = tk.Frame(self.overview_card, bg=self.C_SURFACE_ACTIVE)
        ov_r2.pack(fill=tk.X, pady=(2, 0))
        ov_r2.bind("<Button-1>", lambda e: self.select_module("overview"))

        self.ov_subtitle = tk.Label(
            ov_r2,
            text="Hồ sơ kiến trúc, ưu điểm & rủi ro",
            font=(self.F_FAMILY, 8),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE_ACTIVE,
            anchor="w"
        )
        self.ov_subtitle.pack(fill=tk.X, padx=(18, 0))
        self.ov_subtitle.bind("<Button-1>", lambda e: self.select_module("overview"))

        # --- 6 Hạng Mục Đo Kiểm (Flat, Title Case, Nét Mảnh Regular) ---
        self.card_widgets = {}
        for mod_key, short_name, full_key, default_pts, desc_text in self.MODULE_DEFS:
            card = tk.Frame(self.cards_inner, bg=self.C_SURFACE, padx=12, pady=6, cursor="hand2")
            card.pack(fill=tk.X, padx=8, pady=2)
            card.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))
            card.bind("<Enter>", lambda e, c=card, k=mod_key: self._on_card_hover(c, k, True))
            card.bind("<Leave>", lambda e, c=card, k=mod_key: self._on_card_hover(c, k, False))

            # Row 1: Tên mục (Trái) + Điểm số (Phải)
            r1 = tk.Frame(card, bg=self.C_SURFACE)
            r1.pack(fill=tk.X)
            r1.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))

            name_lbl = tk.Label(r1, text=short_name, font=(self.F_FAMILY, 9), fg=self.C_TEXT_SUB, bg=self.C_SURFACE)
            name_lbl.pack(side=tk.LEFT)
            name_lbl.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))

            score_lbl = tk.Label(r1, text=f"-- / {default_pts}đ", font=(self.F_FAMILY, 9), fg=self.C_TEXT_MUTED, bg=self.C_SURFACE)
            score_lbl.pack(side=tk.RIGHT)
            score_lbl.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))

            # Row 2: Trạng thái (Trái) + Trọng số (Phải)
            r2 = tk.Frame(card, bg=self.C_SURFACE)
            r2.pack(fill=tk.X, pady=(2, 0))
            r2.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))

            status_lbl = tk.Label(r2, text="○ Chờ đo kiểm", font=(self.F_FAMILY, 8), fg=self.C_TEXT_DIM, bg=self.C_SURFACE)
            status_lbl.pack(side=tk.LEFT)
            status_lbl.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))

            weight_lbl = tk.Label(r2, text=f"Trọng số: {default_pts}%", font=(self.F_FAMILY, 8), fg=self.C_TEXT_MUTED, bg=self.C_SURFACE)
            weight_lbl.pack(side=tk.RIGHT)
            weight_lbl.bind("<Button-1>", lambda e, k=mod_key: self.select_module(k))

            self.card_widgets[mod_key] = {
                'frame': card,
                'name_lbl': name_lbl,
                'status_lbl': status_lbl,
                'score_lbl': score_lbl,
                'weight_lbl': weight_lbl,
                'r1': r1,
                'r2': r2,
                'max_pts': default_pts,
                'short_name': short_name,
                'full_key': full_key,
                'desc_text': desc_text
            }

        # -------------------------------------------------------------
        # CỘT PHẢI: MAIN INSPECTOR WORKSPACE (Liền mạch, tích hợp Telemetry)
        # -------------------------------------------------------------
        right_workspace = tk.Frame(workspace, bg=self.C_BG)
        right_workspace.grid(row=0, column=1, sticky="nsew")

        # Telemetry & Section Header (Tích hợp liền khối trên nóc vùng Inspector)
        telemetry_hdr = tk.Frame(right_workspace, bg=self.C_SURFACE, padx=20, pady=8)
        telemetry_hdr.pack(side=tk.TOP, fill=tk.X)

        # Header Row 1: Section Title (Trái) + Điểm / Badge (Phải)
        t_row1 = tk.Frame(telemetry_hdr, bg=self.C_SURFACE)
        t_row1.pack(fill=tk.X)

        self.detail_title_lbl = tk.Label(
            t_row1,
            text="TỔNG QUAN HỆ THỐNG & TECH STACK",
            font=(self.F_FAMILY, 9, "bold"),
            fg=self.C_TEXT,
            bg=self.C_SURFACE
        )
        self.detail_title_lbl.pack(side=tk.LEFT)

        self.detail_badge_lbl = tk.Label(
            t_row1,
            text="CHƯA QUÉT",
            font=(self.F_FAMILY, 8),
            fg=self.C_TEXT_DIM,
            bg=self.C_CARD_BG,
            padx=8,
            pady=2,
            highlightthickness=1,
            highlightbackground=self.C_BORDER
        )
        self.detail_badge_lbl.pack(side=tk.RIGHT)

        # Header Row 2: Telemetry Metrics Inline
        t_row2 = tk.Frame(telemetry_hdr, bg=self.C_SURFACE)
        t_row2.pack(fill=tk.X, pady=(4, 0))

        self.score_val_lbl = tk.Label(
            t_row2,
            text="Điểm Benchmark: -- / 100",
            font=(self.F_FAMILY, 9, "bold"),
            fg=self.C_CYAN,
            bg=self.C_SURFACE
        )
        self.score_val_lbl.pack(side=tk.LEFT, padx=(0, 16))

        self.grade_val_lbl = tk.Label(
            t_row2,
            text="Xếp hạng: --",
            font=(self.F_FAMILY, 9),
            fg=self.C_TEXT_SUB,
            bg=self.C_SURFACE
        )
        self.grade_val_lbl.pack(side=tk.LEFT, padx=(0, 16))

        self.archetype_val_lbl = tk.Label(
            t_row2,
            text="Loại hình: Chưa xác định",
            font=(self.F_FAMILY, 8),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE
        )
        self.archetype_val_lbl.pack(side=tk.LEFT, padx=(0, 16))

        self.scope_val_lbl = tk.Label(
            t_row2,
            text="Phạm vi: 6 Hạng Mục Chuẩn Mực",
            font=(self.F_FAMILY, 8),
            fg=self.C_TEXT_MUTED,
            bg=self.C_SURFACE
        )
        self.scope_val_lbl.pack(side=tk.LEFT)

        # Hairline divider dưới Header
        hdr_sep = tk.Frame(right_workspace, bg=self.C_BORDER, height=1)
        hdr_sep.pack(side=tk.TOP, fill=tk.X)

        # Detail Content Text Box
        content_box_frame = tk.Frame(right_workspace, bg=self.C_BG)
        content_box_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            content_box_frame,
            bg=self.C_SURFACE,
            troughcolor=self.C_BG,
            activebackground="#212026",
            relief=tk.FLAT,
            bd=0,
            width=6
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.details_box = tk.Text(
            content_box_frame,
            font=(self.F_FAMILY, 9),
            bg=self.C_BG,
            fg=self.C_TEXT_SUB,
            relief=tk.FLAT,
            padx=20,
            pady=16,
            wrap=tk.WORD,
            insertbackground=self.C_CYAN,
            yscrollcommand=scrollbar.set
        )
        self.details_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.details_box.yview)

        # Text Tags (Nét chữ mảnh chuẩn Antigravity)
        self.details_box.tag_configure("h1", font=(self.F_FAMILY, 10, "bold"), foreground="#ffffff", spacing3=6)
        self.details_box.tag_configure("h2", font=(self.F_FAMILY, 9, "bold"), foreground="#ffffff", spacing1=8, spacing3=4)
        self.details_box.tag_configure("bullet", font=(self.F_FAMILY, 9), foreground=self.C_TEXT_SUB, spacing1=2)
        self.details_box.tag_configure("success", font=(self.F_FAMILY, 9), foreground=self.C_CYAN)
        self.details_box.tag_configure("warning", font=(self.F_FAMILY, 9), foreground=self.C_AMBER)
        self.details_box.tag_configure("danger", font=(self.F_FAMILY, 9), foreground=self.C_ROSE)
        self.details_box.tag_configure("code", font=(self.F_CODE_FAMILY, 9), foreground=self.C_CYAN)
        self.details_box.tag_configure("muted", font=(self.F_FAMILY, 8), foreground=self.C_TEXT_MUTED)

        self.render_initial_welcome()

    def _on_btn_hover(self, is_hover):
        if self.is_running:
            return
        self.start_btn.config(bg="#0ea5e9" if is_hover else "#0284c7")

    def _on_card_hover(self, card, mod_key, is_hover):
        if self.active_module_key == mod_key:
            return
        bg_col = self.C_SURFACE_HOVER if is_hover else self.C_SURFACE
        card.config(bg=bg_col)
        data = self.card_widgets.get(mod_key, {})
        for w_name in ['name_lbl', 'status_lbl', 'score_lbl', 'weight_lbl', 'r1', 'r2']:
            if w_name in data:
                data[w_name].config(bg=bg_col)

    def render_initial_welcome(self):
        self.details_box.config(state=tk.NORMAL)
        self.details_box.delete("1.0", tk.END)

        self.details_box.insert(tk.END, "HỆ THỐNG ĐO KIỂM & CHẨN ĐOÁN KIẾN TRÚC MÃ NGUỒN\n", "h1")
        self.details_box.insert(tk.END, "Cơ chế phân bổ trọng số thích ứng tự động (Adaptive Archetype Weighting Engine)\n\n", "muted")

        self.details_box.insert(tk.END, "NGUYÊN LÝ PHÂN BỔ TRỌNG SỐ THEO TÍNH CHẤT DỰ ÁN:\n", "h2")
        self.details_box.insert(tk.END, "• Dự án FRONTEND SPA / UI-UX : Frontend (35đ) & Anti-Crash (25đ) chiếm trọng số áp đảo; Backend/DB được miễn trừ.\n", "bullet")
        self.details_box.insert(tk.END, "• Dự án BACKEND API / DATA   : Backend (35đ) & Database (25đ) chiếm tỷ trọng chính; Frontend được miễn trừ.\n", "bullet")
        self.details_box.insert(tk.END, "• Dự án FULL-STACK TOÀN DIỆN : Cân bằng tỷ trọng giữa FE, BE, DB, Anti-Crash và Tài liệu Onboarding.\n\n", "bullet")

        self.details_box.insert(tk.END, "QUY TRÌNH THỰC HIỆN:\n", "h2")
        self.details_box.insert(tk.END, "1. Nhập hoặc duyệt thư mục dự án cần đo kiểm ở thanh công cụ phía trên.\n", "bullet")
        self.details_box.insert(tk.END, "2. Nhấn nút 'BẮT ĐẦU BENCHMARK'.\n", "bullet")
        self.details_box.insert(tk.END, "3. Hệ thống sẽ tự động len lỏi phân tích mã nguồn (Waterflow Traversal) và lập bảng xếp hạng chuẩn xác.\n", "bullet")

        self.details_box.insert(tk.END, "\n👉 Bạn có thể click vào bất kỳ hạng mục nào ở cột bên trái để kiểm tra chi tiết các vi phạm và giải pháp refactor tương ứng.\n", "muted")
        self.details_box.config(state=tk.DISABLED)

    def select_module(self, key):
        self.active_module_key = key
        self.update_card_active_states()
        self.render_selected_detail()

    def update_card_active_states(self):
        # Update overview
        if self.active_module_key == "overview":
            self.overview_card.config(bg=self.C_SURFACE_ACTIVE)
            self.ov_bullet.config(bg=self.C_SURFACE_ACTIVE, fg=self.C_CYAN)
            self.ov_status.config(bg=self.C_SURFACE_ACTIVE)
            self.ov_subtitle.config(bg=self.C_SURFACE_ACTIVE)
        else:
            self.overview_card.config(bg=self.C_SURFACE)
            self.ov_bullet.config(bg=self.C_SURFACE, fg=self.C_TEXT_MUTED)
            self.ov_status.config(bg=self.C_SURFACE)
            self.ov_subtitle.config(bg=self.C_SURFACE)

        # Update module items
        for mod_key, data in self.card_widgets.items():
            card = data['frame']
            is_active = (self.active_module_key == mod_key)
            active_bg = self.C_SURFACE_ACTIVE if is_active else self.C_SURFACE

            card.config(bg=active_bg)
            data['r1'].config(bg=active_bg)
            data['r2'].config(bg=active_bg)
            data['name_lbl'].config(bg=active_bg, fg=self.C_TEXT if is_active else self.C_TEXT_SUB)
            data['status_lbl'].config(bg=active_bg)
            data['score_lbl'].config(bg=active_bg)
            data['weight_lbl'].config(bg=active_bg)

    def render_selected_detail(self):
        self.details_box.config(state=tk.NORMAL)
        self.details_box.delete("1.0", tk.END)

        if self.active_module_key == "overview":
            self.detail_title_lbl.config(text="TỔNG QUAN HỆ THỐNG & TECH STACK")
            if not self.auditor:
                self.detail_badge_lbl.config(text="CHƯA QUÉT", fg=self.C_TEXT_DIM)
                self.render_initial_welcome()
                return

            score = self.auditor.calculate_total_score() if hasattr(self.auditor, 'calculate_total_score') else 0
            grade = self.auditor.get_letter_grade(score)
            self.detail_badge_lbl.config(text=f"TỔNG ĐIỂM: {score} / 100 [{grade.split()[0]}]", fg=self.C_CYAN)

            prof = self.auditor.profile
            self.details_box.insert(tk.END, "HỒ SƠ HỆ THỐNG & KẾT QUẢ BENCHMARK\n", "h1")
            self.details_box.insert(tk.END, f"• Loại hình dự án : {prof.get('archetype', 'N/A')}\n", "bullet")
            self.details_box.insert(tk.END, f"• Tech Stack      : {', '.join(prof.get('languages', []))} ({', '.join(prof.get('frameworks', []))})\n", "bullet")
            self.details_box.insert(tk.END, f"• Kiến trúc       : {prof.get('arch_style', 'N/A')}\n", "bullet")
            if prof.get('databases'):
                self.details_box.insert(tk.END, f"• Cơ sở dữ liệu   : {', '.join(prof.get('databases', []))} | {', '.join(prof.get('tools', []))}\n", "bullet")
            self.details_box.insert(tk.END, f"• Mã nguồn quét   : {self.auditor.details.get('anti_crash', {}).get('scanned_files', 0)} tệp mã nguồn\n\n", "bullet")

            if self.auditor.innovations:
                self.details_box.insert(tk.END, "ĐIỂM SÁNG CÔNG NGHỆ & ƯU ĐIỂM (STRENGTHS):\n", "h2")
                for item in self.auditor.innovations:
                    self.details_box.insert(tk.END, f"  ✔ {item}\n", "success")
                self.details_box.insert(tk.END, "\n")

            if self.auditor.gaps:
                self.details_box.insert(tk.END, "KHOẢNG TRỐNG KIẾN TRÚC CẦN BỔ SUNG (GAPS):\n", "h2")
                for gap in self.auditor.gaps:
                    self.details_box.insert(tk.END, f"  ✖ {gap}\n", "danger")
                self.details_box.insert(tk.END, "\n")

            if hasattr(self.auditor, 'bloat') and self.auditor.bloat:
                self.details_box.insert(tk.END, "RÁC DỰ ÁN & RỦI RO BẢO MẬT (BLOAT & RISKS):\n", "h2")
                for b in self.auditor.bloat:
                    self.details_box.insert(tk.END, f"  ! {b}\n", "warning")
                self.details_box.insert(tk.END, "\n")

            if self.auditor.violations:
                self.details_box.insert(tk.END, "TOP VỊ TRÍ VI PHẠM MÃ NGUỒN CẦN REFACTOR GẤP:\n", "h2")
                for v in self.auditor.violations[:5]:
                    self.details_box.insert(tk.END, f"  • {v['file']}:{v['line']} ", "code")
                    self.details_box.insert(tk.END, f"[{v['type']}]: {v['desc']}\n", "danger")
                if len(self.auditor.violations) > 5:
                    self.details_box.insert(tk.END, f"    ... và còn {len(self.auditor.violations) - 5} vị trí khác (xem chi tiết trong file report).\n", "muted")

            self.details_box.insert(tk.END, "\n👉 Gợi ý: Click vào từng HẠNG MỤC BENCHMARK ở cột bên trái để soi chi tiết từng phần.\n", "muted")
            self.details_box.config(state=tk.DISABLED)
            return

        # Render module detail
        mod_key = self.active_module_key
        card_meta = self.card_widgets.get(mod_key, {})
        short_name = card_meta.get('short_name', mod_key)
        desc_text = card_meta.get('desc_text', '')

        self.detail_title_lbl.config(text=f"{short_name} • CHI TIẾT BENCHMARK")

        if not self.auditor:
            max_pts = card_meta.get('max_pts', 20)
            self.detail_badge_lbl.config(text=f"TỐI ĐA: {max_pts} ĐIỂM", fg=self.C_TEXT_DIM)
            self.details_box.insert(tk.END, f"TIÊU CHUẨN ĐO KIỂM: {short_name}\n", "h1")
            self.details_box.insert(tk.END, f"Mô tả mục tiêu: {desc_text}\n\n", "muted")
            self.details_box.insert(tk.END, "Hệ thống chưa chạy benchmark. Nhấn 'BẮT ĐẦU BENCHMARK' để phân tích mã nguồn.", "bullet")
            self.details_box.config(state=tk.DISABLED)
            return

        detail = self.auditor.details.get(mod_key, {})
        is_na = detail.get('is_na', False)
        pts_earned = detail.get('points_earned', 0)
        max_pts = detail.get('max_points', card_meta.get('max_pts', 20))
        raw_score = detail.get('raw_score', detail.get('score', 0))

        if is_na:
            self.detail_badge_lbl.config(text="MIỄN TRỪ [N/A]", fg=self.C_TEXT_DIM)
            self.details_box.insert(tk.END, f"{short_name}\n", "h1")
            self.details_box.insert(tk.END, "TRẠNG THÁI: MIỄN TRỪ HOÀN TOÀN (N/A)\n", "h2")
            self.details_box.insert(tk.END, f"Hạng mục này không yêu cầu đối với loại hình dự án '{self.auditor.profile.get('archetype')}'.\n", "bullet")
            self.details_box.insert(tk.END, "Dự án không bị trừ điểm, hệ số trọng số được tái phân bổ vào các hạng mục cốt lõi khác.\n\n", "bullet")
            self.details_box.config(state=tk.DISABLED)
            return

        status_tag = "OPTIMAL" if raw_score >= 90 else ("PASS" if raw_score >= 80 else ("DEFICIT" if raw_score >= 60 else "CRITICAL"))
        color_tag = self.C_CYAN if raw_score >= 80 else (self.C_AMBER if raw_score >= 60 else self.C_ROSE)
        self.detail_badge_lbl.config(text=f"{pts_earned} / {max_pts} ĐIỂM [{status_tag}]", fg=color_tag)

        self.details_box.insert(tk.END, f"{short_name}\n", "h1")
        self.details_box.insert(tk.END, f"• Điểm hệ số đạt được : {pts_earned} / {max_pts} ĐIỂM\n", "bullet")
        self.details_box.insert(tk.END, f"• Trọng số phân bổ    : {max_pts}% (Tự động thích ứng theo loại hình {self.auditor.profile.get('archetype')})\n", "bullet")
        self.details_box.insert(tk.END, f"• Mức độ tuân thủ     : {raw_score}% (Trạng thái: {status_tag})\n\n", "bullet")

        # Passed checks
        self.details_box.insert(tk.END, "TIÊU CHUẨN ĐẠT ĐƯỢC (PASSED CHECKS):\n", "h2")
        found_items = detail.get('found', [])
        if found_items:
            for item in found_items:
                self.details_box.insert(tk.END, f"  ✔ {item}\n", "success")
        else:
            self.details_box.insert(tk.END, "  (Chưa phát hiện tiêu chuẩn cấu hình đạt yêu cầu)\n", "muted")
        self.details_box.insert(tk.END, "\n")

        # Deficits
        self.details_box.insert(tk.END, "THIẾU SÓT & ĐIỂM TRỪ CẦN HOÀN THIỆN (DEFICITS & GAPS):\n", "h2")
        missing_items = detail.get('missing', [])
        if missing_items:
            for m in missing_items:
                self.details_box.insert(tk.END, f"  ✖ Thiếu: {m}\n", "danger")
        else:
            self.details_box.insert(tk.END, "  ✔ Không có thiếu sót cấu hình cơ bản.\n", "success")

        # Module-specific violations
        if mod_key == 'backend' and detail.get('leaks'):
            self.details_box.insert(tk.END, "\n[RÒ RỈ RANH GIỚI KIẾN TRÚC BACKEND (LAYER LEAKS)]:\n", "h2")
            for leak in detail['leaks']:
                self.details_box.insert(tk.END, f"  ! {leak}\n", "warning")

        if mod_key == 'frontend' and detail.get('god_components'):
            self.details_box.insert(tk.END, "\n[CẢNH BÁO GOD COMPONENT PHÌNH TO QUÁ MỨC (> 350 DÒNG)]:\n", "h2")
            for gc in detail['god_components']:
                self.details_box.insert(tk.END, f"  ! {gc} -> Khuyến nghị: Tách nhỏ thành UI Atoms / Hooks!\n", "warning")

        if mod_key == 'database' and detail.get('sql_risks'):
            self.details_box.insert(tk.END, "\n[NGUY CƠ BẢO MẬT SQL INJECTION (RAW SQL CONCATENATION)]:\n", "h2")
            for risk in detail['sql_risks']:
                self.details_box.insert(tk.END, f"  ! {risk['file']}:{risk['line']} - {risk['snippet']}\n", "danger")

        if mod_key == 'anti_crash' and detail.get('violations'):
            self.details_box.insert(tk.END, f"\n[CHI TIẾT VI PHẠM ANTI-CRASH ({len(detail['violations'])} VỊ TRÍ)]:\n", "h2")
            for v in detail['violations'][:10]:
                self.details_box.insert(tk.END, f"  • {v['file']}:{v['line']} ", "code")
                self.details_box.insert(tk.END, f"[{v['type']}]: {v['snippet']}\n", "danger")
            if len(detail['violations']) > 10:
                self.details_box.insert(tk.END, f"    ... và còn {len(detail['violations']) - 10} vị trí khác.\n", "muted")

        # Recommendations
        self.details_box.insert(tk.END, "\nKHUYẾN NGHỊ TÁI CẤU TRÚC (ARCHITECT RECOMMENDATION):\n", "h2")
        if raw_score >= 90:
            self.details_box.insert(tk.END, "  Hạng mục này đã đạt chất lượng xuất sắc. Tiếp tục duy trì chuẩn mực!\n", "success")
        elif mod_key == 'readme':
            self.details_box.insert(tk.END, "  Bổ sung các lệnh Quick Start rõ ràng và tài liệu cấu hình .ENV vào README.md.\n", "bullet")
        elif mod_key == 'backend':
            self.details_box.insert(tk.END, "  Đảm bảo Controller không gọi trực tiếp SQL/ORM; cài đặt Graceful Shutdown cho Server.\n", "bullet")
        elif mod_key == 'frontend':
            self.details_box.insert(tk.END, "  Refactor ngay các God Component phình to; tạo tệp API Client bọc tập trung có Interceptors.\n", "bullet")
        elif mod_key == 'database':
            self.details_box.insert(tk.END, "  Sử dụng Parameterized Queries, thiết lập Connection Pool Timeout và tạo thư mục Migrations.\n", "bullet")
        elif mod_key == 'anti_crash':
            self.details_box.insert(tk.END, "  Bọc toàn bộ JSON.parse trong Try-Catch; thay thế ': any' bằng Type/Interface chặt chẽ.\n", "bullet")
        elif mod_key == 'contracts':
            self.details_box.insert(tk.END, "  Tạo file AGENTS.MD hướng dẫn AI Agent và tạo thư mục /adrs lưu trữ quyết định kiến trúc.\n", "bullet")

        self.details_box.config(state=tk.DISABLED)

    def browse_directory(self):
        chosen = filedialog.askdirectory(
            initialdir=self.path_var.get(),
            title="Chọn thư mục dự án cần benchmark kiến trúc"
        )
        if chosen:
            self.path_var.set(os.path.normpath(chosen))

    def update_progress(self, percent, message):
        def _do_update():
            total_w = max(self.progress_canvas.winfo_width(), self.root.winfo_width(), 1000)
            self.progress_canvas.delete("all")

            if percent > 0:
                active_w = int((percent / 100.0) * total_w)
                self.progress_canvas.create_line(0, 1, active_w, 1, fill=self.C_CYAN, width=2)

            self.report_notice_var.set(f"[{percent}%] {message}")
            self.pct_var.set(f"{percent}%")
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
        self.start_btn.config(text=" [...] ĐANG ĐO KIỂM... ", state=tk.DISABLED, bg="#16151b", fg=self.C_TEXT_DIM)
        self.open_report_btn.config(state=tk.DISABLED, fg=self.C_TEXT_DIM)
        self.open_folder_btn.config(state=tk.DISABLED, fg=self.C_TEXT_DIM)
        self.copy_prompt_btn.config(state=tk.DISABLED)
        self.progress_canvas.delete("all")
        self.pct_var.set("0%")

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
        self.status_dot.config(fg=self.C_CYAN)
        self.start_btn.config(text=" ▶ CHẠY LẠI BENCHMARK ", state=tk.NORMAL, bg="#0284c7", fg="#ffffff")
        self.open_report_btn.config(state=tk.NORMAL, fg=self.C_TEXT, bg=self.C_CARD_BG)
        self.open_folder_btn.config(state=tk.NORMAL, fg=self.C_TEXT, bg=self.C_CARD_BG)
        self.copy_prompt_btn.config(state=tk.NORMAL)

        grade = self.auditor.get_letter_grade(total_score)
        score_fg = self.C_CYAN if total_score >= 85 else (self.C_AMBER if total_score >= 60 else self.C_ROSE)

        self.score_val_lbl.config(text=f"Điểm Benchmark: {total_score} / 100", fg=score_fg)
        self.grade_val_lbl.config(text=f"Xếp hạng: {grade.split()[0]}", fg=score_fg)
        
        archetype_text = self.auditor.profile.get('archetype', 'Dự án Chuẩn Mực')
        self.archetype_val_lbl.config(text=f"Loại hình: {archetype_text}")

        applicable_count = 0
        for mod_key, data in self.card_widgets.items():
            detail = self.auditor.details.get(mod_key, {})
            is_na = detail.get('is_na', False)
            pts_earned = detail.get('points_earned', 0)
            max_pts = detail.get('max_points', data['max_pts'])
            raw_score = detail.get('raw_score', detail.get('score', 0))

            if is_na:
                data['status_lbl'].config(text="○ Miễn trừ", fg=self.C_TEXT_DIM)
                data['score_lbl'].config(text="[N/A]", fg=self.C_TEXT_DIM)
                data['weight_lbl'].config(text="Không tính điểm", fg=self.C_TEXT_DIM)
            else:
                applicable_count += 1
                data['weight_lbl'].config(text=f"Trọng số: {max_pts}%", fg=self.C_TEXT_MUTED)
                if raw_score >= 90:
                    data['status_lbl'].config(text="● Optimal", fg=self.C_CYAN)
                    data['score_lbl'].config(text=f"{pts_earned} / {max_pts}đ", fg=self.C_CYAN)
                elif raw_score >= 80:
                    data['status_lbl'].config(text="● Pass", fg=self.C_SKY)
                    data['score_lbl'].config(text=f"{pts_earned} / {max_pts}đ", fg=self.C_SKY)
                elif raw_score >= 60:
                    data['status_lbl'].config(text="● Deficit", fg=self.C_AMBER)
                    data['score_lbl'].config(text=f"{pts_earned} / {max_pts}đ", fg=self.C_AMBER)
                else:
                    data['status_lbl'].config(text="● Critical", fg=self.C_ROSE)
                    data['score_lbl'].config(text=f"{pts_earned} / {max_pts}đ", fg=self.C_ROSE)

        self.scope_val_lbl.config(text=f"Phạm vi: {applicable_count} Hạng Mục Áp Dụng", fg=self.C_TEXT_MUTED)

        self.update_card_active_states()
        self.render_selected_detail()

        if self.report_path:
            self.report_notice_var.set(f"✔ Đã lưu báo cáo Benchmark tại: {self.report_path.resolve()}")

    def _on_audit_error(self, err_msg):
        self.is_running = False
        self.status_dot.config(fg=self.C_ROSE)
        self.start_btn.config(text=" ▶ BẮT ĐẦU BENCHMARK ", state=tk.NORMAL, bg="#0284c7", fg="#ffffff")
        messagebox.showerror("Lỗi Benchmark", f"Có lỗi xảy ra trong quá trình đo kiểm:\n{err_msg}")

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
                "Đã sao chép đoạn PROMPT DÀNH CHO AI AGENT vào Clipboard!\n\n"
                "👉 Bạn chỉ cần mở cửa sổ Chat với AI (CLAUDE CODE, CURSOR, ANTIGRAVITY) "
                "và nhấn Ctrl+V để dán cho AI tiến hành REFACTOR mã nguồn."
            )


def main():
    if os.name == 'nt':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

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

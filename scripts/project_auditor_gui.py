#!/usr/bin/env python3
"""
UNIVERSAL PROJECT STARTER KIT - ARCHITECTURE AUDITOR GUI
Compact Windows Dialog (Unikey Style, Portable, Zero-Install, Zero-Dependency)
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# Add script directory to sys.path to import ProjectAuditor
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from project_auditor import ProjectAuditor
except ImportError:
    # If running bundled via PyInstaller
    from scripts.project_auditor import ProjectAuditor


class ProjectAuditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Project Review & Architecture Auditor")
        self.root.geometry("620x600")
        self.root.minsize(580, 560)
        self.root.configure(bg="#f8f9fa")

        # Set Window Icon if exists
        self.set_app_icon()

        # Auditor state
        self.auditor = None
        self.is_running = False
        self.report_path = None

        # Center window on screen
        self.center_window(620, 600)

        # Build UI Components
        self.create_widgets()

    def set_app_icon(self):
        # Look for app-icon.ico in common bundle / project locations
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
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 30
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        style = ttk.Style()
        try:
            style.theme_use('vista' if 'vista' in style.theme_names() else 'clam')
        except Exception:
            pass

        # -------------------------------------------------------------
        # 1. Header Frame
        # -------------------------------------------------------------
        header_frame = tk.Frame(self.root, bg="#1e293b", padx=16, pady=12)
        header_frame.pack(fill=tk.X)

        title_label = tk.Label(
            header_frame,
            text="🚀 UNIVERSAL PROJECT REVIEW & AUDITOR",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#1e293b"
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Kiểm toán kiến trúc đối chiếu chuẩn AI-Native Starter Kit (Offline & Portable)",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        subtitle_label.pack(anchor="w")

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f8f9fa", padx=16, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # 2. Project Target Directory Frame
        # -------------------------------------------------------------
        dir_frame = tk.LabelFrame(
            main_frame,
            text=" 📁 Thư mục dự án cần review ",
            font=("Segoe UI", 9, "bold"),
            bg="#f8f9fa",
            fg="#0f172a",
            padx=10,
            pady=10
        )
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        # Default path: current working directory or exe directory
        default_path = str(Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path.cwd())
        self.path_var = tk.StringVar(value=default_path)

        path_entry = ttk.Entry(dir_frame, textvariable=self.path_var, font=("Segoe UI", 9))
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        browse_btn = ttk.Button(dir_frame, text="Duyệt...", command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT)

        # -------------------------------------------------------------
        # 3. Action Button (Start Audit)
        # -------------------------------------------------------------
        self.start_btn = tk.Button(
            main_frame,
            text="🚀 BẮT ĐẦU QUÉT KIẾN TRÚC",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.start_audit_thread
        )
        self.start_btn.pack(fill=tk.X, pady=(0, 10))

        # -------------------------------------------------------------
        # 4. Progress Bar & Status
        # -------------------------------------------------------------
        progress_frame = tk.Frame(main_frame, bg="#f8f9fa")
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate", maximum=100)
        self.progress_bar.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Sẵn sàng quét. Hãy chọn thư mục dự án và nhấn 'Bắt Đầu Quét Kiến Trúc'.")
        status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 8, "italic"),
            fg="#475569",
            bg="#f8f9fa",
            anchor="w"
        )
        status_label.pack(fill=tk.X, pady=(4, 0))

        # -------------------------------------------------------------
        # 5. Result Summary Card
        # -------------------------------------------------------------
        self.result_frame = tk.LabelFrame(
            main_frame,
            text=" 📊 Kết quả đối chiếu kiến trúc ",
            font=("Segoe UI", 9, "bold"),
            bg="#ffffff",
            fg="#0f172a",
            padx=12,
            pady=8
        )
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Score & Grade Row
        score_row = tk.Frame(self.result_frame, bg="#ffffff")
        score_row.pack(fill=tk.X, pady=(0, 6))

        self.score_label = tk.Label(
            score_row,
            text="🏆 Tổng điểm tuân thủ: -- / 100",
            font=("Segoe UI", 10, "bold"),
            fg="#1e293b",
            bg="#ffffff"
        )
        self.score_label.pack(side=tk.LEFT)

        self.grade_label = tk.Label(
            score_row,
            text="🎖️ Xếp hạng: Chưa quét",
            font=("Segoe UI", 10, "bold"),
            fg="#64748b",
            bg="#ffffff"
        )
        self.grade_label.pack(side=tk.RIGHT)

        # Separator line
        sep = ttk.Separator(self.result_frame, orient="horizontal")
        sep.pack(fill=tk.X, pady=4)

        # Pillars Text Box (read-only)
        self.details_box = tk.Text(
            self.result_frame,
            height=7,
            font=("Consolas", 8),
            bg="#f8fafc",
            fg="#0f172a",
            relief=tk.FLAT,
            padx=6,
            pady=4
        )
        self.details_box.pack(fill=tk.BOTH, expand=True)
        self.details_box.insert(tk.END, "Chưa có dữ liệu kiểm toán. Nhấn 'Bắt Đầu Quét Kiến Trúc' để bắt đầu.")
        self.details_box.config(state=tk.DISABLED)

        # Report output path notice
        self.report_notice_var = tk.StringVar(value="File báo cáo PROJECT_REVIEW_REPORT.md sẽ được tạo tại thư mục dự án.")
        report_notice_label = tk.Label(
            self.result_frame,
            textvariable=self.report_notice_var,
            font=("Segoe UI", 8),
            fg="#059669",
            bg="#ffffff",
            anchor="w"
        )
        report_notice_label.pack(fill=tk.X, pady=(4, 0))

        # -------------------------------------------------------------
        # 6. Action Buttons Footer
        # -------------------------------------------------------------
        footer_frame = tk.Frame(main_frame, bg="#f8f9fa")
        footer_frame.pack(fill=tk.X)

        self.open_report_btn = ttk.Button(
            footer_frame,
            text="📄 Mở Báo Cáo",
            state=tk.DISABLED,
            command=self.open_report_file
        )
        self.open_report_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.open_folder_btn = ttk.Button(
            footer_frame,
            text="📁 Mở Thư Mục Báo Cáo",
            state=tk.DISABLED,
            command=self.open_report_folder
        )
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.copy_prompt_btn = ttk.Button(
            footer_frame,
            text="📋 Copy Prompt Cho AI",
            state=tk.DISABLED,
            command=self.copy_ai_prompt
        )
        self.copy_prompt_btn.pack(side=tk.LEFT, padx=(0, 6))

        close_btn = ttk.Button(footer_frame, text="Đóng", command=self.root.destroy)
        close_btn.pack(side=tk.RIGHT)

    def browse_directory(self):
        chosen = filedialog.askdirectory(
            initialdir=self.path_var.get(),
            title="Chọn thư mục dự án cần review"
        )
        if chosen:
            self.path_var.set(os.path.normpath(chosen))

    def update_progress(self, percent, message):
        def _do_update():
            self.progress_bar['value'] = percent
            self.status_var.set(f"[{percent}%] {message}")
        self.root.after(0, _do_update)

    def start_audit_thread(self):
        target_dir = self.path_var.get().strip()
        if not target_dir or not Path(target_dir).is_dir():
            messagebox.showerror(
                "Lỗi Đường Dẫn",
                "Thư mục dự án không hợp lệ hoặc không tồn tại!\nVui lòng chọn lại thư mục hợp lệ."
            )
            return

        if self.is_running:
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, text="⏳ ĐANG QUÉT KIẾN TRÚC...")
        self.open_report_btn.config(state=tk.DISABLED)
        self.open_folder_btn.config(state=tk.DISABLED)
        self.copy_prompt_btn.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0

        # Run audit in background thread so GUI never freezes
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
        self.start_btn.config(state=tk.NORMAL, text="🔄 QUÉT LẠI / QUÉT TIẾP")
        self.open_report_btn.config(state=tk.NORMAL)
        self.open_folder_btn.config(state=tk.NORMAL)
        self.copy_prompt_btn.config(state=tk.NORMAL)

        grade = self.auditor.get_letter_grade(total_score)
        
        # Color coding for total score
        score_color = "#16a34a" if total_score >= 85 else ("#ca8a04" if total_score >= 60 else "#dc2626")
        self.score_label.config(
            text=f"🏆 Tổng điểm tuân thủ: {total_score} / 100",
            fg=score_color
        )
        self.grade_label.config(
            text=f"🎖️ Xếp hạng: {grade}",
            fg=score_color
        )

        # Update Pillar details
        details_text = []
        for pillar, score in self.auditor.scores.items():
            bar = "█" * (score // 10) + "░" * (10 - (score // 10))
            details_text.append(f"• {pillar:<30} [{bar}] {score:>3}%")

        if self.auditor.innovations:
            details_text.append("\n🌟 ĐIỂM SÁNG NÂNG CAO (INNOVATIONS):")
            for item in self.auditor.innovations[:3]:
                details_text.append(f"  ✔ {item}")

        if self.auditor.gaps:
            details_text.append("\n⚠️ KHOẢNG TRỐNG CẦN KHẮC PHỤC (GAPS):")
            for gap in self.auditor.gaps[:3]:
                details_text.append(f"  ✖ {gap}")

        self.details_box.config(state=tk.NORMAL)
        self.details_box.delete("1.0", tk.END)
        self.details_box.insert(tk.END, "\n".join(details_text))
        self.details_box.config(state=tk.DISABLED)

        # Update notice of report file
        if self.report_path:
            self.report_notice_var.set(f"✔ Đã xuất báo cáo tại: {self.report_path.resolve()}")

    def _on_audit_error(self, err_msg):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL, text="🚀 BẮT ĐẦU QUÉT KIẾN TRÚC")
        messagebox.showerror("Lỗi Kiểm Toán", f"Có lỗi xảy ra trong quá trình quét:\n{err_msg}")

    def open_report_file(self):
        if self.report_path and self.report_path.exists():
            try:
                os.startfile(str(self.report_path.resolve()))
            except Exception as e:
                messagebox.showerror("Lỗi Mở File", f"Không thể mở file báo cáo: {e}")
        else:
            messagebox.showwarning("Cảnh Báo", "Chưa tìm thấy file báo cáo!")

    def open_report_folder(self):
        target_dir = self.path_var.get().strip()
        if target_dir and Path(target_dir).is_dir():
            try:
                os.startfile(target_dir)
            except Exception as e:
                messagebox.showerror("Lỗi Mở Thư Mục", f"Không thể mở thư mục: {e}")

    def copy_ai_prompt(self):
        if self.auditor:
            prompt_text = self.auditor.get_ai_prompt()
            self.root.clipboard_clear()
            self.root.clipboard_append(prompt_text)
            messagebox.showinfo(
                "Đã Sao Chép!",
                "Đã sao chép đoạn Prompt cho AI Agent vào Clipboard!\n\n"
                "👉 Bạn chỉ cần mở cửa sổ Chat với AI (Claude Code, Cursor, Antigravity) "
                "và nhấn Ctrl+V để dán lệnh bắt đầu sửa code."
            )


def main():
    # If launched with CLI argument (e.g. CI/CD or explicit path in terminal)
    if len(sys.argv) > 1 and sys.argv[1] not in ('--gui',):
        target = Path(sys.argv[1]).resolve()
        if target.is_dir():
            auditor = ProjectAuditor(target)
            score = auditor.run()
            sys.exit(0 if score >= 70 else 1)

    # Launch GUI
    root = tk.Tk()
    app = ProjectAuditorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

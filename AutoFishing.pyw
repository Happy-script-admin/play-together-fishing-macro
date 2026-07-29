import tkinter as tk
import customtkinter as ctk # Thư viện UI hiện đại
import mss
import keyboard
import time
import threading
import cv2
import numpy as np
import os
import sys
import ctypes

# Hàm hỗ trợ tìm đường dẫn file icon chính xác cả khi chạy code lẫn khi đóng gói exe
data_dir = getattr(sys, '_MEIPASS', os.path.abspath("."))
def resource_path(relative_path):
    return os.path.join(data_dir, relative_path)

# Khắc phục lỗi Taskbar không nhận icon riêng trên Windows
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AutoFishingBot.App")
except:
    pass

# Cấu hình giao diện mặc định là Dark Theme
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

class InstantPopupBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Fishing Macro")
        self.root.geometry("480x300")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        
        # --- CÀI ĐẶT ICON CHO CỬA SỔ & TASKBAR ---
        try:
            # ⚠️ THAY "icon.ico" BẰNG TÊN FILE .ICO CỦA BẠN (VD: "my_logo.ico")
            icon_file = resource_path("icon.ico") 
            self.root.iconbitmap(icon_file)
        except Exception as e:
            print(f"Không thể tải icon cửa sổ: {e}")
        # ----------------------------------------
        
        self.is_running = False
        self.bbox_fish = None    
        self.bbox_avatar = None   
        self.avatar_template = None 
        
        self.overlay_fish_win = None
        self.overlay_avatar_win = None
        
        self.sct = mss.mss()
        self.bot_thread = None
        self.selection_target = None 
        
        self.current_progress = 0
        self.fish_caught = 0
        self.interrupt_count = 0

        keyboard.add_hotkey('F4', self.safe_toggle)

        # --- GIAO DIỆN HIỆN ĐẠI (UI) ---
        
        # Tiêu đề
        self.lbl_title = ctk.CTkLabel(root, text="AUTO FISHING BOT", font=("Roboto", 16, "bold"))
        self.lbl_title.pack(pady=(15, 0))
        
        self.lbl_subtitle = ctk.CTkLabel(root, text="(Bật/Tắt nhanh bằng phím F4)", font=("Roboto", 11, "italic"), text_color="gray")
        self.lbl_subtitle.pack(pady=(0, 10))

        # Khung Thống kê (Stats Card)
        self.stats_frame = ctk.CTkFrame(root, fg_color="#2B2B2B", corner_radius=8)
        self.stats_frame.pack(pady=5, padx=20, fill="x")
        
        self.lbl_fish = ctk.CTkLabel(self.stats_frame, text="🐟 Cá câu được: 0", font=("Roboto", 13, "bold"), text_color="#2FA572")
        self.lbl_fish.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.lbl_interrupt = ctk.CTkLabel(self.stats_frame, text="⚠️ Check lại: 0", font=("Roboto", 13, "bold"), text_color="#E24A4A")
        self.lbl_interrupt.pack(side=tk.RIGHT, padx=20, pady=5)

        # Thanh Progress Bar hiện đại
        self.prog_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.prog_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(self.prog_frame, width=380, height=12, progress_color="#3A7EBF")
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 10))
        self.progress_bar.set(0)
        
        self.prog_text = ctk.CTkLabel(self.prog_frame, text="0%", font=("Roboto", 12, "bold"), width=30)
        self.prog_text.pack(side=tk.LEFT)

        # Khung Nút bấm
        self.btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.btn_frame.pack(pady=5)

        self.btn_select_fish = ctk.CTkButton(self.btn_frame, text="1. Vùng Check Cá", command=lambda: self.start_selection('fish'), 
                                             width=130, height=32, fg_color="#4A4A4A", hover_color="#5C5C5C", 
                                             font=("Roboto", 12, "bold"), text_color="#FFFFFF")
        self.btn_select_fish.pack(side=tk.LEFT, padx=5)

        self.btn_select_avatar = ctk.CTkButton(self.btn_frame, text="2. Vùng Avatar", command=lambda: self.start_selection('avatar'), 
                                               width=130, height=32, fg_color="#4A4A4A", hover_color="#5C5C5C", 
                                               font=("Roboto", 12, "bold"), text_color="#FFFFFF")
        self.btn_select_avatar.pack(side=tk.LEFT, padx=5)

        self.btn_toggle = ctk.CTkButton(self.btn_frame, text="START (F4)", command=self.toggle_running, 
                                        width=130, height=32, fg_color="#2FA572", hover_color="#25835A", 
                                        font=("Roboto", 12, "bold"), state="disabled", text_color="#FFFFFF")
        self.btn_toggle.pack(side=tk.LEFT, padx=5)

        # Trạng thái hệ thống
        self.lbl_status = ctk.CTkLabel(root, text="Trạng thái: Vui lòng chọn cả 2 vùng!", font=("Roboto", 12), text_color="gray")
        self.lbl_status.pack(pady=(10, 5))

    # --- HÀM CẬP NHẬT UI ---
    def update_stats_ui(self):
        self.lbl_fish.configure(text=f"🐟 Cá câu được: {self.fish_caught}")
        self.lbl_interrupt.configure(text=f"⚠️ Check lại: {self.interrupt_count}")

    def update_progress_ui(self, percent):
        p = min(max(percent, 0), 100)
        self.progress_bar.set(p / 100)
        self.prog_text.configure(text=f"{int(p)}%")
        
        if p < 20:
            self.progress_bar.configure(progress_color="#8CFFF7") 
        elif p < 50:
            self.progress_bar.configure(progress_color="#3A7EBF") 
        elif p < 70:
            self.progress_bar.configure(progress_color="#E08631") 
        else:
            self.progress_bar.configure(progress_color="#2FA572") 

    def sleep_with_progress(self, duration, start_p, end_p):
        start_time = time.time()
        while time.time() - start_time < duration and self.is_running:
            elapsed = time.time() - start_time
            current_p = start_p + (elapsed / duration) * (end_p - start_p)
            self.current_progress = current_p
            self.root.after(0, self.update_progress_ui, current_p)
            time.sleep(0.01)

    def safe_toggle(self):
        if self.btn_toggle.cget("state") == "normal":
            self.root.after(0, self.toggle_running)

    def check_ready_to_start(self):
        if self.bbox_fish and self.bbox_avatar:
            self.btn_toggle.configure(state="normal")
            self.lbl_status.configure(text="Đã lưu 2 vùng! Bấm START để chạy", text_color="#2FA572")

    def draw_overlay(self, bbox, color):
        x1, y1, x2, y2 = bbox
        w, h = x2 - x1, y2 - y1

        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)
        overlay.config(bg="magenta")
        overlay.attributes("-transparentcolor", "magenta")
        overlay.geometry(f"{w}x{h}+{x1}+{y1}")
        
        canvas = tk.Canvas(overlay, bg="magenta", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_rectangle(1, 1, w-1, h-1, outline=color, width=2)
        
        return overlay

    def start_selection(self, target):
        if self.is_running: self.toggle_running()
        self.selection_target = target
        self.root.withdraw()
        
        self.snip_win = tk.Toplevel()
        self.snip_win.attributes('-fullscreen', True)
        self.snip_win.attributes('-alpha', 0.3)
        self.snip_win.attributes('-topmost', True)
        self.snip_win.config(cursor="cross")
        self.snip_win.focus_force()

        self.canvas = tk.Canvas(self.snip_win, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.start_x = self.start_y = self.rect = None
        
        guide_text = "KÉO CHUỘT: Quét trên đầu phao" if target == 'fish' else "KÉO CHUỘT: Khoét ôm sát Avatar"
        self.canvas.create_text(self.snip_win.winfo_screenwidth() // 2, 50, text=guide_text, fill="white", font=("Roboto", 22, "bold"))

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='#3A7EBF', width=3, fill='black')

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        end_x, end_y = event.x, event.y
        bbox = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))
        
        if bbox[2] - bbox[0] > 5 and bbox[3] - bbox[1] > 5:
            if self.selection_target == 'fish':
                self.bbox_fish = bbox
            elif self.selection_target == 'avatar':
                self.bbox_avatar = bbox

        self.snip_win.destroy()
        self.root.deiconify()
        self.check_ready_to_start()
            
    def toggle_running(self):
        if not self.is_running:
            self.is_running = True
            self.btn_toggle.configure(text="STOP (F4)", fg_color="#E24A4A", hover_color="#B83A3A")
            
            self.current_progress = 0
            self.root.after(0, self.update_progress_ui, 0)
            
            if self.bbox_fish:
                self.overlay_fish_win = self.draw_overlay(self.bbox_fish, "#E08631")
            if self.bbox_avatar:
                self.overlay_avatar_win = self.draw_overlay(self.bbox_avatar, "#3A7EBF")

            self.avatar_template = self.capture_cv2_avatar()

            self.bot_thread = threading.Thread(target=self.bot_logic_loop, daemon=True)
            self.bot_thread.start()
        else:
            self.is_running = False
            self.btn_toggle.configure(text="START (F4)", fg_color="#2FA572", hover_color="#25835A")
            self.update_status("Đã dừng hoạt động", "gray")
            
            self.root.after(0, self.update_progress_ui, 0)
            
            if self.overlay_fish_win:
                self.overlay_fish_win.destroy()
                self.overlay_fish_win = None
            if self.overlay_avatar_win:
                self.overlay_avatar_win.destroy()
                self.overlay_avatar_win = None

            keyboard.release('f') 
            keyboard.release('space')

    def update_status(self, text, color):
        color_map = {
            "red": "#E24A4A", "green": "#2FA572", "blue": "#3A7EBF", 
            "orange": "#E08631", "purple": "#9B59B6", "gray": "gray"
        }
        hex_color = color_map.get(color, "white")
        self.lbl_status.configure(text=text, text_color=hex_color)

    def capture_cv2_fish(self):
        monitor = {"top": self.bbox_fish[1], "left": self.bbox_fish[0], "width": self.bbox_fish[2] - self.bbox_fish[0], "height": self.bbox_fish[3] - self.bbox_fish[1]}
        img = self.sct.grab(monitor)
        frame = np.array(img)[:, :, :3]
        return cv2.GaussianBlur(frame, (3, 3), 0)

    def capture_cv2_avatar(self):
        monitor = {"top": self.bbox_avatar[1], "left": self.bbox_avatar[0], "width": self.bbox_avatar[2] - self.bbox_avatar[0], "height": self.bbox_avatar[3] - self.bbox_avatar[1]}
        img = self.sct.grab(monitor)
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2GRAY)
        return cv2.Canny(gray, 50, 150)

    def bot_logic_loop(self):
        while self.is_running:
            self.current_progress = 0
            self.root.after(0, self.update_progress_ui, 5) 
            
            while self.is_running:
                current_avatar = self.capture_cv2_avatar()
                res = cv2.matchTemplate(current_avatar, self.avatar_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                
                is_idle = max_val > 0.6 

                if is_idle:
                    self.update_status("Chưa thả cần. Đang nhấn [F]...", "blue")
                    self.root.after(0, self.update_progress_ui, 10) 
                    keyboard.press('f'); time.sleep(0.03); keyboard.release('f')
                    break 
                else:
                    self.interrupt_count += 1
                    self.root.after(0, self.update_stats_ui)
                    self.update_status("Sai trạng thái. Đang rút cần [F]...", "orange")
                    keyboard.press('f'); time.sleep(0.03); keyboard.release('f')
                    self.sleep_with_progress(2.0, 10, 0)
                    self.root.after(0, self.update_progress_ui, 5) 

            if not self.is_running: break

            self.update_status("Đợi 3s phao ổn định...", "gray")
            self.sleep_with_progress(3.0, 10, 20)
            if not self.is_running: break

            self.update_status("Đang lấy dữ liệu phao gốc...", "purple")
            baseline_frame = self.capture_cv2_fish()

            self.update_status("ĐANG QUÉT CÁ CẮN CÂU...", "green")
            detected = False
            interrupted = False 
            start_wait_time = time.time()
            
            while self.is_running:
                elapsed = time.time() - start_wait_time
                prog = min(50, 20 + (elapsed / 17.0) * 30)
                self.current_progress = prog
                self.root.after(0, self.update_progress_ui, prog)
                
                current_frame = self.capture_cv2_fish()
                diff = cv2.absdiff(baseline_frame, current_frame)
                gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray_diff, 25, 255, cv2.THRESH_BINARY)
                
                if cv2.countNonZero(thresh) > (thresh.shape[0] * thresh.shape[1] * 0.2):
                    detected = True
                    break 
                
                current_avatar_scan = self.capture_cv2_avatar()
                res_scan = cv2.matchTemplate(current_avatar_scan, self.avatar_template, cv2.TM_CCOEFF_NORMED)
                _, max_val_scan, _, _ = cv2.minMaxLoc(res_scan)
                
                if max_val_scan > 0.6:
                    self.update_status("Bị ngắt quãng! Trở về Bước 1...", "red")
                    interrupted = True
                    break

                time.sleep(0.01) 

            if not self.is_running: break
            if interrupted:
                self.interrupt_count += 1
                self.root.after(0, self.update_stats_ui)
                self.root.after(0, self.update_progress_ui, 0)
                continue 

            if detected:
                self.update_status("CÁ CẮN! Đang giữ [F] 4.5s", "red")
                keyboard.press('f')
                self.sleep_with_progress(4.5, self.current_progress, 70)
                keyboard.release('f')
                
                if not self.is_running: break
                self.update_status("Đã thả F. Đợi 1.0s...", "orange")
                self.sleep_with_progress(1.0, 70, 75)
                
                if not self.is_running: break
                self.update_status("Check Avatar trước khi tắt UI...", "purple")
                self.root.after(0, self.update_progress_ui, 80)
                
                current_avatar_check = self.capture_cv2_avatar()
                res_check = cv2.matchTemplate(current_avatar_check, self.avatar_template, cv2.TM_CCOEFF_NORMED)
                _, max_val_check, _, _ = cv2.minMaxLoc(res_check)

                if max_val_check > 0.6:
                    self.interrupt_count += 1
                    self.root.after(0, self.update_stats_ui)
                    self.update_status("Lỗi nhịp! Quay lại Bước 1...", "red")
                    self.root.after(0, self.update_progress_ui, 0)
                    continue
                else:
                    self.update_status("Nhấn [SPACE] hoàn tất", "blue")
                    self.root.after(0, self.update_progress_ui, 90)
                    keyboard.press('space'); time.sleep(0.03); keyboard.release('space')
                    self.update_status("Hoàn thành! Chuẩn bị vòng mới...", "gray")
                    self.sleep_with_progress(1.0, 90, 100)
                    self.fish_caught += 1
                    self.root.after(0, self.update_stats_ui)
                    time.sleep(0.3) 

if __name__ == "__main__":
    root = ctk.CTk()
    app = InstantPopupBot(root)
    root.mainloop()
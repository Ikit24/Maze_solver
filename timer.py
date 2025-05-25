import tkinter as tk

class Timer:
    def __init__(self, root):
        self.root = root
        self.seconds = 0
        self.timer_running = False
        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 40))
        self.timer_label.pack(pady=20)
        self.update_timer()
        
    def start(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            self.seconds += 1
            minutes = self.seconds // 60
            seconds = self.seconds % 60
            time_str = f"{minutes:02}:{seconds:02}"
            self.timer_label.config(text=time_str)
            self.root.after(1000, self.update_timer)
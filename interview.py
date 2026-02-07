import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

# ==========================================================
# GLOBAL CONFIGURATION
# ==========================================================
APP_TITLE = "Pro Mock Interview Simulator (Auto-Start Mode)"
WINDOW_GEOMETRY = "1100x850"

# Timer settings (in seconds)
PREP_TIME_LIMIT = 10  # 10 seconds preparation
INTERVIEW_TIME_LIMIT = 90  # 90 seconds response time
VIDEO_REFRESH_RATE = 15  # ms

# Theme Colors
COLORS = {
    "bg_main": "#f5f6fa",
    "text_primary": "#2f3640",
    "btn_next": "#0097e6",
    "btn_start": "#44bd32",
    "timer_prep": "#f39c12",  # Orange for preparation
    "timer_alert": "#e84118",  # Red for answering
    "video_border": "#2f3640"
}

# Simple Question List
QUESTION_BANK = [
    "What are your career goals for the next three years?",
    "Talk about your most recent project."
]


# ==========================================================

class InterviewSimulator:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry(WINDOW_GEOMETRY)
        self.window.configure(bg=COLORS["bg_main"])

        # --- 1. State Variables ---
        self.questions = QUESTION_BANK
        self.vid = cv2.VideoCapture(0)
        self.timer_running = False
        self.is_prep_phase = False  # New state to track if we are in 10s prep
        self.remaining_time = 0
        self.timer_id = None
        self.current_index = 0

        # --- 2. UI Layout ---
        self._setup_ui()

        # Start Video Stream
        self.update_video()
        self.window.mainloop()

    def _setup_ui(self):
        """Initialize simplified UI components"""

        # Question Display Area
        self.lbl_question = tk.Label(self.window,
                                     text="Welcome to the Mock Interview.\nClick 'Next Question' to start with 10s prep time.",
                                     font=("Segoe UI", 16, "bold"), wraplength=900,
                                     fg=COLORS["text_primary"], bg=COLORS["bg_main"],
                                     pady=40, height=5)
        self.lbl_question.pack()

        # Video Preview
        self.video_frame = tk.Frame(self.window, bg=COLORS["video_border"], bd=5)
        self.video_frame.pack(pady=10)
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480, bg="black")
        self.canvas.pack()

        # Timer Display
        self.lbl_timer = tk.Label(self.window, text="Ready",
                                  font=("Consolas", 32, "bold"), fg=COLORS["timer_prep"], bg=COLORS["bg_main"])
        self.lbl_timer.pack(pady=10)

        # Button Group
        self.btn_frame = tk.Frame(self.window, bg=COLORS["bg_main"])
        self.btn_frame.pack(pady=20)

        self.btn_next = tk.Button(self.btn_frame, text="Next Question", width=20, height=2,
                                  command=self.next_question, bg=COLORS["btn_next"],
                                  fg="white", font=("Arial", 12, "bold"))
        self.btn_next.grid(row=0, column=0, padx=20)

        # Kept for manual pause if needed, but the flow is now auto
        self.btn_start = tk.Button(self.btn_frame, text="Pause/Resume", width=20, height=2,
                                   command=self.toggle_timer, bg=COLORS["btn_start"],
                                   fg="white", font=("Arial", 12, "bold"))
        self.btn_start.grid(row=0, column=1, padx=20)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _format_time(self, seconds):
        """Helper to format seconds into MM:SS"""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def next_question(self):
        """Switch question and AUTOMATICALLY start 10s prep"""
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        if not self.questions:
            messagebox.showwarning("Empty", "Question bank is empty!")
            return

        # 1. Pick next question
        idx = self.current_index % len(self.questions)
        q = self.questions[idx]
        self.lbl_question.config(text=f"Question {idx + 1} of {len(self.questions)}\n\n{q}")
        self.current_index += 1

        # 2. Set state to Preparation Phase
        self.is_prep_phase = True
        self.remaining_time = PREP_TIME_LIMIT
        self.timer_running = True

        # 3. Start countdown immediately
        self.count_down()

    def toggle_timer(self):
        """Manually toggle the countdown (Pause/Resume)"""
        if not self.timer_running:
            self.timer_running = True
            self.count_down()
        else:
            self.timer_running = False
            if self.timer_id:
                self.window.after_cancel(self.timer_id)

    def count_down(self):
        """Automated Countdown Logic (Prep -> Interview)"""
        if self.timer_running:
            if self.remaining_time > 0:
                self.remaining_time -= 1

                # Update UI based on current phase
                if self.is_prep_phase:
                    self.lbl_timer.config(text=f"Prepare: {self.remaining_time}s", fg=COLORS["timer_prep"])
                else:
                    self.lbl_timer.config(text=f"Time Left: {self._format_time(self.remaining_time)}",
                                          fg=COLORS["timer_alert"])

                self.timer_id = self.window.after(1000, self.count_down)

            else:
                # When current timer hits 0
                if self.is_prep_phase:
                    # Transition from Prep to Answer
                    self.is_prep_phase = False
                    self.remaining_time = INTERVIEW_TIME_LIMIT
                    # Optional: Sound alert or visual flash could be added here
                    self.count_down()  # Auto-start the 90s timer
                else:
                    # End of interview response
                    messagebox.showinfo("Time Up", "Your response time is over.")
                    self.timer_running = False

    def update_video(self):
        """Refresh camera feed"""
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk
        self.window.after(VIDEO_REFRESH_RATE, self.update_video)

    def on_closing(self):
        """Clean exit"""
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewSimulator(root, APP_TITLE)
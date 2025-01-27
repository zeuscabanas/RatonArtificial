from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Label

class CameraView:
    def __init__(self, window):
        self.window = window
        self.window.title("Hand Tracking Feed")
        self.video_label = Label(window)
        self.video_label.pack(padx=10, pady=10)
    
    def update_frame(self, image):
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
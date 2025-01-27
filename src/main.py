import tkinter as tk
from vista import CameraView
from controlador import AppController

if __name__ == "__main__":
    root = tk.Tk()
    view = CameraView(root)
    controller = AppController(view)
    root.mainloop()
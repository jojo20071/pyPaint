import tkinter as tk
from tkinter import Canvas, Button, Scale, HORIZONTAL

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.current_color = "black"
        self.brush_size = 2
        self.create_color_palette()
        self.create_brush_size_slider()
        self.setup_bindings()

    def create_color_palette(self):
        colors = ["black", "red", "green", "blue", "yellow", "purple"]
        for i, color in enumerate(colors):
            Button(self.root, bg=color, width=2, command=lambda c=color: self.set_color(c)).pack(side="left")

    def create_brush_size_slider(self):
        self.brush_slider = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, command=self.set_brush_size)
        self.brush_slider.pack(side="left")

    def set_color(self, color):
        self.current_color = color

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def setup_bindings(self):
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, width=self.brush_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

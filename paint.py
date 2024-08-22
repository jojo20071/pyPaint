import tkinter as tk
from tkinter import Canvas, Button, Scale, HORIZONTAL, filedialog

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.current_color = "black"
        self.brush_size = 2
        self.mode = "brush"
        self.start_x = None
        self.start_y = None
        self.create_color_palette()
        self.create_brush_size_slider()
        self.create_clear_button()
        self.create_save_button()
        self.create_shape_buttons()
        self.setup_bindings()

    def create_color_palette(self):
        colors = ["black", "red", "green", "blue", "yellow", "purple"]
        for i, color in enumerate(colors):
            Button(self.root, bg=color, width=2, command=lambda c=color: self.set_color(c)).pack(side="left")

    def create_brush_size_slider(self):
        self.brush_slider = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, command=self.set_brush_size)
        self.brush_slider.pack(side="left")

    def create_clear_button(self):
        Button(self.root, text="Clear", command=self.clear_canvas).pack(side="left")

    def create_save_button(self):
        Button(self.root, text="Save", command=self.save_canvas).pack(side="left")

    def create_shape_buttons(self):
        Button(self.root, text="Brush", command=lambda: self.set_mode("brush")).pack(side="left")
        Button(self.root, text="Line", command=lambda: self.set_mode("line")).pack(side="left")
        Button(self.root, text="Rectangle", command=lambda: self.set_mode("rectangle")).pack(side="left")

    def set_mode(self, mode):
        self.mode = mode

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.postscript(file=file_path + ".eps")
            from PIL import Image
            img = Image.open(file_path + ".eps")
            img.save(file_path, 'png')

    def set_color(self, color):
        self.current_color = color

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def setup_bindings(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def paint(self, event):
        if self.mode == "brush":
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, width=self.brush_size)

    def on_button_press(self, event):
        if self.mode in ["line", "rectangle"]:
            self.start_x = event.x
            self.start_y = event.y

    def on_button_release(self, event):
        if self.mode == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color, width=self.brush_size)
        elif self.mode == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.current_color, width=self.brush_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

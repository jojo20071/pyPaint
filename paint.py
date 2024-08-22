import tkinter as tk
from tkinter import Canvas, Button, Scale, HORIZONTAL, filedialog, font

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.current_color = "black"
        self.brush_size = 2
        self.border_color = "black"
        self.font_family = "Arial"
        self.font_size = 20
        self.mode = "brush"
        self.grid_size = 20
        self.snap_to_grid = False
        self.start_x = None
        self.start_y = None
        self.shapes = []
        self.redo_shapes = []
        self.create_color_palette()
        self.create_brush_size_slider()
        self.create_clear_button()
        self.create_save_button()
        self.create_shape_buttons()
        self.create_eraser_button()
        self.create_undo_button()
        self.create_redo_button()
        self.create_fill_tool_button()
        self.create_text_tool_button()
        self.create_font_options()
        self.create_grid_toggle_button()
        self.create_snap_to_grid_button()
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
        Button(self.root, text="Oval", command=lambda: self.set_mode("oval")).pack(side="left")

    def create_eraser_button(self):
        Button(self.root, text="Eraser", command=lambda: self.set_mode("eraser")).pack(side="left")

    def create_undo_button(self):
        Button(self.root, text="Undo", command=self.undo).pack(side="left")

    def create_redo_button(self):
        Button(self.root, text="Redo", command=self.redo).pack(side="left")

    def create_fill_tool_button(self):
        Button(self.root, text="Fill", command=lambda: self.set_mode("fill")).pack(side="left")

    def create_text_tool_button(self):
        Button(self.root, text="Text", command=lambda: self.set_mode("text")).pack(side="left")

    def create_font_options(self):
        Button(self.root, text="Arial", command=lambda: self.set_font_family("Arial")).pack(side="left")
        Button(self.root, text="Courier", command=lambda: self.set_font_family("Courier")).pack(side="left")
        Button(self.root, text="Times", command=lambda: self.set_font_family("Times")).pack(side="left")
        self.font_size_slider = Scale(self.root, from_=8, to=72, orient=HORIZONTAL, command=self.set_font_size)
        self.font_size_slider.pack(side="left")

    def create_grid_toggle_button(self):
        Button(self.root, text="Toggle Grid", command=self.toggle_grid).pack(side="left")

    def create_snap_to_grid_button(self):
        Button(self.root, text="Snap to Grid", command=self.toggle_snap_to_grid).pack(side="left")

    def set_mode(self, mode):
        self.mode = mode

    def set_font_family(self, family):
        self.font_family = family

    def set_font_size(self, size):
        self.font_size = int(size)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()
        self.redo_shapes.clear()
        if self.grid_size > 0:
            self.draw_grid()

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.postscript(file=file_path + ".eps")
            from PIL import Image
            img = Image.open(file_path + ".eps")
            img.save(file_path, 'png')

    def set_color(self, color):
        self.current_color = color

    def set_border_color(self, color):
        self.border_color = color

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def setup_bindings(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def paint(self, event):
        if self.mode == "brush":
            x1, y1 = self.snap(event.x - 1, event.y - 1)
            x2, y2 = self.snap(event.x + 1, event.y + 1)
            shape_id = self.canvas.create_oval(x1, y1, x2, y2, fill=self.current_color, width=self.brush_size)
            self.shapes.append(shape_id)
            self.redo_shapes.clear()
        elif self.mode == "eraser":
            x1, y1 = self.snap(event.x - 1, event.y - 1)
            x2, y2 = self.snap(event.x + 1, event.y + 1)
            shape_id = self.canvas.create_oval(x1, y1, x2, y2, fill="white", width=self.brush_size)
            self.shapes.append(shape_id)
            self.redo_shapes.clear()

    def on_button_press(self, event):
        if self.mode in ["line", "rectangle", "oval", "text"]:
            self.start_x, self.start_y = self.snap(event.x, event.y)

    def on_button_release(self, event):
        x, y = self.snap(event.x, event.y)
        if self.mode == "line":
            shape_id = self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.current_color, width=self.brush_size)
            self.shapes.append(shape_id)
            self.redo_shapes.clear()
        elif self.mode == "rectangle":
            shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.border_color, width=self.brush_size, fill=self.current_color)
            self.shapes.append(shape_id)
            self.redo_shapes.clear()
        elif self.mode == "oval":
            shape_id = self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.border_color, width=self.brush_size, fill=self.current_color)
            self.shapes.append(shape_id)
            self.redo_shapes.clear()
        elif self.mode == "text":
            text_font = font.Font(family=self.font_family, size=self.font_size)
            shape_id = self.canvas.create_text(self.start_x, self.start_y, text="Text", font=text_font, fill=self.current_color)
            self.shapes.append(shape_id)
            self.redo_shapes.clear()

    def snap(self, x, y):
        if self.snap_to_grid:
            return (x // self.grid_size) * self.grid_size, (y // self.grid_size) * self.grid_size
        return x, y

    def toggle_grid(self):
        if self.grid_size > 0:
            self.grid_size = 0
            self.clear_canvas()
        else:
            self.grid_size = 20
            self.draw_grid()

    def toggle_snap_to_grid(self):
        self.snap_to_grid = not self.snap_to_grid

    def draw_grid(self):
        for i in range(0, self.canvas.winfo_width(), self.grid_size):
            self.canvas.create_line(i, 0, i, self.canvas.winfo_height(), fill="lightgray")
        for i in range(0, self.canvas.winfo_height(), self.grid_size):
            self.canvas.create_line(0, i, self.canvas.winfo_width(), i, fill="lightgray")

    def undo(self):
        if self.shapes:
            shape_id = self.shapes.pop()
            self.redo_shapes.append(shape_id)
            self.canvas.delete(shape_id)

    def redo(self):
        if self.redo_shapes:
            shape_id = self.redo_shapes.pop()
            self.canvas.itemconfig(shape_id, state="normal")
            self.shapes.append(shape_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

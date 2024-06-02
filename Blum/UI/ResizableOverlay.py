import tkinter as tk
from Blum.DataBridge import DataBridge

class ResizableOverlay:
    def __init__(self, root, data_bridge: DataBridge):
        self.root = root
        self.root.title("overlay")
        self.data_bridge = data_bridge

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}')

        # Remove the titlebar and make the window transparent
        self.root.overrideredirect(True)
        self.root.attributes("-transparentcolor", "white")
        self.root.config(bg="red")

        # Make the window always on top
        self.root.wm_attributes("-topmost", 1)

        # Create a canvas for drawing the rectangle
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a red rectangle
        self.rect = self.canvas.create_rectangle(*data_bridge.rect, outline="red", width=5)

        # Bind events for resizing
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Button-1>", self.start_resize)
        self.canvas.bind("<B1-Motion>", self.do_resize)
        self.canvas.bind("<ButtonRelease-1>", self.stop_resize)

        self.resizing = False
        self.active_side = None
        self.running = True

    def on_motion(self, event):
        # Change the cursor based on position
        x, y = event.x, event.y
        if 0 <= x <= self.canvas.winfo_width() and 0 <= y <= self.canvas.winfo_height():
            if abs(x - self.canvas.coords(self.rect)[0]) < 5:
                self.canvas.config(cursor="sb_h_double_arrow")
                self.active_side = 'left'
            elif abs(x - self.canvas.coords(self.rect)[2]) < 5:
                self.canvas.config(cursor="sb_h_double_arrow")
                self.active_side = 'right'
            elif abs(y - self.canvas.coords(self.rect)[1]) < 5:
                self.canvas.config(cursor="sb_v_double_arrow")
                self.active_side = 'top'
            elif abs(y - self.canvas.coords(self.rect)[3]) < 5:
                self.canvas.config(cursor="sb_v_double_arrow")
                self.active_side = 'bottom'
            else:
                self.canvas.config(cursor="")
                self.active_side = None

    def start_resize(self, event):
        # Start resizing
        if self.active_side:
            self.resizing = True
            self.start_x = event.x
            self.start_y = event.y

    def update_rect(self):
        self.canvas.coords(self.rect, *self.data_bridge.rect)

    def do_resize(self, event):
        if self.resizing:
            cur_x, cur_y = event.x, event.y
            coords = self.canvas.coords(self.rect)

            if self.active_side == 'left':
                new_x1 = max(0, min(coords[2] - 10, cur_x))
                self.canvas.coords(self.rect, new_x1, coords[1], coords[2], coords[3])
            elif self.active_side == 'right':
                new_x2 = min(self.canvas.winfo_width(), max(coords[0] + 10, cur_x))
                self.canvas.coords(self.rect, coords[0], coords[1], new_x2, coords[3])
            elif self.active_side == 'top':
                new_y1 = max(0, min(coords[3] - 10, cur_y))
                self.canvas.coords(self.rect, coords[0], new_y1, coords[2], coords[3])
            elif self.active_side == 'bottom':
                new_y2 = min(self.canvas.winfo_height(), max(coords[1] + 10, cur_y))
                self.canvas.coords(self.rect, coords[0], coords[1], coords[2], new_y2)

            self.start_x, self.start_y = cur_x, cur_y

        self.data_bridge.rect = self.canvas.coords(self.rect)

    def stop_resize(self, event):
        # Stop resizing
        self.resizing = False

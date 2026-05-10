import tkinter as tk

class OvalButton:
    def __init__(self, parent, text, command, bg="#C8D9BD", fg="black", font=("Arial", 12), width=160, height=45):
        self.command = command
        self.bg = bg
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.oval = self.canvas.create_oval(2, 2, width-2, height-2, fill=bg, outline=bg)
        self.label = self.canvas.create_text(width//2, height//2, text=text, font=font, fill=fg)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def _on_click(self, e):
        self.command()

    def _on_enter(self, e):
        self.canvas.itemconfig(self.oval, fill="#a8c89a")

    def _on_leave(self, e):
        self.canvas.itemconfig(self.oval, fill=self.bg)
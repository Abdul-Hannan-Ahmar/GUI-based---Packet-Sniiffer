import tkinter as tk
from tkinter import ttk
from scapy.all import get_if_list
import threading as T
import time

from app.widgets import OvalButton
from app.sniffer import start_sniff, parse_packet


class myGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.config(background="#FFEE8C")
        self.root.geometry("1920x1080")

        self._build_left_panel()
        self._build_right_panel()

        self.sniffThread = None
        self.speed = 1

        self.root.mainloop()

    def _build_left_panel(self):
        self.LeftFrame = tk.Frame(self.root, background="#C3B1E1", width=432, height=720)
        self.LeftFrame.pack(side="left", fill="y")
        self.LeftFrame.pack_propagate(False)

        self._build_interface_buttons()
        self._build_control_buttons()

    def _build_interface_buttons(self):
        self.upper = tk.Frame(self.LeftFrame, background="#C3B1E1", width=432, height=360)
        self.upper.pack(side="top", fill="x")
        self.upper.pack_propagate(False)

        self.upper.grid_rowconfigure((0, 1, 2), weight=1)
        self.upper.grid_columnconfigure(0, weight=1)

        interfaces = get_if_list()
        for i, iface in enumerate(interfaces[:3]):
            btn = OvalButton(
                self.upper, text=iface,
                command=lambda x=iface: self.start_interface(x),
                bg="#C8D9BD", font=("Arial", 12), width=180, height=50
            )
            btn.grid(row=i, column=0, padx=40, pady=(80 if i == 0 else 15, 15))

    def _build_control_buttons(self):
        self.lower = tk.Frame(self.LeftFrame, background="#C3B1E1", width=432, height=360)
        self.lower.pack(side="bottom", fill="x")
        self.lower.pack_propagate(False)

        self.lower.grid_rowconfigure((0, 1, 2), weight=1)
        self.lower.grid_columnconfigure((0, 1, 2), weight=1)

        OvalButton(self.lower, text="Slow", command=lambda: self.sniff_speed(True),
                   bg="#EDE8D0", width=100, height=45).grid(row=1, column=0, padx=20, pady=15)

        OvalButton(self.lower, text="Play", command=self.play,
                   bg="#EDE8D0", width=100, height=45).grid(row=0, column=1, padx=20, pady=(20, 15))

        OvalButton(self.lower, text="Pause", command=self.pause,
                   bg="#EDE8D0", width=100, height=45).grid(row=2, column=1, padx=20, pady=(15, 80))

        OvalButton(self.lower, text="Fast", command=lambda: self.sniff_speed(False),
                   bg="#EDE8D0", width=100, height=45).grid(row=1, column=2, padx=20, pady=15)

    def _build_right_panel(self):
        self.RightFrame = tk.Frame(self.root, background="#FFEE8C", width=648, height=720)
        self.RightFrame.pack(side="right", fill="both", expand=True)

        tk.Label(self.RightFrame, background="#FFEE8C", text="Packet Sniffer",
                 font=("Arial", 30)).pack(pady=20, anchor="n")

        columns = ("Source IP_address", "Destination IP_address", "Protocol", "Flag")
        self.table = ttk.Treeview(self.RightFrame, columns=columns, show="headings", height=10000000)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=250, anchor="center")

        self.table.pack(padx=40, pady=(0, 40))

    def start_interface(self, iface):
        if self.sniffThread and self.sniffThread.is_alive():
            return
        self.sniffThread = T.Thread(
            target=start_sniff,
            args=(iface, self.on_packet),
            daemon=True
        )
        self.sniffThread.start()

    def on_packet(self, packet):
        result = parse_packet(packet)
        if result:
            time.sleep(self.speed)
            self.root.after(0, self.add_to_table, *result)

    def add_to_table(self, src, dst, proto, flags):
        self.table.insert('', 'end', values=(src, dst, proto, flags))

    def sniff_speed(self, slow):
        self.speed = self.speed * 10 if slow else self.speed / 10

    def play(self):
        pass  # implement resume logic here

    def pause(self):
        pass  # implement pause logic here
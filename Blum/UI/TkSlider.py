import tkinter as tk
from tkinter import ttk
from Blum.DataBridge import DataBridge


class TkFloatSlider:
    def __init__(self, master, title, data_bridge: DataBridge, data_name,
                 from_=0, to=100, initial_value=50, **kwargs):
        self.db = data_bridge
        self.data_name = data_name

        self.frame = ttk.Frame(master)
        self.frame.pack(pady=10)

        self.title_label = ttk.Label(self.frame, text=title)
        self.title_label.pack(side='top', pady=5)

        self.value_var = tk.DoubleVar(value=initial_value)

        self.slider = ttk.Scale(self.frame, from_=from_, to=to, orient='horizontal',
                                command=self.on_slider_change, **kwargs)
        self.slider.pack(side='left', padx=5)
        self.slider.set(initial_value)

        self.entry = ttk.Entry(self.frame, textvariable=self.value_var, width=5)
        self.entry.pack(side='left', padx=5)

        self.value_var.trace_add('write', self.on_entry_change)

    def on_slider_change(self, value):
        self.db.__setattr__(self.data_name, round(float(value), 2))
        self.value_var.set(round(float(value), 2))

    def on_entry_change(self, *args):
        try:
            self.slider.set(self.value_var.get())
        except tk.TclError:
            pass

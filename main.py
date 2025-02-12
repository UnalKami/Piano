import tkinter as tk
import winsound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class notes:
    def __init__(self, parent):
        self.frec = {
            "C4": 261.63,   # Do4
            "C#4": 277.18,  # Do#4 / Reb4
            "D4": 293.66,   # Re4
            "D#4": 311.13,  # Re#4 / Mib4
            "E4": 329.63,   # Mi4
            "F4": 349.23,   # Fa4
            "F#4": 369.99,  # Fa#4 / Solb4
            "G4": 392.00,   # Sol4
            "G#4": 415.30,  # Sol#4 / Lab4
            "A4": 440.00,   # La4 
            "A#4": 466.16,  # La#4 / Sib4
            "B4": 493.88    # Si4
            }
        self.plot_enabled = True
        self.frequencies = []
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().grid(row=3, columnspan=7, sticky="nsew")

    def play_note(self, note):
        winsound.Beep(int(self.frec[note]), 1000)
        if self.plot_enabled:
            self.frequencies.append(self.frec[note])
            self.plot_wave()

    def plot_wave(self):
        t = np.linspace(0, len(self.frequencies), 100 * len(self.frequencies))
        wave = np.concatenate([np.sin(2 * np.pi * freq * t[i*100:(i+1)*100]) for i, freq in enumerate(self.frequencies)])

        self.ax.clear()  # Limpiar el eje antes de volver a dibujar
        self.ax.plot(t, wave)
        self.ax.set_title("Waveform of Played Notes")
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.canvas.draw()

    def toggle_plot(self, button):
        self.plot_enabled = not self.plot_enabled
        button.config(text="Desactivar gráfica" if self.plot_enabled else "Activar gráfica")

class app:
    def __init__(self):
        self.window = tk.Tk()
        self.notes = notes(self.window)
        self.white_keys = ["C4","D4","E4","F4","G4","A4","B4"]
        self.black_keys = ["C#4","D#4","F#4","G#4","A#4"]   
        self.key_mapping = {
            "a": "C4",
            "w": "C#4",
            "s": "D4",
            "e": "D#4",
            "d": "E4",
            "f": "F4",
            "t": "F#4",
            "g": "G4",
            "y": "G#4",
            "h": "A4",
            "u": "A#4",
            "j": "B4"
        }

    def draw_keys(self):
        for i, key in enumerate(self.white_keys):
            button = tk.Button(self.window, text = key, bd = 12, width = 9, height = 12, font = ("arial", 16, "bold"))
            button.grid(row = 1, column = i, sticky = "nsew")
            button.config(command = lambda note = key: self.notes.play_note(note))

        for i, key in enumerate(self.black_keys):
            button = tk.Button(self.window, text = key, bd = 12, width = 5, height = 9, bg = "black", fg= "white", font = ("arial", 16, "bold"))
            button.grid(row = 0, column = i*2, sticky = "nsew", padx = (0,2))
            button.config(command = lambda note = key: self.notes.play_note(note))
        
        toggle_button = tk.Button(self.window, text = "Desactivar gráfica" if self.notes.plot_enabled else "Activar gráfica", command = lambda: self.notes.toggle_plot(toggle_button))
        toggle_button.grid(row = 2, columnspan = 7, sticky = "nsew")

        self.window.title("TeoInfo Piano")
        self.window.grid_rowconfigure(0, weight = 1)
        self.window.grid_rowconfigure(1, weight = 1)
        self.window.grid_rowconfigure(2, weight = 1)
        self.window.grid_columnconfigure(list(range(1, 16, 21)), weight = 1)

        self.window.bind("<KeyPress>", self.on_key_press)
        self.window.mainloop()

    def on_key_press(self, event):
        note = self.key_mapping.get(event.char)
        if note:
            self.notes.play_note(note)
    
if __name__ == "__main__":
    app = app()
    app.draw_keys()

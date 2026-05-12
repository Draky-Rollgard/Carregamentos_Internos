import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np


class GraficoCortante:

    def __init__(self, frame):

        self.fig = Figure(figsize=(5, 3), dpi=100)

        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.plotar()


    def plotar(self):

        x = np.array([0,2,2,6,6,10])

        y = np.array([0,0,-5,-5,-2,-2])

        self.ax.clear()

        self.ax.plot(
            x,
            y
        )

        self.ax.fill_between(
            x,
            y,
            alpha=0.3
        )

        self.ax.axhline(
            0,
            color='black'
        )

        self.ax.set_title(
            "Diagrama de Força Cortante"
        )

        self.ax.set_xlabel("x (m)")

        self.ax.set_ylabel("V (N)")

        self.ax.grid(True)

        self.canvas.draw()


class GraficoMomento:

    def __init__(self, frame):

        self.fig = Figure(figsize=(5, 3), dpi=100)

        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.plotar()


    def plotar(self):

        x = np.linspace(0, 10, 100)

        y = -((x - 5)**2) + 25

        self.ax.clear()

        self.ax.plot(
            x,
            y
        )

        self.ax.fill_between(
            x,
            y,
            alpha=0.3
        )

        self.ax.axhline(
            0,
            color='black'
        )

        self.ax.set_title(
            "Diagrama de Momento Fletor"
        )

        self.ax.set_xlabel("x (m)")

        self.ax.set_ylabel("M (N.m)")

        self.ax.grid(True)

        self.canvas.draw()
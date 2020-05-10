"""Main module.  Runs the dialog."""
import PySimpleGUI as sg
from bearing.angle import Bearing
import pyperclip
import math
import webbrowser

DEGREE = u"\N{DEGREE SIGN}"
SIZE_X = 200
SIZE_Y = 200
NUMBER_MARKER_FREQUENCY = 25


class UI:
    def __init__(self):
        """
        Run the user interface using PySimpleGUI
        """

        # Theme must be defined before layout
        # Reddit, SandyBeach, LightBrown1, SystemDefaultForReal, LightBrown12
        sg.theme("SystemDefaultForReal")
        self.canvas = sg.Graph(
            canvas_size=[SIZE_X * 2, SIZE_Y * 2],
            graph_top_right=[100, 100],
            graph_bottom_left=[-100, -100],
            key="graph",
        )

        layout = [
            [sg.Text("Bearing:")],
            [
                sg.Spin(
                    values=["S", "N"],
                    initial_value="N",
                    key="northing",
                    enable_events=True,
                ),
                sg.Input("00", size=(2, 1), key="degree", enable_events=True,),
                sg.Text(DEGREE, size=(1, 1)),
                sg.Input("00", size=(2, 1), key="minute", enable_events=True,),
                sg.Text("'", size=(1, 1)),
                sg.Input("00", size=(2, 1), key="second", enable_events=True,),
                sg.Text('"', size=(1, 1)),
                sg.Spin(
                    values=["W", "E"],
                    initial_value="E",
                    key="easting",
                    enable_events=True,
                ),
            ],
            [sg.Text("Azimuth:")],
            [sg.Input("0.0", size=(15, 2), key="azimuth", enable_events=True,)],
            [
                sg.Button("Copy Bearing", key="copy_bear"),
                sg.Button("Copy Azimuth", key="copy_az"),
                sg.Button("Docs", key="docs"),
                sg.Button("Exit"),
            ],
            [self.canvas],
        ]

        window = sg.Window("Bearing - Azimuth", layout, font=("Ubuntu", 16))
        self.direction = Bearing()

        # Event dispatch handler
        while True:
            event, values = window.read()

            if event in (None, "Exit"):
                break
            elif event in ("northing", "degree", "minute", "second", "easting"):
                angle = self.direction.submit_bearing(
                    values["northing"],
                    values["degree"],
                    values["minute"],
                    values["second"],
                    values["easting"],
                )

                window["azimuth"].update(angle)

            elif event == "azimuth":
                bear = self.direction.submit_azimuth(values["azimuth"])
                window["northing"].update(bear["northing"])
                window["degree"].update(bear["degrees"])
                window["minute"].update(bear["minutes"])
                window["second"].update(bear["seconds"])
                window["easting"].update(bear["easting"])
            elif event == "copy_bear":
                value = self.direction.get_bearing()
                pyperclip.copy(value)
            elif event == "copy_az":
                value = str(self.direction.get_azimuth())
                pyperclip.copy(value)
            elif event == "docs":
                webbrowser.open("https://bearingazimuth.readthedocs.io/en/latest/")
            self.canvas.erase()
            self.draw_axis()
            self.draw_vector()

        window.close()

    def draw_axis(self):
        """
        Draws the X and Y axis on the canvas for the graphical representation of
        the angle.
        """
        self.canvas.draw_line((-90, 0), (90, 0), color="blue")  # axis lines
        self.canvas.draw_line((0, -90), (0, 90), color="blue")
        self.canvas.draw_text("E", location=(95, 0), color="blue")
        self.canvas.draw_text("W", color="blue", location=(-95, 0))
        self.canvas.draw_text("N", color="blue", location=(0, 95))
        self.canvas.draw_text("S", color="blue", location=(0, -95))

    def draw_vector(self):
        """
        Draws the angle on the canvas.  Adds a little arc to illustrate.
        """
        angle = self.direction.get_azimuth()
        radians = math.radians(angle)
        x = y = 0
        end_x = x + 90 * math.sin(radians)
        end_y = y + 90 * math.cos(radians)

        self.canvas.draw_arc(
            top_left=(-50, 50),
            bottom_right=(50, -50),
            start_angle=90,
            extent=angle * -1,
            arc_color="green",
        )
        self.canvas.draw_line((x, y), (end_x, end_y), color="red", width=2)


if __name__ == "__main__":
    UI()

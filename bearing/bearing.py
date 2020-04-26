"""Main module."""
import PySimpleGUI as sg
from angle import Bearing
import pyperclip

DEGREE = u'\N{DEGREE SIGN}'


class UI:
    def __init__(self):
        """
        Run the user interface
        """

        # Theme must be defined before layout
        # Reddit, SandyBeach, LightBrown1, SystemDefaultForReal, LightBrown12
        sg.theme('SystemDefaultForReal')
        canvas = [sg.Graph(canvas_size=[200, 200],
                           graph_top_right=[100, 100],
                           graph_bottom_left=[-100, -100],
                           key="graph")
                  ]
        layout = [
            [sg.Text('Bearing:')],
            [
                sg.Spin(values=['S', 'N'], initial_value='N', key='northing', enable_events=True, ),
                sg.Input('00', size=(2, 1), key='degree', enable_events=True, ),
                sg.Text(DEGREE, size=(1, 1)),
                sg.Input('00', size=(2, 1), key='minute', enable_events=True, ),
                sg.Text('\'', size=(1, 1)),
                sg.Input('00', size=(2, 1), key='second', enable_events=True, ),
                sg.Text('"', size=(1, 1)),
                sg.Spin(values=['W', 'E'], initial_value='E', key='easting', enable_events=True, ),
            ],
            [sg.Text('Azimuth:')],
            [
                sg.Input('0.0', size=(15, 2), key='azimuth', enable_events=True, )
            ],
            [sg.Button('Copy Bearing', key="copy_bear"), sg.Button('Copy Azimuth', key="copy_az"),
             sg.Button('Exit')]

        ]

        window = sg.Window("Bearing - Azimuth", layout, font=('Ubuntu', 16))
        direction = Bearing()

        # Event dispatch handler
        while True:
            event, values = window.read()
            if event in (None, "Exit"):
                break
            elif event in ("northing", "degree", "minute", "second", "easting"):
                angle = direction.submit_bearing(values["northing"], values["degree"],
                                                 values["minute"],
                                                 values["second"], values["easting"])

                window["azimuth"].update(angle)

            elif event == "azimuth":
                bear = direction.submit_azimuth(values["azimuth"])
                window["northing"].update(bear["northing"])
                window["degree"].update(bear["degrees"])
                window["minute"].update(bear["minutes"])
                window["second"].update(bear["seconds"])
                window["easting"].update(bear["easting"])
            elif event == "copy_bear":
                value = direction.get_bearing()
                pyperclip.copy(value)
            elif event == "copy_az":
                value = str(direction.get_azimuth())
                pyperclip.copy(value)

        window.close()


if __name__ == "__main__":
    UI()

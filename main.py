import PySimpleGUI as sg
from pycaw.pycaw import AudioUtilities
import os, time
import json


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.

sessions = AudioUtilities.GetAllSessions()
sessions_list = []
for session in sessions:
    try:
        session.Process.name()
        sessions_list.append(session)
    except:
        pass

layout = [  [[sg.Text(session.Process.name()), sg.InputText()] for session in sessions_list],
            [sg.Button('Okay'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Vile', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print(event, values)
window.close()
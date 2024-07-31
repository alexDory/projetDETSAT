'''
Ce script permet d'afficher des graphs en temps réel de la capture en EL.
Decomenter les #Graphs dans mainGUI.py
Fermer la fenetre pour continuer le balayage
'''

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import PySimpleGUI as sg


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def graph(ps) :
    NUM_DATAPOINTS = 100
    # define the form layout
    layout = [[sg.Text('Animated Matplotlib', size=(40, 1),
                justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS-')],
              [sg.Text('Progress through the data')],
              [sg.Slider(range=(0, NUM_DATAPOINTS), size=(60, 10),
                orientation='h', key='-SLIDER-')],
              [sg.Text('Number of data points to display on screen')],
               [sg.Slider(range=(10, 500), default_value=40, size=(40, 10),
                    orientation='h', key='-SLIDER-DATAPOINTS-')],
              [sg.Button('Exit', size=(10, 1), pad=((280, 0), 3), font='Helvetica 14')]]

    # create the form and show it without the plot
    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
                layout, finalize=True)

    canvas_elem = window['-CANVAS-']
    slider_elem = window['-SLIDER-']
    canvas = canvas_elem.TKCanvas

    # draw the initial plot in the window
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-50,50)
    ax.set_ylim(-40,15)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()
    fig_agg = draw_figure(canvas, fig)  
    data_points = [ele[0] for ele in ps ]
    dpts_corrected = [power[1] for power in ps]
    # dpts_corrected = savgol_filter(dpts_corrected,8,1,mode = 'nearest')
    for i in range(len(data_points)):

        event, values = window.read(timeout=1)
        if event in ('Exit', None):
            exit(69)
        slider_elem.update(i)       # slider shows "progress" through the data points
        ax.plot(data_points[:i],dpts_corrected[:i],  color='purple')
        fig_agg.draw()
    window.read(close=True)

    return
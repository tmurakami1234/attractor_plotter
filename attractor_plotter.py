import tkinter, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse

def parse_arguments():
    lorenz_attractor = [10.,28.,8./3]
    rossler_attractor = [0.2, 0.2, 5.7]
    multiscroll_attractor = [19., 1.2, 14.5]
    brusselator_attractor = [1,3,0]
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--par', nargs=3, type=float, default=multiscroll_attractor, metavar=('p', 'r', 'b'), help='')
    parser.add_argument('--init-var', nargs=3, type=float, default=[10.,20.,30.], metavar=('x', 'y', 'z'), help='')
    parser.add_argument('--step-width', type=float, default=0.005, metavar='FLOAT', help='')
    parser.add_argument('--start-time', type=float, default=0., metavar='FLOAT', help='')
    parser.add_argument('--end-time', type=float, default=100., metavar='FLOAT', help='')
    args = parser.parse_args()
    return args

def derivative_of_x_wrt_t(variables, time, parameters):
    p = parameters[:]
    v = variables[:]
    t = time
    lorenz_eq = p[0]*(v[1]-v[0])
    rossler_eq = -v[1]-v[2]
    multiscroll_eq = p[0]*(v[1]-v[0])
    brusselator_eq = p[0]+v[0]**2*v[1]-(p[1]+1)*v[0]
    #return lorenz_eq
    #return rossler_eq
    return multiscroll_eq
    #return brusselator_eq

def derivative_of_y_wrt_t(variables, time, parameters):
    p = parameters[:]
    v = variables[:]
    t = time
    lorenz_eq = v[0]*(p[1]-v[2])-v[1]
    rossler_eq = v[0]+p[0]*v[1]
    multiscroll_eq = (p[2]-p[0]-v[2])*v[0]+p[2]*v[1]
    brusselator_eq = p[1]*v[0]-v[0]**2*v[1]
    #return lorenz_eq
    #return rossler_eq
    return multiscroll_eq
    #return brusselator_eq

def derivative_of_z_wrt_t(variables, time, parameters):
    p = parameters[:]
    v = variables[:]
    t = time
    lorenz_eq = v[0]*v[1]-p[2]*v[2]
    rossler_eq = p[1]+(v[0]-p[2])*v[2]
    multiscroll_eq = v[0]*v[1]-p[1]*v[2]
    brusselator_eq = 0
    #return lorenz_eq
    #return rossler_eq
    return multiscroll_eq
    #return brusselator_eq

def differential_eq(variables, time, parameters):
    return np.array([derivative_of_x_wrt_t(variables, time, parameters),
                     derivative_of_y_wrt_t(variables, time, parameters),
                     derivative_of_z_wrt_t(variables, time, parameters)])

def runge_kutta_4(variables, parameters, step_width, start_time, end_time):
    v = np.array(variables)
    p = np.array(parameters)
    t = start_time
    h = step_width
    n = int((end_time - start_time)/float(step_width))

    variable_list = [np.array(v)]
    time_list = [t]
    for i in range(1, n):
        k1 = differential_eq(v, t, p)
        k2 = differential_eq(v+k1*h*0.5, t+0.5*h, p)
        k3 = differential_eq(v+k2*h*0.5, t+0.5*h, p)
        k4 = differential_eq(v+k3*h, t+h, p)
        v += (k1+2*k2+2*k3+k4)*h/6.0    
        #v = [e if e > 0.0 else 0.0 for e in v]
        t += h
        variable_list.append(np.array(v))
        time_list.append(t)
    return variable_list, time_list

def plot_image(n):
    ax1.cla()
    ax2.cla()
    var = [variable1.get(), variable2.get(), variable3.get()]
    par = [parameter1.get(), parameter2.get(), parameter3.get()]
    variable_list, time_list = runge_kutta_4(var, par, args.step_width, start_time.get(), end_time.get())
    variable_list = np.array(variable_list)
    x_list = variable_list[:,0]
    y_list = variable_list[:,1]
    z_list = variable_list[:,2]

    ax1.grid(True)
    ax1.set_xlabel("time")
    ax1.set_ylabel("value of variable")
    ax1.plot(time_list, x_list, label = "x", linewidth=0.75)
    ax1.plot(time_list, y_list, label = "y", linewidth=0.75)
    ax1.plot(time_list, z_list, label = "z", linewidth=0.75)
    ax1.legend(loc='upper right')
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel(f"z")
    ax2.plot(x_list, y_list, z_list, linewidth=0.75)
    canvas.draw()

def set_widget(frame, row, column, resolution, variable_range, entry_label, variable_initial, variable_type = 'int'):
    variable = tkinter.IntVar() if variable_type == 'int' else tkinter.DoubleVar()
    variable.set(variable_initial)
    variable_label = tkinter.Label(frame, text=entry_label)
    variable_entry = tkinter.Entry(frame, width = 5)
    variable_scale = tkinter.Scale(frame, from_ = variable_range[0], to = variable_range[1],
                                   resolution = resolution, orient = "h",
                                   tickinterval = (variable_range[0]-variable_range[1])/5.0,
                                   length = 300, variable = variable,
                                   command = plot_image)
    variable_label.grid(row=row, column=column)
    variable_scale.grid(row=row, column=column+1)
    variable_entry.grid(row=row, column=column+3)
    return variable, variable_entry, variable_scale
    
def keep_parameter():
    start_time_entry.delete(0, tkinter.END)
    start_time_entry.insert(tkinter.END, start_time.get())
    end_time_entry.delete(0, tkinter.END)
    end_time_entry.insert(tkinter.END, end_time.get())
    parameter1_entry.delete(0, tkinter.END)
    parameter1_entry.insert(tkinter.END, parameter1.get())
    parameter2_entry.delete(0, tkinter.END)
    parameter2_entry.insert(tkinter.END, parameter2.get())
    parameter3_entry.delete(0, tkinter.END)
    parameter3_entry.insert(tkinter.END, parameter3.get())
    variable1_entry.delete(0, tkinter.END)
    variable1_entry.insert(tkinter.END, variable1.get())
    variable2_entry.delete(0, tkinter.END)
    variable2_entry.insert(tkinter.END, variable2.get())
    variable3_entry.delete(0, tkinter.END)
    variable3_entry.insert(tkinter.END, variable3.get())
    
def set_parameter():
    start_time.set(start_time_entry.get())
    end_time.set(end_time_entry.get())
    parameter1.set(parameter1_entry.get())
    parameter2.set(parameter2_entry.get())
    parameter3.set(parameter3_entry.get())
    variable1.set(variable1_entry.get())
    variable2.set(variable2_entry.get())
    variable3.set(variable3_entry.get())
    plot_image(0)

if __name__=="__main__":
    args = parse_arguments()
    
    root = tkinter.Tk()
    root.title("Sample")
    frame1 = tkinter.Frame(root)
    frame2 = tkinter.Frame(root)
    
    fig = Figure(figsize=(12,5))
    canvas = FigureCanvasTkAgg(fig, master=frame1)
    canvas.get_tk_widget().grid(row=5, column=0)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122,projection = "3d")
    
    set_parameter_button = tkinter.Button(frame2, text="set <=", width=5, command=set_parameter)
    keep_parameter_button = tkinter.Button(frame2, text="keep =>", width=5, command=keep_parameter)   
    keep_parameter_button.grid(row=1, column=2, rowspan=2)
    set_parameter_button.grid(row=5, column=2, rowspan=2)
    
    start_time, start_time_entry, start_time_scale = set_widget(frame2,0,0,1,[0,1000],'start time',args.start_time, 'double')
    end_time, end_time_entry, end_time_scale = set_widget(frame2, 1,0,1,[0,1000],'end time',args.end_time, 'double')
    parameter1, parameter1_entry, parameter1_scale = set_widget(frame2,2,0,0.01,[-50,50],'parameter 1',args.par[0], 'double')
    parameter2, parameter2_entry, parameter2_scale = set_widget(frame2,3,0,0.01,[-50,50],'parameter 2',args.par[1], 'double')
    parameter3, parameter3_entry, parameter3_scale = set_widget(frame2,4,0,0.01,[-50,50],'parameter 3',args.par[2], 'double')
    variable1, variable1_entry, variable1_scale = set_widget(frame2,5,0,0.01,[-50,50],'initial x',args.init_var[0], 'double')
    variable2, variable2_entry, variable2_scale = set_widget(frame2,6,0,0.01,[-50,50],'initial y',args.init_var[1], 'double')
    variable3, variable3_entry, variable3_scale = set_widget(frame2,7,0,0.01,[-50,50],'initial z',args.init_var[2], 'double')

    plot_image(0)

    sys.setrecursionlimit(10000)
    
    frame2.grid(row=0, column=0, pady=10, padx=10)
    frame1.grid(row=0, column=1, pady=10, padx=10)
    root.mainloop()

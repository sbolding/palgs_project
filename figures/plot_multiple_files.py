import numpy as np
import matplotlib.pyplot as plt
import re
from sys import argv
from pylab import *

def main():

    #labels
    labels = ["Serial", "Domain Copy", "Domain Decomp."]
    symbols = ["-b", "g--", "r-", "g--"]

    #get plottable data
    x_data   = [[] for i in xrange(3)]
    y_data   = [[] for i in xrange(3)]
     
    f = open('raw_data','r')

    for line in f:
        d = line.split()
        print d
        if len(d) > 0:
            xline = [float(d[0]), float(d[2]), float(d[4])]
            yline = [float(d[1]), float(d[3]), float(d[5])]
            for i in range(3):
                x_data[i].append(xline[i])
                y_data[i].append(yline[i])

    print x_data, y_data
    
        
    #plot some stuff
    figure(0)
    plt.xlabel('$x$ (cm)')
    plt.ylabel('$\phi(x)$ (cm$^{-2}$ s$^{-1}$)')
    plt.title('Comparison of Scalar Flux Solutions') 

    for i in range(len(x_data)):

        plt.plot(x_data[i], y_data[i], symbols[i], label=labels[i])

    #plt.plot(x_c, mat_t, "-b", label="$T_m$ HOLO-ECMC", linewidth=1.0)

    plt.axis([min(x_data[0]), max(x_data[0])*1.001,
        min(min(y_data[-1]),-0.001), max(y_data[-1])*1.1])
    l = plt.legend(loc='lower right', prop={'size':11})
    l.draw_frame(False)
 #   plt.savefig(ofile_name.replace(".pdf","_"+str(counter)+".pdf"), bbox_inches='tight')
    plt.savefig('solutions.pdf', bbox_inches='tight')
    plt.show()


def plot_holo_file(f_name, t_step=-1):

    infile = open(f_name, "r")

    #x_coords hardcoded
    rad_t = []
    mat_t = []
    times = []
    locations = []

    new_data = False

    #find all possible time steps
    for line in infile:
        if re.search("The time at",line):
            times.append(float(line.split()[8]))
            locations.append(infile.tell())
        else:
            continue

    #interactively plot a time step
    counter = 0
    plt.ion()
    if (t_step == -1):
        step = len(times)-1
    #get the data
    rad_t =[]
    mat_t = []
    x_coords = []
    if step==0:
        infile.seek(0)
    elif step < -1:
        exit()
    else:
        i =1
        while True:
            if step-i < 0:
                infile.seek(0)
                break
            if (locations[step-i] == locations[step]):
                i+=1
            else:
                infile.seek(locations[step-i])
                break

    new_data = False

    for line in infile:

       if re.search("The time at",line):
           t = (float(line.split()[8]))
           if t ==times[step]:
               new_data = True
       if new_data == True:
           if (re.search("^\s*\d+\.\d+\S+\s+",line)):
               if re.search("nan",line.split()[1]):
                   rad_t.append(0.0)
               else: 
                   rad_t.append(float(line.split()[1]))
               mat_t.append(float(line.split()[2]))
               x_coords.append(float(line.split()[0]))
           if re.search("Solving the low", line) or re.search("HOLO",line) or re.search("End of Data",line):
               new_data = False
               break

    if step < -1:
        exit()
    x_c = x_coords;
    time = times[step]

    #plot the centers
    #////////////////////////////////////////////////
    x_c = []
    rad_c = []
    mat_c = []
    for i in range(0,len(x_coords),2):
        rad_c.append(0.5*(rad_t[i]+rad_t[i+1]))
        mat_c.append(0.5*(mat_t[i]+mat_t[i+1]))
        x_c.append(0.5*(x_coords[i]+x_coords[i+1]))

    mat_t = mat_c
    rad_t = rad_c
    #////////////////////////////////////////////////

    return x_c, rad_t, mat_t, time
   



if __name__ == "__main__":
    main()



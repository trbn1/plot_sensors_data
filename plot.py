##plot data from .csv files
import argparse
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

#define
working_dir = '.'
file_ext = '.csv'
newline = ''
verify_h = "['timestamp', 'x', 'y', 'z']"
new_header = ['timestamp','x', 'y', 'z']

label_x = 'x'
label_y = 'y'
label_z = 'z'

width = 10
height = 2
fig_dpi = 100
line_width = 0.5

legend_loc = 'lower right'

acc = "acc.csv"
gyro = "gyro.csv"
lin = "linAcc.csv"

#parse cmd line arguments
parser = argparse.ArgumentParser(description='Plot data from .csv files. To use, place .csv files in any folder/subfolder.')
parser.add_argument("-pw", "--width", metavar='N', dest='pw', nargs='?', help="plot width", type=int, default=width)
parser.add_argument("-ph", "--height", metavar='N', dest='ph', nargs='?', help="plot height", type=int, default=height)
parser.add_argument("-dpi", metavar='N', nargs='?', dest='dpi', help="plot DPI", type=int, default=fig_dpi)
parser.add_argument("-lw", "--linewidth", metavar='N', dest='lw', nargs='?', help="line width", type=float, default=line_width)
args = parser.parse_args()
width = args.pw
heigth = args.ph
fig_dpi = args.dpi
line_width = args.lw

#verify/add header to .csv files
for directory, subdirectories, files in os.walk(working_dir):
    for file in files:
        if not file.endswith(file_ext):
            continue
        file2 = os.path.join(directory, file)
        with open(file2,newline=newline) as f:
            r = csv.reader(f)
            h = next(r)
            if not verify_h == h:
                data = [line for line in r]
                with open(file2,'w',newline=newline) as f:
                    w = csv.writer(f)
                    w.writerow(new_header)
                    w.writerows(data)

        #read .csv files and create plots
        df = pd.read_csv(file2)
        plot_data = df[label_x]
        plot_data2 = df[label_y]
        plot_data3 = df[label_z]
        plt.figure(figsize=(width,heigth), dpi=fig_dpi)
        plt.plot(plot_data, label=label_x, linewidth=line_width)
        plt.plot(plot_data2, label=label_y, linewidth=line_width)
        plt.plot(plot_data3, label=label_z, linewidth=line_width)
        plt.legend(loc=legend_loc)

        #correctly label each plot
        if gyro == file:
            plt.xlabel('Index')
            plt.ylabel('Rate of rotation [rad/s]')
            plt.title('Gyroscope')

        if acc == file:
            plt.xlabel('Index')
            plt.ylabel('Acceleration [m/s2]')
            plt.title('Accelerometer')

        if lin == file:
            plt.xlabel('Index')
            plt.ylabel('Acceleration [m/s2]')
            plt.title('Linear Acceleration')

        #save to .png
        png = file2[:-4] + ".png"
        plt.savefig(png)
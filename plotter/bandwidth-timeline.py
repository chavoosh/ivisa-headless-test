#!/usr/bin/python
#=============================================================
# DESCRIPTION:
# Feed this file with the collected log file of pupeteer script.
#
# The output is a plot, showing the bandwidth changes during
# playing back the video.
#
# author: Chavoosh Ghasemi <chghasemi@cs.arizona.edu>
#=============================================================

import os
import sys
import getopt
import subprocess

ndn_log_file = ""
ip_log_file  = ""

ndn_bw = []
ip_bw  = []

ndn_data = "ndn-data.txt"
ip_data  = "ip-data.txt"

def print_help():
    print "program usage:\n\tpython bandwidth-timeline.py\n",\
          "\t-n: ndn log file\n",\
          "\t-p: ip log file\n"
    sys.exit(2)


# =============
#    Input
# =============
if len(sys.argv) == 1:
    print_help()
try:
    opts, args = getopt.getopt(sys.argv[1:], "p:n:")
except getopt.GetoptError:
    print_help()

if len(opts) == 0:
    print_help()

for opt, arg in opts:
    if opt == '-n':
        ndn_log_file = arg
    elif opt == '-p':
        ip_log_file = arg
    else:
         print_help()

# =========================================================
# Extract the desired information from the input log file
# and put it in arg.
#
# @log_file Name of the log_file to process
# @arg The array to put the extracted information inside
# =========================================================
def process_log(log_file, arg):
    f = file(log_file, "r")
    line = f.readline()
    while line:
        record = ""
        line = line.rstrip()
        if line.find('bandwidth=') == -1:
            line = f.readline()
            continue

        phrases = line.split(' ')
        time = phrases[0] # time stamp always have a fixed position
        bw = phrases[3].split('=')[1]

        # uncomment to print in std output
        #record += time + ' ' + bw
        #print record

        arg.append((time, bw));
        line = f.readline()
    f.close()


# =========================================================
# Prepare data file to feed into plotter
#
# @fname Name of the file to create and put the data inside.
# @arg An array that contains the extracted information
#      from the input log file.
# =========================================================
def populate_data(fname, arg):
    f = open(fname, "w+")
    for s in arg:
        f.write("%s %s\n" % (s[0], s[1]))
    f.close()


# =========================================================
# Plot a figure that includes either solely data1 or both
# data1 and data2.
#
# @data1 Name of the data file
# @data2 (optional) Name of the data file
# =========================================================
def plotter(data1, data2=None):
    f = open("plot.txt", "w+")
    if data2 != None:
        f.writelines(["set terminal dumb 100, 40\n",
                      "set title 'Est. Bandwidth'\n",
                      "set arrow from graph 0,first 300 to graph 1,first 300 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 600 to graph 1,first 600 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 1500 to graph 1,first 1500 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 3000 to graph 1,first 3000 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 6000 to graph 1,first 6000 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set key inside bottom right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'timestamp'\n",
                      "set ylabel 'Est. Bandwidth'\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xticlabels(1) title '",data1,"' w lines ls 5",
                      ", '",data2,"' using 2:xticlabels(1) title '",data2,"' w lines ls 9\n"])
    else:
        f.writelines(["set terminal dumb size 100, 40\n",
                      "set title 'Est. Bandwidth'\n",
                      "set arrow from graph 0,first 300 to graph 1,first 300 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 600 to graph 1,first 600 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 1500 to graph 1,first 1500 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 3000 to graph 1,first 3000 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set arrow from graph 0,first 6000 to graph 1,first 6000 nohead lw 0.5 lc rgb '#000000' front\n"
                      "set key inside bottom right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'timestamp'\n",
                      "set ylabel 'Est. Bandwidth'\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xticlabels(1) title '",data1,"' w lines ls 1"])
    f.close()

    command = "gnuplot plot.txt"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, err = process.communicate()
    print output

    # cleanup
    os.remove("plot.txt")
    os.remove(data1)
    if data2 != None:
        os.remove(data2)


# ====================
#        Run
# ====================
if ndn_log_file != "" :
    process_log(ndn_log_file, ndn_bw)
    populate_data(ndn_data, ndn_bw)
if ip_log_file != "" :
    process_log(ip_log_file, ip_bw)
    populate_data(ip_data, ip_bw)
if ndn_log_file == "":
    plotter(ip_data)
elif ip_log_file == "":
    plotter(ndn_data)
else:
    plotter(ndn_data, ip_data)

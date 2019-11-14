#!/usr/bin/python
#=============================================================
# DESCRIPTION:
# Feed this file with the a *collections* of log files collected
# by pupeteer script.
#    e.g., python startup-delay.py -n <dir>/ip-<video-name>\*.log
#    This means process all ip log files for a specific video.
#
#
# The output is a plot, showing the number of rebufferings of
# different streams of the same video.
#
# author: Chavoosh Ghasemi <chghasemi@cs.arizona.edu>
#=============================================================

import os
import sys
import glob
import getopt
import subprocess

ndn_data = "ndn-data.txt"
ip_data  = "ip-data.txt"

ndn_rebufferings = []
ip_rebufferings = []

ndn_log_files = ""
ip_log_files  = ""

def print_help():
    print "program usage:\n\tpython rebufferings-number.py\n",\
          "\t-n: ndn log files (escape the wildcard characters)\n",\
          "\t-p: ip log file (escape the wildcard characters)\n"
    sys.exit(2)

# =============
#    Input
# =============
if len(sys.argv) <= 1:
    print_help();
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:p:")
except getopt.GetoptError:
    print_help();

if len(opts) == 0:
    print_help();

for opt, arg in opts:
    if opt == '-n':
        ndn_log_files = arg
    elif opt == '-p':
        ip_log_files = arg
    else:
        print_help();


# =========================================================
# Extract the desired information from the input log file
# and put it in arg.
#
# @log_file Name of the log_file to process
# @arg The array to put the extracted information inside
# =========================================================
def process_log(logs, arg):
    filenames = sorted(glob.glob(logs))
    for f in filenames:
        for line in reversed(open(f).readlines()):
            # Startup delay is at the bottom of the file
            if (line.find("Number of bufferings:") != -1):
                line = line.strip();
                # Log file | Startup Delay (s)
                arg.append((f, line.split(': ')[1]));
                break;


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
        f.writelines(["set terminal dumb size 100, 20\n",
                      "set title 'Number of Rebufferings'\n",
                      "set key outside top right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'runs'\n",
                      "set ylabel 'Est. Bandwidth'\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xticlabels(1) title '",data1,"' w points",
                      ", '",data2,"' using 2:xticlabels(1) title '",data2,"' w points"])
    else:
        f.writelines(["set terminal dumb size 100, 20\n",
                      "set title 'Number of Rebufferings'\n",
                      "set key outside top right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'runs'\n",
                      "set ylabel 'Est. Bandwidth'\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xticlabels(1) title '",data1,"' w points"])
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
if ndn_log_files != "" :
    process_log(ndn_log_files, ndn_rebufferings)
    populate_data(ndn_data, ndn_rebufferings)
if ip_log_files != "" :
    process_log(ip_log_files, ip_rebufferings)
    populate_data(ip_data, ip_rebufferings)

if ndn_log_files == "":
    plotter(ip_data)
elif ip_log_files == "":
    plotter(ndn_data)
else:
    plotter(ndn_data, ip_data)

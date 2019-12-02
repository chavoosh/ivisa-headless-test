#!/usr/bin/python
#=============================================================
# DESCRIPTION:
# Feed this file with a *collection* of log files collected
# by pupeteer script.
#    e.g., python ttfb.py -n <dir>/ip-<video-name>\*.log
#    This means process all ip log files for a specific video.
#
#
# The output is a plot, showing Time To First Byte (TTFB) which
# shows the delay between the content server and the consumer.
# If this number is close to the RTT to GW, then we can say the
# content comes from the GW (i.e., the edge server), otherwise
# it means the edge server experienced cache miss and asked the
# content from another server.
#
# author: Chavoosh Ghasemi <chghasemi@cs.arizona.edu>
#=============================================================

import os
import sys
import glob
import argparse
import subprocess

ndn_data = "ndn-data.txt"
ip_data  = "ip-data.txt"

ndn_ttfbs = []
ip_ttfbs = []

ndn_log_files = ""
ip_log_files  = ""

# =============
#    Input
# =============
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nfiles', help='path to a collection of ndn log files', action= 'store', metavar='')
parser.add_argument('-p', '--pfiles', help='path to a collection of ip log files', action= 'store', metavar='')
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()
if (args.nfiles):
    ndn_log_files = args.nfiles
if (args.pfiles):
    ip_log_files = args.pfiles


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
            # both ndnping and ip ping have this line 
            if (line.find("Unload latency") != -1):
                line = line.strip();
                # Log file | TTFB (s)
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
                      "set title 'Time To First Byte'\n",
                      "set key outside top right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'runs'\n",
                      "set ylabel 'TTFB (s)'\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xticlabels(1) title '",data1,"' w points",
                      ", '",data2,"' using 2:xticlabels(1) title '",data2,"' w points\n"])
    else:
        f.writelines(["set terminal dumb size 100, 20\n",
                      "set title 'Minimum RTT to gateway'\n",
                      "set key outside top right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'runs'\n",
                      "set ylabel 'TTFB (s)'\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xticlabels(1) title '",data1,"' w points\n"])
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
    process_log(ndn_log_files, ndn_ttfbs)
    populate_data(ndn_data, ndn_ttfbs)
if ip_log_files != "" :
    process_log(ip_log_files, ip_ttfbs)
    populate_data(ip_data, ip_ttfbs)

if ndn_log_files == "":
    plotter(ip_data)
elif ip_log_files == "":
    plotter(ndn_data)
else:
    plotter(ndn_data, ip_data)

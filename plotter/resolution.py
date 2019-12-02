#!/usr/bin/python
#=============================================================
# DESCRIPTION:
# Feed this file with the a *collection* of log files collected
# by puppeteer script.
#
# The output is a plot, showing the distribution of of experienced
# video resolutions during each playback.
#
# author: Chavoosh Ghasemi <chghasemi@cs.arizona.edu>
#=============================================================

import os
import sys
import glob
import argparse
import subprocess

ndn_log_files = ""
ip_log_files  = ""

ndn_data = "ndn-data.txt"
ip_data  = "ip-data.txt"

ndn_res = {} 
ip_res  = {} 

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


def bandwidth_categorizer(bw, arg):
    if (bw < 600):
        arg["240p"] += 1
    elif (bw < 1500):
        arg["360p"] += 1
    elif (bw < 3000):
        arg["480p"] += 1
    elif (bw < 6000):
        arg["720p"] += 1
    else:
        arg["1080p"] += 1

# =========================================================
# Extract the desired information from the input log file
# and put it in arg.
#
# @log_file Name of the log_file to process
# @arg The array to put the extracted information inside
# =========================================================
def process_log(logs, arg):
    filenames = sorted(glob.glob(logs))
    for fname in filenames:
        f = file(fname, "r")
        line = f.readline()
        # Required BW  : Number of samples 
        resolutions = {"240p"   : 0,
                       "360p"   : 0,
                       "480p"   : 0,
                       "720p"   : 0,
                       "1080p"  : 0}
        total = 0
        while line:
            record = ""
            line = line.rstrip()
            if line.find('bandwidth=') == -1:
                line = f.readline()
                continue

            phrases = line.split(' ')
            time = phrases[0] # time stamp always have a fixed position
            bw = phrases[3].split('=')[1]
            bandwidth_categorizer(float(bw), resolutions)
            total += 1
            line = f.readline()

        for k in resolutions:
            resolutions[k] = float(resolutions[k]) / float(total)

        # save percentiles for each log file
        arg[fname] = resolutions
        f.close()

# =========================================================
# Prepare data file to feed into plotter
#
# @data Name of the file to create and put the data inside.
# @arg An array that contains the extracted information
#      from the input log file.
#      -------------------------------------------------
#      <log-file-name : resolutions
#                       <res : percentile>> 
# =========================================================
def populate_data(data, arg):
    f = open(data, "w+")
    for k in arg:
        f.write("%s %s %s %s %s %s\n" %
                (k, arg[k]["240p"], arg[k]["360p"], arg[k]["480p"], arg[k]["720p"], arg[k]["1080p"]))
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
                      "set title 'Video resolutions percentile'\n",
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
        f.writelines(["set terminal dumb size 200, 30\n",
                      "set title 'Percentile of video resolutions for each run'\n",
                      "set key outside top right\n",
                      "set ytics out\n",
                      "set xtics out\n",
                      "unset xtics\n",
                      "set xlabel 'runs'\n",
                      "set ylabel 'Video Resolution Percentile'\n",
                      "set style data histogram\n",
                      "set style histogram cluster gap 1\n",
                      "set boxwidth 0.9\n",
                      "set offset graph 0.1, graph 0.1, graph 0.1, graph 0.1\n",
                      "plot '",data1,"' using 2:xtic(1) title '",data1,"-240(*)' ls 1",
                                 ", ''  using 3         title '",data1,"-360(|)' ls -1",
                                 ", ''  using 4         title '",data1,"-480($)' ls 3",
                                 ", ''  using 5         title '",data1,"-720(@)' ls 5",
                                 ", ''  using 6         title '",data1,"-1080(=)' ls 7"])
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
    process_log(ndn_log_files, ndn_res)
    populate_data(ndn_data, ndn_res)
if ip_log_files != "" :
    process_log(ip_log_files, ip_res)
    populate_data(ip_data, ip_res)

if ndn_log_files == "":
    plotter(ip_data)
elif ip_log_files == "":
    plotter(ndn_data)
else:
    plotter(ndn_data, ip_data)

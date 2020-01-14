#!/usr/bin/python
#=============================================================
# DESCRIPTION:
# Feed this file with a *collection* of log files collected
# by pupeteer script from one of the following CDNs.
#    e.g., python rtt.py -l <dir>/ip-<video-name>\*.log
#    This means process all input log files for a specific video.
#
#
# The output is column-based data for different metrics that can
# be used to draw figures by excel or gnuplot.
#
# author: Chavoosh Ghasemi <chghasemi@cs.arizona.edu>
#=============================================================

import os
import sys
import glob
import argparse
import subprocess
data  = "data.txt";

rtts = {'ndn'     : [],
        'akamai'  : [],
        'azure'   : [],
        'fastly'  : [],
        'bitsngo' : [],
        'cdnsun'  : []};

startups = {'ndn'     : [],
            'akamai'  : [],
            'azure'   : [],
            'fastly'  : [],
            'bitsngo' : [],
            'cdnsun'  : []};

ttfbs = {'ndn'     : [],
         'akamai'  : [],
         'azure'   : [],
         'fastly'  : [],
         'bitsngo' : [],
         'cdnsun'  : []};

logs = '';
filenames = '';

# =============
#    Input
# =============
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--logfiles', help='path to a collection of log files', action= 'store', metavar='')
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args();
if (args.logfiles):
    logs = args.logfiles;
    filenames = sorted(glob.glob(logs))

# =========================================================
# Extract the desired information from the input log file
# and put it in arg.
# =========================================================
def rtt():
    print '=============';
    print 'RTT FOR EXCEL';
    print '=============';
    for f in filenames:
        valid = False;
        for line in reversed(open(f).readlines()):
            if (line.find("min/avg/max/mdev") != -1): # ndnping & ping
                line = line.strip();
                # Log file | Min RTT | Avg RTT | Max RTT (ms)
                tokens = line.split('=')[1].split('/');
                cdn = f.rpartition('/')[2].split('-')[0];
                rtts[cdn].append((tokens[0].split(' ')[1], tokens[1], tokens[2]));
                valid = True;
                break;
            elif (line.find("Max rtt:") != -1): # Nping
                line = line.strip();
                # Log file | Min RTT | Avg RTT | Max RTT (ms)
                tokens = line.split(' ');
                cdn = f.rpartition('/')[2].split('-')[0];
                rtts[cdn].append((tokens[6].split('m')[0], tokens[10].split('m')[0], tokens[2].split('m')[0]));
                valid = True;
                break;
        if valid == False:
            print 'file ' + f + ' is not a valid log file...'

    # print
    walker = 0;
    print 'index ndn-min ndn-avg ndn-max '    +\
          'akamai-min akamai-avg akamai-max ' +\
          'azure-min azure-avg azure-max '    +\
          'fastly-min fastly-avg fastly-max ' +\
          'cdnsun-min cdnsun-avg cdnsun-max ' +\
          'bitsngo-min bitsngo-avg bitsngo-max';
    while 1==1:
        line = '[' + str(walker) + '] ';
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(rtts[c]) > walker:
                line += rtts[c][walker][0] + ',' + rtts[c][walker][1] + ',' + rtts[c][walker][2] + ' ';
            else:
                line += 'NULL NULL NULL '
        if line.find('NULL') != -1:
            print '------------\nLast line:\n' + line + '\n------------';
            break;
        print line;
        walker += 1;


def startup_delay():
    print '=======================';
    print 'STARTUP DELAY FOR EXCEL';
    print '=======================';
    for f in filenames:
        valid = False;
        for line in reversed(open(f).readlines()):
            if (line.find("Load latency: ") != -1):
                line = line.strip();
                cdn = f.rpartition('/')[2].split('-')[0];
                # Log file | Startup Delay (s)
                startups[cdn].append(line.split(': ')[1]);
                valid = True;
                break;
        if valid == False:
            print 'file ' + f + ' is not a valid log file...'

    # print
    walker = 0;
    print 'index ndn akamai azure fastly cdnsun bitsngo';
    while 1==1:
        line = '[' + str(walker) + '] ';
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(startups[c]) > walker:
                line += startups[c][walker] + ' ';
            else:
                line += 'NULL '
        if line.find('NULL') != -1:
            print '------------\nLast line:\n' + line + '\n------------';
            break;
        print line;
        walker += 1;

def ttfb():
    print '=======================';
    print 'TTFB FOR EXCEL';
    print '=======================';
    for f in filenames:
        valid = False;
        for line in reversed(open(f).readlines()):
            if (line.find("TTFB") != -1):
                line = line.strip();
                cdn = f.rpartition('/')[2].split('-')[0];
                # Log file | TTFB (ms)
                ttfbs[cdn].append(line.split(': ')[1]);
                valid = True;
                break;
        if valid == False:
            print 'file ' + f + ' is not a valid log file...'

    # print
    walker = 0;
    print 'index ndn akamai azure fastly cdnsun bitsngo';
    while 1==1:
        line = '[' + str(walker) + '] ';
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(ttfbs[c]) > walker:
                line += ttfbs[c][walker] + ' ';
            else:
                line += 'NULL ';
        if line.find('NULL') != -1:
            print '------------\nLast line:\n' + line + '\n------------';
            break;
        print line;
        walker += 1;


# ====================
#        Run
# ====================
rtt()
startup_delay()
ttfb()

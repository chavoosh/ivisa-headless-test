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
import copy
import argparse
import subprocess
data  = "data.txt";

rtts = {'ndn'     : [],
        'akamai'  : [],
        'azure'   : [],
        'fastly'  : [],
        'bitsngo' : [],
        'cdnsun'  : []};

startups = copy.deepcopy(rtts);
ttfbs = copy.deepcopy(rtts);
resolutions = copy.deepcopy(rtts);
rebufferings = copy.deepcopy(rtts);

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

def bandwidth_categorizer(bw, arg):
    if (bw < 600):
        arg['240p'] += 1
    elif (bw < 1500):
        arg['360p'] += 1
    elif (bw < 3000):
        arg['480p'] += 1
    elif (bw < 6000):
        arg['720p'] += 1
    else:
        arg['1080p'] += 1

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
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(rtts[c]) > walker:
                valid = True;
                line += rtts[c][walker][0] + ',' + rtts[c][walker][1] + ',' + rtts[c][walker][2] + ' ';
            else:
                line += 'NULL,NULL,NULL '
        if valid == False:
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
        valid = False;
        line = '[' + str(walker) + '] ';
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(startups[c]) > walker:
                valid = True;
                line += str(startups[c][walker]) + ' ';
            else:
                line += 'NULL '
        if valid == False:
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
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(ttfbs[c]) > walker:
                valid = True;
                line += str(ttfbs[c][walker]) + ' ';
            else:
                line += 'NULL ';
        if valid == False:
            break;
        print line;
        walker += 1;

def number_of_rebufferings():
    print '=======================';
    print 'REBUFFERINGS FOR EXCEL';
    print '=======================';
    for f in filenames:
        valid = False;
        for line in reversed(open(f).readlines()):
            # Startup delay is at the bottom of the file
            if (line.find("Number of bufferings:") != -1):
                line = line.strip();
                cdn = f.rpartition('/')[2].split('-')[0];
                # Log file | Startup Delay (s)
                rebufferings[cdn].append(line.split(': ')[1]);
                valid = True;
                break;
        if valid == False:
            print 'file ' + f + ' is not a valid log file...'
    # print
    walker = 0;
    print 'index ndn akamai azure fastly cdnsun bitsngo';
    while 1==1:
        line = '[' + str(walker) + '] ';
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(rebufferings[c]) > walker:
                valid = True;
                line += str(rebufferings[c][walker]) + ' ';
            else:
                line += 'NULL ';
        if valid == False:
            break;
        print line;
        walker += 1;

def map_resolutions():
    print '============================';
    print 'NUM OF RESOLUTIONS FOR EXCEL';
    print '============================';
    # Required BW  : Number of samples
    for f in filenames:
        valid = False;
        # Required BW  : Number of samples
        resMap = {'240p'   : 0,
                  '360p'   : 0,
                  '480p'   : 0,
                  '720p'   : 0,
                  '1080p'  : 0}
        total = 0
        for line in reversed(open(f).readlines()):
            if line.find('bandwidth=') != -1:
                valid = True;
                line = line.strip();
                phrases = line.split(' ')
                time = phrases[0] # time stamp always have a fixed position
                bw = phrases[3].split('=')[1]
                bandwidth_categorizer(float(bw), resMap)
                total += 1

        if valid == False:
            print 'file ' + f + ' is not a valid log file...'
            continue;
        for k in resMap:
            resMap[k] = float(resMap[k]) / float(total)
        # save percentages for each log file
        cdn = f.rpartition('/')[2].split('-')[0];
        resolutions[cdn].append(resMap);

    # print
    walker = 0;
    print 'index ' +\
          'ndn-240p ndn-360p ndn-480p ndn-720p ndn-1080p ' +\
          'akamai-240p akamai-360p akamai-480p akamai-720p akamai-1080p ' +\
          'azure-240p azure-360p azure-480p azure-720p azure-1080p '    +\
          'fastly-240p fastly-360p fastly-480p fastly-720p fastly-1080p ' +\
          'cdnsun-240p cdnsun-360p cdnsun-480p cdnsun-720p cdnsun-1080p ' +\
          'bitsngo-240p bitsngo-360p bitsngo-480p bitsngo-720p bitsngo-1080p';
    while 1==1:
        line = '[' + str(walker) + '] ';
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if len(resolutions[c]) > walker:
                valid = True;
                line += str(resolutions[c][walker]['240p']) + ',' +\
                        str(resolutions[c][walker]['360p']) + ',' +\
                        str(resolutions[c][walker]['480p']) + ',' +\
                        str(resolutions[c][walker]['720p']) + ',' +\
                        str(resolutions[c][walker]['1080p']) + ' ';
            else:
                line += 'NULL,NULL,NULL,NULL,NULL ';
        if valid == False:
            break;
        print line;
        walker += 1;

# ====================
#        Run
# ====================
rtt()
startup_delay()
ttfb()
number_of_rebufferings()
map_resolutions()

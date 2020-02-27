#!/usr/bin/python
#=============================================================
# DESCRIPTION:
# Feed this file with a *collection* of log files collected
# by pupeteer script from one of the following CDNs.
#    e.g., python excel.py -l <dir>/ip-<video-name>\*.log
#    This means process all input log files for a specific video.
#
# The output is column-based data for different metrics that can
# be used to draw figures by excel or gnuplot.
#
# author: Chavoosh Ghasemi <chghasemi@cs.arizona.edu>
#=============================================================

import os
import re
import sys
import copy
import glob
import json
import socke
import argparse
import subprocess

from urllib2 import urlopen

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKCYNE = '\033[96m'
    OKPINK = '\033[95m'
    OKORANGE = '\033[33m'
    OKGRAY = '\033[37m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


data  = "data.txt";

# indicate whether a given CDN is present in log files
exist = {'ndn'     : False,
         'akamai'  : False,
         'azure'   : False,
         'fastly'  : False,
         'bitsngo' : False,
         'cdnsun'  : False};

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
locations = copy.deepcopy(rtts);

_decorated = False;
logs = '';
filenames = '';

# =============
#    Inpu
# =============
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--logfiles', help='path to a collection of log files', action= 'store', metavar='')
parser.add_argument('-d', '--decorated', help='just print the decorated output', action= 'store_true')
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args();
if (args.logfiles):
    logs = args.logfiles;
    filenames = sorted(glob.glob(logs))
if (args.decorated):
    _decorated = True;

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
    for f in filenames:
        valid = False;
        for line in reversed(open(f).readlines()):
            if (line.find("min/avg/max/mdev") != -1): # ndnping & ping
                line = line.strip();
                # Log file | Min RTT | Avg RTT | Max RTT (ms)
                tokens = line.split('=')[1].split('/');
                cdn = f.rpartition('/')[2].split('-')[0];
                exist[cdn] = True;
                rtts[cdn].append((tokens[0].split(' ')[1], tokens[1], tokens[2]));
                valid = True;
                break;
            elif (line.find("Max rtt:") != -1): # Nping
                line = line.strip();
                # Log file | Min RTT | Avg RTT | Max RTT (ms)
                tokens = line.split(' ');
                cdn = f.rpartition('/')[2].split('-')[0];
                exist[cdn] = True;
                rtts[cdn].append((tokens[6].split('m')[0], tokens[10].split('m')[0], tokens[2].split('m')[0]));
                valid = True;
                break;
        if valid == False:
            print 'file ' + f + ' is not a valid log file...'

    # prin
    if _decorated == True:
        return;
    print '=============';
    print 'RTT FOR EXCEL';
    print '=============';
    walker = 0;
    header = 'index';
    for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
        if exist[c] == True:
            header = header + ' ' + c + '-min ' + c + '-avg ' + c + '-max';
    print header;
    while 1==1:
        line = '[' + str(walker) + '] ';
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if exist[c] == False:
                continue;
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

    # prin
    if _decorated == True:
        return;
    print '=======================';
    print 'STARTUP DELAY FOR EXCEL';
    print '=======================';
    walker = 0;
    header = 'index';
    for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
        if exist[c] == True:
            header = header + ' ' + c;
    print header;
    while 1==1:
        valid = False;
        line = '[' + str(walker) + '] ';
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if exist[c] == False:
                continue;
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
    # prin
    if _decorated == True:
        return;
    print '=======================';
    print 'TTFB FOR EXCEL';
    print '=======================';
    walker = 0;
    header = 'index';
    for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
        if exist[c] == True:
            header = header + ' ' + c;
    print header;
    while 1==1:
        line = '[' + str(walker) + '] ';
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if exist[c] == False:
                continue;
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
    # prin
    if _decorated == True:
        return;
    print '=======================';
    print 'REBUFFERINGS FOR EXCEL';
    print '=======================';
    walker = 0;
    header = 'index';
    for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
        if exist[c] == True:
            header = header + ' ' + c;
    print header;
    while 1==1:
        line = '[' + str(walker) + '] ';
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if exist[c] == False:
                continue;
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
        for line in open(f).readlines():
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

    # prin
    if _decorated == True:
        return;
    print '============================';
    print 'NUM OF RESOLUTIONS FOR EXCEL';
    print '============================';
    walker = 0;
    header = 'index';
    for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
        if exist[c] == True:
            header = header + ' ' + c + '-240p ' + c + '-360p ' + c + '-480p ' +
                     c + '-720p ' + c + '-1080p';
    print header;
    while 1==1:
        line = '[' + str(walker) + '] ';
        valid = False;
        for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
            if exist[c] == False:
                continue;
            if len(resolutions[c]) > walker:
                valid = True;
                line += str(resolutions[c][walker]['240p']) + ',' +
                        str(resolutions[c][walker]['360p']) + ',' +
                        str(resolutions[c][walker]['480p']) + ',' +
                        str(resolutions[c][walker]['720p']) + ',' +
                        str(resolutions[c][walker]['1080p']) + ' ';
            else:
                line += 'NULL,NULL,NULL,NULL,NULL ';
        if valid == False:
            break;
        print line;
        walker += 1;

def location():
    for f in filenames:
        valid = False;
        gw_ip = 'NULL';
        pub_ip = 'NULL';
        pub_location = 'NO_LOCATION';
        gw_location = 'NO_LOCATION';
        for line in open(f).readlines():
            line = line.strip();
            cdn = f.rpartition('/')[2].split('-')[0];
            if line.find("PUBLIC_IP") != -1: # in some files it might not exis
                pub_ip = line.split(': ')[1];
                url = "http://ipinfo.io/" + pub_ip + "/json"
                response = urlopen(url)
                data = json.load(response)
                pub_location = (data['country']).encode('utf-8') + '|' + (data['city']).encode('utf-8');
                if 'hostname' in  data:
                    pub_location += '|' + (data['hostname']).encode('utf-8');
                pub_location = pub_location.replace(' ', '_');
            if line.find("SENT") != -1:
                valid = True;
                gw_ip = re.split(':|\(', line)[3]; # ip address of the gw
                url = "http://ipinfo.io/" + gw_ip + "/json"
                response = urlopen(url)
                data = json.load(response)
                gw_location = (data['country']).encode('utf-8') + '|' + (data['city']).encode('utf-8');
                if 'hostname' in  data:
                    gw_location += '|' + (data['hostname']).encode('utf-8');
                gw_location = gw_location.replace(' ', '_');
                break; # do not process the file after this line
        if valid == False:
            print 'No IP found. File ' + f + ' is not a valid log file...'
        else:
            locations[cdn].append((pub_ip, pub_location, gw_ip, gw_location)); # ip address of the gw


def decorate():
    print '\n\n=======================\nDECORATED SECTION\n=======================';
    for c in ['ndn', 'akamai', 'azure', 'fastly', 'cdnsun', 'bitsngo']:
        if exist[c] == False:
            continue;
        header = '********\n' + bcolors.WARNING + bcolors.BOLD + c + bcolors.ENDC + '\n********\nindex';
        header += bcolors.OKGREEN + ' rtt-min rtt-avg rtt-max';
        header += bcolors.OKBLUE + ' startup(s)' +
                  bcolors.FAIL + ' TTFB(ms)' +
                  bcolors.OKCYNE + ' rebuffering';
        header += bcolors.OKPINK + ' 240p 360p 480p 720p 1080p';
        header += bcolors.OKORANGE + ' gw_ip gw_location consumer_ip' +
                  bcolors.OKGRAY + ' consumer_location' + bcolors.ENDC;
        print header
        walker = 0;
        valid = False;
        upper_bound = max(len(rtts[c]), len(startups[c]), len(ttfbs[c]), len(rebufferings[c]));
        while walker <  upper_bound:
            line = '[' + str(walker) + '] ';
            if len(rtts[c]) > walker:
                valid = True;
                line += bcolors.OKGREEN + rtts[c][walker][0] + ' ' + rtts[c][walker][1] + ' ' + rtts[c][walker][2] + ' ' + bcolors.ENDC;
            else:
                line += bcolors.OKGREEN + 'NULL NULL NULL ' + bcolors.ENDC
            if len(startups[c]) > walker:
                valid = True;
                line += bcolors.OKBLUE + str(startups[c][walker]) + ' ' + bcolors.ENDC;
            else:
                line += bcolors.OKBLUE + 'NULL ';
            if len(ttfbs[c]) > walker:
                valid = True;
                line += bcolors.FAIL + str(ttfbs[c][walker]) + ' ' + bcolors.ENDC;
            else:
                line += bcolors.FAIL + 'NULL ' + bcolors.ENDC;
            if len(rebufferings[c]) > walker:
                valid = True;
                line += bcolors.OKCYNE + str(rebufferings[c][walker]) + ' ' + bcolors.ENDC;
            else:
                line += bcolors.OKCYNE + 'NULL ' + bcolors.ENDC;
            if len(resolutions[c]) > walker:
                valid = True;
                line += bcolors.OKPINK +
                        str(resolutions[c][walker]['240p']) + ' ' +
                        str(resolutions[c][walker]['360p']) + ' ' +
                        str(resolutions[c][walker]['480p']) + ' ' +
                        str(resolutions[c][walker]['720p']) + ' ' +
                        str(resolutions[c][walker]['1080p']) + ' ' + bcolors.ENDC;
            else:
                line += bcolors.OKPINK + 'NULL,NULL,NULL,NULL,NULL ' + bcolors.ENDC;
            if len(locations[c]) > walker:
                line += bcolors.OKORANGE +
                        str(locations[c][walker][2]) + ' ' + str(locations[c][walker][3]) + ' ' +
                        bcolors.OKGRAY +
                        str(locations[c][walker][0]) + ' ' + str(locations[c][walker][1]) +
                        bcolors.ENDC;
            else:
                line += bcolors.OKRANGE + 'NULL NO_LOCATION' + bcolors.OKGRAY + ' NULL NO_LOCATION' + bcolors.ENDC;
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
location()
# group each cdn's data
decorate()

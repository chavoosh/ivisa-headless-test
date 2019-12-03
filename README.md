# Headless tests for NDN video streaming service

This repository includes a test that watches a video in headless mode using IP and NDN technology and
a number of scripts to parse the collected results and draw some figures.


## Install
- Install `ndnping` from [ndn-tools](https://github.com/named-data/ndn-tools)
- Run `$ bash install.sh`

## Run
- Switch to the repo root directory and run the following command:
    
      $ nodejs headless-video-player.js https://ivisa.named-data.net/html/ndn_vs_ip.html

## Schedule the runs
Add the following line to crontab task manager to watch a video over IP and NDN every 30 minutes
(run `$ cront -e`):
  
    */30 *  *   *   *     /bin/bash /home/<USER_NAME>/ivisa-headless-test/run.sh

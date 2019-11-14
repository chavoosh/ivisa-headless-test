# Headless tests for NDN video streaming service

This repository includes a test that watches a video in headless mode using IP and NDN technology and
a number of scripts to parse the collected results and draw some figures.


## Install
- Install [nodejs](https://nodejs.org/en/)
- Install [Puppeteer-Core](https://www.npmjs.com/package/puppeteer#puppeteer-core)
- Install [Google Chrome Browser](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=en)
- Install python 2.7.x

      $ sudo apt-get install python2.7

## Run
- Use the following command to run a test:
    
      $ nodejs headless-video-player.js https://ivisa.named-data.net/html/ndn_vs_ip.html

## Schedule the runs
Add the following lines to crontab task manager to watch a video over IP and NDN every 30 minutes
(run `$ cront -e`):

    */30 *  *   *   *     /usr/bin/node /home/chavoosh/icdn/scripts/headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ndn-research-questions.html
    */30 *  *   *   *     /usr/bin/node /home/chavoosh/icdn/scripts/headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ip-research-questions.html



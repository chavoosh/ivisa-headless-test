#!/bin/bash

(cd ~ && wget -N https://raw.githubusercontent.com/chavoosh/ivisa-headless-test/master/headless-video-player.js)

(cd ~ && nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ndn-ndn_vs_ip.html)
sleep 5
(cd ~ && nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ip-ndn_vs_ip.html)
sleep 5
(cd ~ && rm headless-video-player.js)

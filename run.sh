#!/bin/bash

(cd ~ && wget -N https://raw.githubusercontent.com/chavoosh/ivisa-headless-test/master/headless-video-player.js)

(cd ~ && nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ndn-research-questions.html &)
(cd ~ && nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ip-research-questions.html)
(cd ~ && rm headless-video-player.js)

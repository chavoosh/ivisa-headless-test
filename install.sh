#!/bin/bash

# Install nodejs and npm
sudo apt-get update && wait
sudo apt-get install nodejs && wait
sudo apt-get install npm && wait

# Install packages
npm i puppeteer-core && wait

# Install Python
sudo apt-get install python2.7

# Install Google Chrome
sudo bash -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
wget https://dl.google.com/linux/linux_signing_key.pub && wait
sudo apt-key add linux_signing_key.pub && wait
rm linux_signing_key.pub && wait
sudo apt-get update && wait
sudo apt-get --fix-broken install && wait
sudo apt-get install google-chrome-stable && wait

# Clone the repository in home directory and run a quick test
sudo apt-get install git && wait
(cd ~ && git clone https://github.com/chavoosh/ivisa-headless-test && wait)
(cd ~/ivisa-headless-test && nodejs headless-video-player.js https://ivisa.named-data.net/html/ndn_vs_ip.html && wait)

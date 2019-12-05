#!/bin/bash

# Install nodejs and npm
sudo apt-get update
sudo apt-get install nodejs
sudo apt-get install npm

# Install packages
npm i puppeteer-core

# Install Python
sudo apt-get install python2.7

# Install Google Chrome
sudo bash -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
wget https://dl.google.com/linux/linux_signing_key.pub
sudo apt-key add linux_signing_key.pub
rm linux_signing_key.pub
sudo apt-get update
sudo apt-get --fix-broken install
sudo apt-get install google-chrome-stable

# Check ndnping
if hash ndnping 2>/dev/null; then
  echo "ndnping exist!"
else
  echo -e "\n\tERROR: ndnping does not exist... Please install it from here https://github.com/named-data/ndn-tools"
  exit 1
fi

# Run a quick test
nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ip-research-questions.html

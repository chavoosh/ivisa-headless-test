#!/bin/bash

# Install nodejs and npm
sudo apt-get update -y
sudo apt-get install nodejs -y
sudo apt-get install npm -y
sudo apt-get install nmap -y
sudo apt-get install gnuplot -y

# Install packages
npm i puppeteer-core

# Install Python
sudo apt-get install python2.7 -y

# Install Google Chrome
sudo bash -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
wget https://dl.google.com/linux/linux_signing_key.pub
sudo apt-key add linux_signing_key.pub
rm linux_signing_key.pub
sudo apt-get update
sudo apt-get --fix-broken install -y
sudo apt-get install google-chrome-stable -y

# Check ndnping
if hash nfdc 2>/dev/null; then
  echo "NFDC exist!"
else
  echo -e "\n\tERROR: NFDC does not exist... Please install NFD from here https://github.com/named-data/NFD"
  exit 1
fi

if hash ndnping 2>/dev/null; then
  echo "ndnping exist!"
else
  echo -e "\n\tERROR: ndnping does not exist... Please install it from here https://github.com/named-data/ndn-tools"
  exit 1
fi


# Run a quick test
nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/ip-ndn_vs_ip.html

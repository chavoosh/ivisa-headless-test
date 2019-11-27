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

# Install ndnping and library
if hash ndnping 2>/dev/null; then
  echo "ndnping already exist!"
else
  sudo cp ndnping /usr/bin/
fi

# Clone the repository in home directory
if [ ! -d "~/ivisa-headless-test" ]
then
  sudo apt-get install git && wait
  (cd ~ && git clone https://github.com/chavoosh/ivisa-headless-test && wait)
fi

# Install ndnping and library
if hash ndnping 2>/dev/null; then
  echo "ndnping already exist!"
else
  (cd ~/ivisa-headless-test && sudo cp ./ndnping /usr/bin/ && wait)
fi

if [ ! -f "/usr/local/lib/libndn-cxx.so.0.6.6" ]
then
  (cd ~/ivisa-headless-test && sudo cp ./libndn-cxx.so.0.6.6 /usr/loacl/lib/ && wait)
fi

# Run a quick test
(cd ~/ivisa-headless-test && nodejs headless-video-player.js https://ivisa.named-data.net/html/ndn_vs_ip.html && wait)

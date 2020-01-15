#!/bin/bash

(cd ~ && wget -N https://raw.githubusercontent.com/chavoosh/ivisa-headless-test/master/headless-video-player.js)


# In each loop we watch the same video but with different name which seems a different video for IP CDNs.
for i in {1..10}
do
  # Akamai
  (cd ~ && timeout 180 nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/akamai-ip-ndn_vs_ip.html)
  sleep 5
  # Fastly
  (cd ~ && timeout 180 nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net.global.prod.fastly.net/html/fastly-ip-ndn_vs_ip.html)
  sleep 5
  # CDNSun
  (cd ~ && timeout 180 nodejs headless-video-player.js http://cdnsun.ivisa-icdn-1.dynu.net/html/cdnsun-ip-ndn_vs_ip.html)
  sleep 5
  #BitsNgo
  (cd ~ && timeout 180 nodejs headless-video-player.js http://bitsngo.ivisa-icdn-1.dynu.net/html/bitsngo-ip-ndn_vs_ip.html)
  sleep 5
  # Azure
  (cd ~ && timeout 180 nodejs headless-video-player.js http://ivisa-icdn-1.azureedge.net/html/azure-ip-ndn_vs_ip.html)
  sleep 5

<<COMMENT1
  # Akamai
  (cd ~ && timeout 180 nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net/html/akamai-ip-ndn_vs_ip_$i.html)
  sleep 5
  # Fastly
  (cd ~ && timeout 180 nodejs headless-video-player.js http://ivisa-icdn-1.dynu.net.global.prod.fastly.net/html/fastly-ip-ndn_vs_ip_$i.html)
  sleep 5
  curl -XPOST -H "Fastly-Key:YnJ5hqEjpbq6ltYttduq4pGjUFXfzmBm" https://api.fastly.com/service/0HYprY29yAXbwObrbKDVQ6/purge_all
  # CDNSun
  (cd ~ && timeout 180 nodejs headless-video-player.js http://cdnsun.ivisa-icdn-1.dynu.net/html/cdnsun-ip-ndn_vs_ip_$i.html)
  sleep 5
  #BitsNgo
  (cd ~ && timeout 180 nodejs headless-video-player.js http://bitsngo.ivisa-icdn-1.dynu.net/html/bitsngo-ip-ndn_vs_ip_$i.html)
  sleep 5
  # Azure
  (cd ~ && timeout 180 nodejs headless-video-player.js http://ivisa-icdn-1.azureedge.net/html/azure-ip-ndn_vs_ip_$i.html)
  sleep 5
COMMENT1

  # NDN
  (cd ~ && timeout 180 nodejs headless-video-player.js http://150.135.68.166/html/ndn-ndn_vs_ip.html)
  sleep 5
done
(cd ~ && rm headless-video-player.js)

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const util = require('util');
const exec = util.promisify(require('child_process').exec);

// ==========================
//         utility
// ==========================
function sectionize(content) {
  var line = '\n===================================\n';
  line += content;
  line += '===================================';
  return line;
}

// ==========================
// Resolve RTT to the server
// ==========================
async function resolveRtt(host) {
  if (host.search('ndn@') > -1) { // NDN
    host = host.split('@')[1];
    try {
      // Make a UDP tunnel to the chosen hub to run ndnping
      var { stdout, stderr } = await exec('curl -s http://ndndemo.arl.wustl.edu/testbed-nodes.json | grep -i ' + host + ' -C 2 | grep "prefix" | awk -F\'"\' \'{print $4}\'');
      var prefixname = stdout.split(':')[1];
      var { stdout, stderr } = await exec('/usr/local/bin/nfdc face create udp://' + host + ' && sleep 3 && /usr/local/bin/nfdc route add / udp://' + host + ' && sleep 1');
      var line = sectionize(stdout + '\n' + stderr);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', line + '\n', (err) => { if (err) throw err; });
      console.log(line);

      // Run ndnping
      var { stdout, stderr } = await exec('/usr/local/bin/ndnping -c 10 ' + prefixname);
      line = sectionize(stdout);
      console.log(line);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', line + '\n', (err) => { if (err) throw err; });
    } catch (err) {
      console.log(err);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', err + '\n', (err) => { if (err) throw err; });
    }
    // Destroy the created face in NFD
    var { stdout, stderr } = await exec('/usr/local/bin/nfdc face destroy udp://' + host);
    var line = sectionize(stdout + '\n' + stderr);
    console.log(line);
  }
  else if (host.search('ip@') > -1) { // IP
    host = host.split('@')[1];
    try {
      var { stdout, stderr } = await exec('nping -c 10 ' + host);
      var line = sectionize(stdout);
      console.log(line);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', line + '\n', (err) => { if (err) throw err; });
    } catch (err) {
      console.log(err);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', err + '\n', (err) => { if (err) throw err; });
    }
    try {
      var { stdout, stderr } = await exec('traceroute ' + host);
      var line = sectionize(stdout);
      console.log(line);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', line + '\n', (err) => { if (err) throw err; });
    } catch (err) {
      console.log(err);
      fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', err + '\n', (err) => { if (err) throw err; });
    }
  }
};

// =============================
//  Check the results directory
// =============================
RESULT_DIR = process.env['HOME'] + '/.ivisa-tests/';
if (!fs.existsSync(RESULT_DIR)){
  fs.mkdirSync(RESULT_DIR);
}


// ============
//  Indicators
// ============
var START = false;   // whether the video is started
var CONS_OUT = true; // print the log to std output
if (process.argv[3] == 0) CONS_OUT = false;
var EXEC = '/etc/alternatives/google-chrome';


// =================
//  Parse video url
// =================
var URL = process.argv[2];
var TODAY = new Date();
var VIDEO_DATE_TIME = URL.slice(URL.lastIndexOf('/') + 1, URL.lastIndexOf('.')) + '_' +
                      TODAY.getMonth()    + '-' +
                      TODAY.getDate()      + '-' +
                      TODAY.getFullYear() + '_' +
                      TODAY.getHours()    + ':' +
                      TODAY.getMinutes()  + ':' +
                      TODAY.getSeconds();

// ========================
//  Header of the log file
// ========================
var DELIMITER = '=';
for (var i = 0; i < URL.length + 8; ++i) DELIMITER += '=';
var HEADER =  DELIMITER + '\n' +
             'DATE  : ' + Date() + '\n' +
             'VLINK : ' + URL + '\n' +
             DELIMITER + '\n';
fs.writeFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', HEADER, (err) => { if (err) throw err; });



// =================
//  Run the program
// =================
(async () => {
  const browser = await puppeteer.launch({executablePath: EXEC, args: ['--disable-web-security'], headless: true});
  const page = await browser.newPage();
  page.on('console', msg => {
    line = new Date().getHours() + ':' +
           new Date().getMinutes() + ':' +
           new Date().getSeconds() + '.' +
           new Date().getMilliseconds() + ' ' +
           msg.text();

    if (msg.text().search('onChooseStreams') > -1)
      START = true;

    if (CONS_OUT)  console.log(line);
    fs.appendFile(RESULT_DIR + VIDEO_DATE_TIME + '.log', line + '\n', (err) => { if (err) throw err; });

    if (msg.text().search('CONNECTING TO') > -1) {
      var host = msg.text().split('>')[1].split(':')[0];
      resolveRtt(host);
    }

    if (msg.text().search('buffered to end of presentation') > -1) {
      browser.close();
    }
  });

  await page.goto(URL, {waitUntil: 'load', timeout: 5000});
  await page.waitFor(1000);

  if (await page.$('video') !== null)  {
    const video = await page.$('video');
    video.click();
  }

  // check whether the video has been started after 8s
  await page.waitFor(8000);
  if (START === false)
    await browser.close();

  // take a screenshot after a cumulative 10s
  await page.waitFor(2000);
  await page.screenshot({ path: RESULT_DIR + VIDEO_DATE_TIME + '.png' });
})();



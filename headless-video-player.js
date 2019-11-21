const puppeteer = require('puppeteer-core');
const fs = require('fs');


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

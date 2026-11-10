const puppeteer = require('puppeteer-core');
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function verifyLive() {
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.toString()));

  const url = 'https://3-erode-h-ackathon.vercel.app';
  console.log(`Navigating to live production: ${url}...`);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 25000 });

  // 1. Switch through all tabs
  console.log('Testing navigation tabs...');
  const tabs = ['home', 'chat', 'vision', 'optimizer', 'market', 'marketplace'];
  for (const t of tabs) {
    await page.evaluate(k => window.selectTab(k), t);
    await new Promise(r => setTimeout(r, 200));
  }

  // 2. Test chat
  console.log('Testing Agri Chat on production...');
  await page.evaluate(() => window.selectTab('chat'));
  await page.type('#chatInput', 'How to prevent rhizome rot in Turmeric?');
  await page.evaluate(() => window.sendUserMessage());
  await new Promise(r => setTimeout(r, 3000));

  // 3. Test vision
  console.log('Testing Crop Vision on production...');
  await page.evaluate(() => window.selectTab('vision'));
  await page.evaluate(() => window.pickLeafPreset(null, 'rice'));
  await new Promise(r => setTimeout(r, 1500));

  // 4. Test optimizer
  console.log('Testing Crop Optimizer on production...');
  await page.evaluate(() => window.selectTab('optimizer'));
  await page.evaluate(() => window.handleDistrictChange('Thanjavur'));
  await new Promise(r => setTimeout(r, 1000));

  // 5. Test offer modal in marketplace
  console.log('Testing Marketplace & Offer Modal on production...');
  await page.evaluate(() => window.selectTab('marketplace'));
  await page.evaluate(() => window.openOfferModal('Erode Turmeric', 'Murugan K.', 145, '919876543210'));
  await new Promise(r => setTimeout(r, 400));
  await page.evaluate(() => window.closeOfferModal());

  await page.screenshot({ path: 'screenshot_production_verified.png', fullPage: true });
  console.log('Screenshot saved: screenshot_production_verified.png');
  console.log(`Live Verification Complete. Total Console/Page Errors: ${errors.length}`);

  await browser.close();
  if (errors.length > 0) {
    console.error('Errors found:', errors);
    process.exit(1);
  }
}

verifyLive().catch(err => {
  console.error('Live test failed:', err);
  process.exit(1);
});

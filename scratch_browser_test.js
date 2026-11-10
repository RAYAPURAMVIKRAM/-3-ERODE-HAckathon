const puppeteer = require('puppeteer-core');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function testUrl(url) {
  console.log(`\n========================================`);
  console.log(`TESTING URL: ${url}`);
  console.log(`========================================`);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const page = await browser.newPage();

  const consoleLogs = [];
  const pageErrors = [];

  page.on('console', msg => {
    const text = `[CONSOLE ${msg.type().toUpperCase()}] ${msg.text()}`;
    consoleLogs.push(text);
    console.log(text);
  });

  page.on('pageerror', err => {
    const text = `[PAGE ERROR] ${err.toString()}`;
    pageErrors.push(text);
    console.error(text);
  });

  try {
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    console.log(`Loaded ${url}`);

    if (url.includes('vercel.app') || url.includes('index.html')) {
      // Test tab switching
      const tabIds = ['tab-home', 'tab-chat', 'tab-vision', 'tab-optimizer', 'tab-market', 'tab-marketplace'];
      
      const getStyles = async () => {
        return await page.evaluate((ids) => {
          const res = {};
          for (const id of ids) {
            const el = document.getElementById(id);
            res[id] = el ? window.getComputedStyle(el).display : 'NOT_FOUND';
          }
          return res;
        }, tabIds);
      };

      console.log('\n--- Initial Tab Displays ---');
      console.log(await getStyles());

      // Click each tab button
      const tabButtons = await page.$$('.tab-btn');
      console.log(`Found ${tabButtons.length} tab buttons`);

      for (let i = 0; i < tabButtons.length; i++) {
        const btnText = await page.evaluate(el => el.innerText.trim(), tabButtons[i]);
        const dataTab = await page.evaluate(el => el.getAttribute('data-tab'), tabButtons[i]);
        console.log(`\nClicking Tab Button [${i}]: "${btnText}" (data-tab: ${dataTab})`);
        
        await tabButtons[i].click();
        await new Promise(r => setTimeout(r, 500));
        
        const styles = await getStyles();
        console.log(`Displays after clicking tab "${dataTab}":`, styles);
      }

      // Click home module cards
      console.log('\n--- Clicking Home Module Cards ---');
      // First go back to home
      await page.evaluate(() => window.selectTab && window.selectTab('home'));
      await new Promise(r => setTimeout(r, 500));

      const cards = await page.$$('.home-module-card');
      console.log(`Found ${cards.length} home module cards`);
      for (let i = 0; i < cards.length; i++) {
        const cardTitle = await page.evaluate(el => {
          const t = el.querySelector('.home-module-title');
          return t ? t.innerText.trim() : 'card';
        }, cards[i]);
        console.log(`\nClicking Home Module Card [${i}]: "${cardTitle}"`);
        await cards[i].click();
        await new Promise(r => setTimeout(r, 500));
        console.log(`Displays after clicking "${cardTitle}":`, await getStyles());

        // Return to home for next card test
        await page.evaluate(() => window.selectTab && window.selectTab('home'));
        await new Promise(r => setTimeout(r, 300));
      }
    } else {
      // Streamlit test
      console.log('\n--- Streamlit Page Test ---');
      const title = await page.title();
      console.log('Streamlit Page Title:', title);

      // Find all buttons in Streamlit
      const buttons = await page.$$('button');
      console.log(`Found ${buttons.length} buttons on Streamlit page`);
      let chatBtn = null;
      for (let i = 0; i < buttons.length; i++) {
        const btnText = await page.evaluate(el => el.innerText.trim(), buttons[i]);
        if (btnText.includes('Agri Chat')) {
          console.log(`Found Agri Chat button at index [${i}]: "${btnText}"`);
          chatBtn = buttons[i];
          break;
        }
      }

      if (chatBtn) {
        console.log('Clicking Agri Chat button in Streamlit...');
        await chatBtn.click();
        await new Promise(r => setTimeout(r, 3000));
        const newUrl = page.url();
        console.log('Streamlit URL after clicking Agri Chat:', newUrl);
        const newTitle = await page.title();
        console.log('Streamlit Title after click:', newTitle);
      }
    }
  } catch (err) {
    console.error('Test execution error:', err);
  } finally {
    await browser.close();
  }

  console.log(`\nSummary for ${url}:`);
  console.log(`Total Console Messages: ${consoleLogs.length}`);
  console.log(`Total Page Errors: ${pageErrors.length}`);
}

async function run() {
  const localHtmlPath = 'file:///' + __dirname.replace(/\\/g, '/') + '/index.html';
  console.log('Testing local HTML file:', localHtmlPath);
  await testUrl(localHtmlPath);
  await testUrl('http://localhost:8501');
}

run();

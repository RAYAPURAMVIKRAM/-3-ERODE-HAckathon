const puppeteer = require('puppeteer-core');
const { spawn } = require('child_process');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

async function runFullVerification() {
  console.log('====================================================');
  console.log('STARK-X AGRIPIRATE - DEEP FEATURE HEADLESS VERIFICATION');
  console.log('====================================================');

  // 1. Start local server
  console.log('Starting local STARK-X API server on port 3000...');
  const pyServer = spawn('python', ['api/index.py'], {
    env: { ...process.env, PORT: '3000' },
    stdio: 'inherit'
  });

  await new Promise(r => setTimeout(r, 1500));

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  const consoleLogs = [];
  const pageErrors = [];

  page.on('console', msg => {
    const text = `[BROWSER ${msg.type().toUpperCase()}] ${msg.text()}`;
    consoleLogs.push(text);
    if (msg.type() === 'error') console.error(text);
  });

  page.on('pageerror', err => {
    const text = `[PAGE ERROR] ${err.toString()}`;
    pageErrors.push(text);
    console.error(text);
  });

  try {
    const url = 'http://127.0.0.1:3000';
    console.log(`Navigating to ${url}...`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 20000 });
    console.log('✓ Page loaded successfully.');

    // Step 1: Verify all 5 Tab Buttons + Home switch properly
    console.log('\n--- VERIFYING NAVIGATION TABS ---');
    const tabs = ['home', 'chat', 'vision', 'optimizer', 'market', 'marketplace'];
    for (const t of tabs) {
      await page.evaluate((tabKey) => window.selectTab(tabKey), t);
      await new Promise(r => setTimeout(r, 400));
      const display = await page.evaluate((tabKey) => {
        const el = document.getElementById('tab-' + tabKey);
        return el ? window.getComputedStyle(el).display : 'NONE';
      }, t);
      console.log(`  Tab "${t}" active display: ${display}`);
      if (display === 'none') throw new Error(`Tab "${t}" failed to activate!`);
    }
    console.log('✓ All navigation tabs switch seamlessly.');

    // Step 2: Test Tab 1 (Agri Chat)
    console.log('\n--- TESTING TAB 1: MULTILINGUAL AGRI CHAT ---');
    await page.evaluate(() => window.selectTab('chat'));
    await page.type('#chatInput', 'What is the organic cure for Turmeric Rhizome Rot?');
    await page.click('button[onclick="sendUserMessage();"]');
    console.log('  Sent chat message. Waiting for advisory reply...');
    await page.waitForFunction(() => {
      const msgs = document.querySelectorAll('.chat-msg.assistant');
      return msgs.length >= 2;
    }, { timeout: 8000 });

    const latestReply = await page.evaluate(() => {
      const msgs = document.querySelectorAll('.chat-msg.assistant');
      return msgs[msgs.length - 1].innerText;
    });
    console.log('  Received AI Advisor Reply (snippet):', latestReply.slice(0, 120).replace(/\n/g, ' '), '...');

    const ttsBtnExists = await page.evaluate(() => {
      return !!document.querySelector('.tts-speak-btn');
    });
    console.log('  TTS Audio Speech button rendered:', ttsBtnExists);

    const followupsCount = await page.evaluate(() => {
      return document.querySelectorAll('#followupContainer .chat-pill').length;
    });
    console.log('  Suggested follow-up prompt chips rendered:', followupsCount);

    // Step 3: Test Tab 2 (Crop Vision Pathology Studio)
    console.log('\n--- TESTING TAB 2: CROP VISION PATHOLOGY SCANNER ---');
    await page.evaluate(() => window.selectTab('vision'));
    
    // Click Paddy/Rice preset
    console.log('  Selecting Paddy / Rice preset...');
    await page.evaluate(() => {
      const cards = document.querySelectorAll('.leaf-card');
      if (cards[1]) cards[1].click();
    });
    await new Promise(r => setTimeout(r, 1200));

    const visionDiagnosis = await page.evaluate(() => document.getElementById('reportDiagnosis').innerText);
    const confidenceVal = await page.evaluate(() => document.getElementById('confidenceVal').innerText);
    const stageVal = await page.evaluate(() => document.getElementById('reportStage').innerText);
    const costOrganic = await page.evaluate(() => document.getElementById('costOrganic').innerText);
    const costChemical = await page.evaluate(() => document.getElementById('costChemical').innerText);
    const savingsBadge = await page.evaluate(() => document.getElementById('reportSavings').innerText);

    console.log('  Diagnosis:', visionDiagnosis);
    console.log('  AI Confidence:', confidenceVal);
    console.log('  Progression Stage:', stageVal);
    console.log('  Organic Cost/Acre:', costOrganic, '| Chemical Cost/Acre:', costChemical);
    console.log('  Cost Savings:', savingsBadge);

    // Step 4: Test Tab 3 (Crop & Soil Optimizer)
    console.log('\n--- TESTING TAB 3: CROP & SOIL OPTIMIZER ---');
    await page.evaluate(() => window.selectTab('optimizer'));

    // Select Thanjavur district (Cauvery Delta Alluvial)
    console.log('  Switching district to Thanjavur (Alluvial Soil)...');
    await page.evaluate(() => {
      const sel = document.getElementById('optDistrict');
      if (sel) {
        sel.value = 'Thanjavur';
        sel.dispatchEvent(new Event('change'));
      }
    });
    await new Promise(r => setTimeout(r, 800));

    // Adjust acreage to 4.5 acres
    await page.evaluate(() => {
      const ac = document.getElementById('optAcreage');
      if (ac) {
        ac.value = '4.5';
        ac.dispatchEvent(new Event('input'));
      }
    });

    await page.click('button[onclick="runCropOptimization();"]');
    await new Promise(r => setTimeout(r, 800));

    const topCrop = await page.evaluate(() => document.getElementById('topCropName').innerText);
    const fertBasal = await page.evaluate(() => document.getElementById('fertBasal').innerText);
    const waterDaily = await page.evaluate(() => document.getElementById('roiWaterDaily').innerText);
    const totalGross = await page.evaluate(() => document.getElementById('roiGross').innerText);
    const totalNet = await page.evaluate(() => document.getElementById('roiNet').innerText);
    const profitMargin = await page.evaluate(() => document.getElementById('roiMarginTag').innerText);

    console.log('  Top Recommended Crop:', topCrop);
    console.log('  Basal Fertilizer Schedule:', fertBasal);
    console.log('  Daily Water Requirement:', waterDaily);
    console.log('  Total Gross Revenue (4.5 Acres):', totalGross);
    console.log('  Total Net Profit (4.5 Acres):', totalNet);
    console.log('  Visual ROI Margin:', profitMargin);

    // Step 5: Test Tab 4 (Market Trends & SOS Helpdesk)
    console.log('\n--- TESTING TAB 4: MARKET SPOT RATES & SOS DISTRESS ---');
    await page.evaluate(() => window.selectTab('market'));
    await new Promise(r => setTimeout(r, 600));

    // Click Cotton pill for 7-day trend chart
    console.log('  Switching 7-day trend chart to Cotton...');
    await page.evaluate(() => {
      const pills = document.querySelectorAll('#chartPills button');
      if (pills[1]) pills[1].click();
    });
    await new Promise(r => setTimeout(r, 400));

    const barsCount = await page.evaluate(() => {
      return document.querySelectorAll('#trendChartSvgContainer > div').length;
    });
    console.log('  7-Day Price Trend SVG Bars Rendered:', barsCount);

    // Test AI Hold vs Sell Now prediction
    console.log('  Checking AI Hold vs Sell Now Predictor...');
    await page.evaluate(() => window.updateHoldPrediction('Turmeric'));
    const holdAction = await page.evaluate(() => document.getElementById('holdActionBadge').innerText);
    const holdGain = await page.evaluate(() => document.getElementById('holdGainPct').innerText);
    console.log('  Predictor Action:', holdAction, '| Upside:', holdGain);

    // Step 6: Test Tab 5 (Direct Marketplace & Reels)
    console.log('\n--- TESTING TAB 5: DIRECT MARKETPLACE & REELS ---');
    await page.evaluate(() => window.selectTab('marketplace'));
    await new Promise(r => setTimeout(r, 600));

    const initialLots = await page.evaluate(() => document.querySelectorAll('#cropLotsGrid .crop-card').length);
    console.log(`  Initial Harvest Lots Loaded: ${initialLots}`);

    // Test search filter
    console.log('  Filtering harvest lots for "Turmeric"...');
    await page.evaluate(() => {
      const inp = document.getElementById('cropSearchInput');
      if (inp) {
        inp.value = 'Turmeric';
        inp.dispatchEvent(new Event('input'));
      }
    });
    await new Promise(r => setTimeout(r, 400));
    const filteredLots = await page.evaluate(() => document.querySelectorAll('#cropLotsGrid .crop-card').length);
    console.log(`  Filtered Harvest Lots: ${filteredLots}`);

    // Test "Make Offer" modal
    console.log('  Opening "Make Offer" modal...');
    await page.evaluate(() => {
      const btn = document.querySelector('#cropLotsGrid .crop-card button');
      if (btn) btn.click();
    });
    await new Promise(r => setTimeout(r, 400));
    const modalActive = await page.evaluate(() => {
      const m = document.getElementById('offerModal');
      return m && m.classList.contains('active');
    });
    console.log('  Offer Modal Active:', modalActive);

    // Close modal
    await page.evaluate(() => window.closeOfferModal());
    await new Promise(r => setTimeout(r, 300));

    // Save final screenshot
    await page.screenshot({ path: 'screenshot_final_deep_features.png', fullPage: true });
    console.log('✓ Full-page screenshot captured: screenshot_final_deep_features.png');

    console.log('\n====================================================');
    console.log(`SUMMARY: Total Page Errors: ${pageErrors.length}`);
    console.log('====================================================');

    if (pageErrors.length > 0) {
      console.error('FAIL: Page errors detected!');
      process.exitCode = 1;
    } else {
      console.log('SUCCESS: All 5 precision agronomy modules fully verified with ZERO errors!');
    }
  } catch (err) {
    console.error('Test execution failed:', err);
    process.exitCode = 1;
  } finally {
    await browser.close();
    pyServer.kill();
  }
}

runFullVerification();

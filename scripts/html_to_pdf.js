// Print standalone HTML files to PDF with the preinstalled headless Chromium.
// Usage: node scripts/html_to_pdf.js in.html out.pdf [in2.html out2.pdf ...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i += 2) {
    await page.goto('file://' + path.resolve(args[i]));
    await page.pdf({ path: args[i + 1], format: 'Letter', preferCSSPageSize: true, printBackground: true });
    console.log('wrote', args[i + 1]);
  }
  await browser.close();
})();

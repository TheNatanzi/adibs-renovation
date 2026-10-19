const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w,name] of [[1280,'desk'],[400,'phone']]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto('file://' + process.argv[2], { waitUntil: 'load', timeout: 20000 }).catch(()=>{});
    await p.waitForTimeout(800);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    console.log(name, 'scrollWidth', sw);
    await p.screenshot({ path: process.argv[3] + '-' + name + '.png', fullPage: true });
  }
  await b.close();
})();

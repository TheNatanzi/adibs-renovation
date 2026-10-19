const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w,name] of [[1280,'desk'],[400,'phone']]) {
    const p = await b.newPage({ viewport: { width: w, height: 1100 } });
    await p.goto(process.argv[2], { waitUntil: 'networkidle' });
    await p.waitForTimeout(800);
    console.log(name, await p.evaluate(() => [document.documentElement.scrollWidth, document.querySelectorAll('tbody tr').length, (document.querySelector('#cnt')||{}).textContent]));
    await p.screenshot({ path: process.argv[3] + '-' + name + '.png' });
  }
  await b.close();
})();

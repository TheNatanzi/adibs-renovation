const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [html,pdf] of [['index.html','Adibs-Store-Toolkit.pdf'],['drawings.html','Adibs-Drawings.pdf'],['storage.html','Adibs-Storage-Toolkit.pdf']]) {
    await p.goto('file://' + process.argv[2] + '/' + html, { waitUntil: 'networkidle', timeout: 60000 }).catch(e=>console.log('goto',e.message));
    await p.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'); await Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))); });
    await p.emulateMedia({ media: 'print' });
    await p.pdf({ path: process.argv[2] + '/' + pdf, format: 'Tabloid', landscape: true, printBackground: true, margin: { top: '0.4in', bottom: '0.4in', left: '0.4in', right: '0.4in' } });
    console.log('wrote', pdf);
  }
  await b.close();
})();

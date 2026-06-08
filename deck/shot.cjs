const puppeteer = require('/Users/ayushgarg/.local/lib/node_modules/puppeteer');
const path = require('path');
const CHROME = process.env.HOME + '/.cache/puppeteer/chrome/mac_arm-148.0.7778.97/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
(async () => {
  const b = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve('deck/slides_filled.html'), { waitUntil: 'networkidle0' });
  const slides = await p.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({ path: `deck/slides/${String(i + 1).padStart(2, '0')}.png` });
  }
  const box = async (sel) => p.$eval(sel, (el) => {
    const r = el.getBoundingClientRect(), s = el.closest('.slide').getBoundingClientRect();
    return { x: r.x - s.x, y: r.y - s.y, w: r.width, h: r.height };
  });
  const boxes = { search: await box('#vid-search'), term: await box('#vid-term') };
  require('fs').writeFileSync('deck/video_boxes.json', JSON.stringify(boxes));
  await b.close();
  console.log('shot ' + slides.length + ' slides + boxes');
})();

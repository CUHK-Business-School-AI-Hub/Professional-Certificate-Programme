/* Export the existing English HTML deck; no content is rewritten here. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
(async () => {
  const root = path.resolve(__dirname, '..');
  const qa = process.env.COURSE_QA_DIR || path.resolve(root, '../build/ventures-package');
  fs.mkdirSync(qa, {recursive:true});
  const file = path.join(root, 'slides/AI-Ventures-202612-Slides-1.html');
  const chrome = process.env.CHROME_BIN || (process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : undefined);
  const browser = await chromium.launch({headless:true, ...(chrome ? {executablePath:chrome}: {})});
  try {
    const page = await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
    const errors=[]; page.on('pageerror', e=>errors.push(e.message));
    await page.goto(pathToFileURL(file).href); await page.evaluate(()=>document.fonts.ready);
    const count = await page.locator('.slide').count();
    const badImages = await page.evaluate(()=>[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt));
    if(count!==83 || badImages.length || errors.length) throw Error(JSON.stringify({count,badImages,errors}));
    await page.emulateMedia({media:'print'});
    await page.pdf({path:file.replace(/\.html$/,'.pdf'),printBackground:true,preferCSSPageSize:true});
    await page.emulateMedia({media:'screen'});
    for (const n of [1,45,59,71,72,83]) {
      await page.evaluate(n=>{location.hash='slide-'+n},n); await page.waitForTimeout(80);
      await page.screenshot({path:path.join(qa,`slide-${n}.png`)});
    }
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>{location.hash='slide-71'}); await page.waitForTimeout(80);
    await page.screenshot({path:path.join(qa,'phone-71.png')});
    await page.keyboard.press('End');
    const end=await page.locator('#position').textContent();
    fs.writeFileSync(path.join(qa,'slides-export.json'),JSON.stringify({count,badImages,errors,end},null,2));
    console.log('Exported 83-page PDF and slide previews.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});

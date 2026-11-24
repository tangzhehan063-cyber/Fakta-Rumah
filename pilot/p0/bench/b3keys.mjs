import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png' };
const server = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); });
await new Promise(r => server.listen(0, r)); const port = server.address().port;
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const frames = [10,20,30,40,45,50,55,60,65,70,80,89];
fs.mkdirSync(path.join(ROOT, 'bench/b3out'), { recursive: true });
for (const [tag, cut, src] of [['kS1',0,'S1'],['kK1',0,'K1'],['kK2',0,'K2'],['kS2',0,'S2']]) {
  const page = await browser.newPage({ viewport: { width: 540, height: 960 } });
  page.on('pageerror', e => console.log('[err]', e.message.slice(0, 200)));
  await page.goto(`http://localhost:${port}/bench/b3.html?scale=0.5&cut=${cut}&step=4&src=${src}`); await page.waitForFunction('window.__ready===true', null, { timeout: 120000 });
  await page.evaluate(() => window.renderClip(0));
  const ts = [];
  for (const f of frames) { const a = Date.now(); await page.evaluate(fr => window.renderClip(fr), f); await page.locator('canvas').screenshot({ path: path.join(ROOT, `bench/b3out/${tag}_f${f}.png`) }); ts.push(Date.now() - a); }
  console.log(tag, 'ms/frame (render+screenshot png):', Math.round(ts.reduce((a, b) => a + b) / ts.length));
  await page.close();
}
await browser.close(); server.close();

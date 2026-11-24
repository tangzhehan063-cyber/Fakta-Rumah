// Render P0 jalur WEB: Three.js + Chromium headless (SwiftShader) lewat Playwright.
// pakai: node web/render.mjs stills [draft|final] | clip [scale] [seconds-override]
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.mjs': 'text/javascript' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]).replace(/^\/web\/?$/, '/web/index.html'));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, r));
const port = server.address().port;

const mode = process.argv[2] || 'stills';
const quality = process.argv[3] || 'final';
const scale = mode === 'clip' ? parseFloat(process.argv[3] || '0.5') : 1;
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'] });
const scene = JSON.parse(fs.readFileSync(path.join(ROOT, 'spec/scene.json'), 'utf8'));
const W = Math.round(scene.format.width * (mode === 'clip' ? scale : 1)), H = Math.round(scene.format.height * (mode === 'clip' ? scale : 1));
const page = await browser.newPage({ viewport: { width: W, height: H } });
page.on('console', m => { if (['error', 'warning'].includes(m.type())) console.log('[page]', m.text().slice(0, 200)); });
page.on('pageerror', e => console.log('[pageerror]', e.message.slice(0, 300)));
const q = mode === 'clip' ? 'final' : quality;
await page.goto(`http://localhost:${port}/web/index.html?q=${q}&scale=${scale}`);
await page.waitForFunction('window.__ready === true', null, { timeout: 120000 });
const timings = {};
if (mode === 'stills') {
  fs.mkdirSync(path.join(ROOT, 'out/web'), { recursive: true });
  for (const name of Object.keys(scene.cameras)) {
    const t0 = Date.now();
    await page.evaluate(n => window.renderShot(n), name);
    await page.evaluate(n => window.renderShot(n), name); // pass kedua: transmission/AO stabil
    await page.locator('canvas').screenshot({ path: path.join(ROOT, `out/web/${name}_${quality}.png`) });
    timings[name] = (Date.now() - t0) / 1000;
    console.log(name, timings[name].toFixed(1) + 's');
  }
} else {
  const secs = parseFloat(process.argv[4] || scene.clip.seconds);
  const n = Math.round(secs * scene.format.fps);
  scene.clip.seconds = secs;
  fs.mkdirSync(path.join(ROOT, 'frames/web'), { recursive: true });
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    await page.evaluate(([fr, nn]) => { return window.renderClip(fr); }, [f, Math.round(scene.clip.seconds * scene.format.fps)]);
    await page.locator('canvas').screenshot({ path: path.join(ROOT, `frames/web/f${String(f).padStart(4, '0')}.png`) });
    if (f % 10 === 0) console.log('frame', f, '/', n, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  console.log('total', ((Date.now() - t0) / 1000).toFixed(0) + 's untuk', n, 'frame');
}
fs.writeFileSync(path.join(ROOT, `out/web/timings_${mode}_${quality}.json`), JSON.stringify(timings, null, 1));
await browser.close(); server.close();

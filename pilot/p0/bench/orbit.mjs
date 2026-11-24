// Menghasilkan frame orbit isometrik: tiap frame = dua reproyeksi (dari dua keyframe terdekat) + bobot; dicampur di Remotion.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = process.argv[2]; const NF = parseInt(process.argv[3] || '114'); const AZ0 = 41, AZ1 = 49, KEYS = [41, 43, 45, 47, 49];
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png' };
const server = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); });
await new Promise(r => server.listen(0, r)); const port = server.address().port;
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
fs.mkdirSync(OUT, { recursive: true });
const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;   // easeInOutQuad
const meta = []; const need = {};   // key -> [frames]
for (let f = 0; f < NF; f++) {
  const az = AZ0 + (AZ1 - AZ0) * ease(f / (NF - 1));
  let i = Math.min(KEYS.length - 2, Math.max(0, Math.floor((az - AZ0) / 2))); const w = (az - KEYS[i]) / 2;
  meta.push({ f, az, a: KEYS[i], b: KEYS[i + 1], w: Math.min(1, Math.max(0, w)) });
  (need[KEYS[i]] ||= []).push({ f, az, role: 'a' }); (need[KEYS[i + 1]] ||= []).push({ f, az, role: 'b' });
}
const t0 = Date.now(); let n = 0;
for (const key of Object.keys(need)) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.log('[err]', e.message.slice(0, 200)));
  await page.goto(`http://localhost:${port}/bench/orbit.html?key=${key}`); await page.waitForFunction('window.__ready===true', null, { timeout: 180000 });
  for (const it of need[key]) {
    await page.evaluate(az => window.renderAz(az), it.az);
    await page.locator('canvas').screenshot({ path: path.join(OUT, `f${String(it.f).padStart(3, '0')}_${it.role}.jpg`), type: 'jpeg', quality: 93 });
    n++; if (n % 40 === 0) console.log(n, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  await page.close();
}
fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify(meta));
console.log('selesai', n, 'gambar,', ((Date.now() - t0) / 1000).toFixed(0), 's');
await browser.close(); server.close();

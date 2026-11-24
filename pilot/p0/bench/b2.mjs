import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const mime = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png' };
const server = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p)) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); });
await new Promise(r => server.listen(0, r)); const port = server.address().port;
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const variants = JSON.parse(process.argv[2]); const par = +process.argv[3] || 1; const N = 12; const res = [];
async function run(v, k) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  const qs = new URLSearchParams({ n: v.n, blur: v.blur || 0, sweep: v.sweep ? 1 : 0, part: v.part || 0 });
  await page.goto(`http://localhost:${port}/bench/b2.html?${qs}`); await page.waitForFunction('window.__ready===true');
  await page.evaluate(() => window.setFrame(0)); await page.screenshot({ type: 'jpeg', quality: 90 });
  const t0 = Date.now();
  for (let i = 0; i < N; i++) { await page.evaluate(f => window.setFrame(f), i * 7); await page.screenshot({ type: 'jpeg', quality: 90 }); }
  const dt = (Date.now() - t0) / N; await page.close(); return dt;
}
for (const v of variants) {
  const t0 = Date.now();
  const ts = await Promise.all(Array.from({ length: par }, (_, k) => run(v, k)));
  const wall = Date.now() - t0;
  const row = { name: v.name, parallel: par, ms_per_frame_per_worker: Math.round(ts.reduce((a, b) => a + b) / ts.length), effective_ms_per_frame: Math.round(ts.reduce((a, b) => a + b) / ts.length / par) };
  console.log(JSON.stringify(row)); res.push(row);
}
fs.writeFileSync(path.join(ROOT, `bench/b2_result_p${par}.json`), JSON.stringify(res, null, 1));
await browser.close(); server.close();

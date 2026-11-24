// B1: biaya Three.js per frame untuk jalur kamera P0 dengan variasi pengaturan (bukan kualitas akhir)
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module'; import { fileURLToPath } from 'node:url';
const { chromium } = createRequire(import.meta.url)('playwright');
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png' };
const server = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); });
await new Promise(r => server.listen(0, r)); const port = server.address().port;
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const variants = JSON.parse(process.argv[2]);
const N = 8, FR = 90;
const out = [];
for (const v of variants) {
  const scale = v.scale || 1;
  const page = await browser.newPage({ viewport: { width: Math.round(1080 * scale), height: Math.round(1920 * scale) } });
  const qs = new URLSearchParams({ q: 'final', scale: String(scale), sh: String(v.sh ?? 4096), static: v.static ? '1' : '0', ao: v.ao === false ? '0' : '1', ms: String(v.ms ?? 4), dof: v.dof === false ? '0' : '1' });
  await page.goto(`http://localhost:${port}/bench/web3d.html?${qs}`);
  await page.waitForFunction('window.__ready === true', null, { timeout: 120000 });
  await page.evaluate(() => window.renderClip(0)); // pemanasan + pembuatan shadow map
  const t0 = Date.now(); const tR = []; const tS = [];
  for (let i = 0; i < N; i++) {
    const f = Math.round(i * (FR - 1) / (N - 1));
    const a = Date.now(); await page.evaluate(([fr, n]) => window.renderClip(fr), [f, FR]); const b = Date.now();
    await page.locator('canvas').screenshot({ type: 'jpeg', quality: 90 }); const c = Date.now();
    tR.push(b - a); tS.push(c - b);
  }
  const avg = a => Math.round(a.reduce((x, y) => x + y, 0) / a.length);
  const row = { name: v.name, scale, render_ms: avg(tR), screenshot_ms: avg(tS), total_ms: avg(tR) + avg(tS) };
  console.log(JSON.stringify(row)); out.push(row); await page.close();
}
fs.writeFileSync(path.join(ROOT, 'bench/b1_result.json'), JSON.stringify(out, null, 1));
await browser.close(); server.close();

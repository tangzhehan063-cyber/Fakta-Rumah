#!/usr/bin/env python3
"""Mengukur sebuah perintah: waktu dinding, RAM puncak (jumlah RSS seluruh pohon proses), CPU (inti rata-rata/puncak).
pakai: python3 bench/measure.py <label> -- perintah ...   -> mencetak JSON satu baris dan menambah ke bench/results.jsonl"""
import json, os, subprocess, sys, time
PAGE = os.sysconf('SC_PAGE_SIZE'); HZ = os.sysconf('SC_CLK_TCK')

def children_map():
    m = {}
    for p in os.listdir('/proc'):
        if not p.isdigit(): continue
        try:
            with open(f'/proc/{p}/stat') as f: s = f.read()
            rest = s[s.rindex(')') + 2:].split()
            ppid = int(rest[1]); ut = int(rest[11]); st = int(rest[12])
            with open(f'/proc/{p}/statm') as f: rss = int(f.read().split()[1]) * PAGE
            m[int(p)] = (ppid, ut + st, rss)
        except Exception: pass
    return m

def tree(root, m):
    keep = {root}; changed = True
    while changed:
        changed = False
        for pid, (pp, _, _) in m.items():
            if pp in keep and pid not in keep: keep.add(pid); changed = True
    return keep

label = sys.argv[1]; cmd = sys.argv[sys.argv.index('--') + 1:]
t0 = time.time(); p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
peak_rss = 0; prev_cpu = None; prev_t = t0; cores = []; rss_series = []
cpu_total_ticks_seen = {}
while p.poll() is None:
    time.sleep(0.5); m = children_map(); ids = tree(p.pid, m)
    rss = sum(m[i][2] for i in ids if i in m); peak_rss = max(peak_rss, rss); rss_series.append((round(time.time() - t0, 1), rss // 1048576))
    for i in ids:
        if i in m: cpu_total_ticks_seen[i] = max(cpu_total_ticks_seen.get(i, 0), m[i][1])
    cpu_now = sum(cpu_total_ticks_seen.values()) / HZ; now = time.time()
    if prev_cpu is not None and now > prev_t: cores.append((cpu_now - prev_cpu) / (now - prev_t))
    prev_cpu, prev_t = cpu_now, now
out = p.stdout.read(); wall = time.time() - t0
cpu_s = sum(cpu_total_ticks_seen.values()) / HZ
res = {'label': label, 'exit': p.returncode, 'wall_s': round(wall, 1), 'peak_rss_mb': peak_rss // 1048576, 'cpu_seconds': round(cpu_s, 1),
       'avg_cores': round(cpu_s / wall, 2), 'peak_cores': round(max(cores), 2) if cores else None,
       'rss_start_mb': rss_series[len(rss_series) // 4][1] if rss_series else None, 'rss_end_mb': rss_series[-1][1] if rss_series else None}
json.dump(rss_series, open(os.path.join(os.path.dirname(__file__), f'rss_{label}.json'), 'w'))
open(os.path.join(os.path.dirname(__file__), 'results.jsonl'), 'a').write(json.dumps(res) + '\n')
open(os.path.join(os.path.dirname(__file__), f'log_{label}.txt'), 'w').write(out)
print(json.dumps(res))

import React from 'react';
import { AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';

// ---------- util deterministik (tanpa Math.random) ----------
const hash = (n: number) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const ease = Easing.inOut(Easing.cubic);
const easeSine = Easing.inOut(Easing.sin);
const P = (n: string) => staticFile(`plates/${n}`);
const FILL: React.CSSProperties = { position: 'absolute', left: 0, top: 0, width: 1080, height: 1920 };

// ---------- bidang berkedalaman ----------
const Plane: React.FC<{ src: string; dx?: number; dy?: number; scale?: number; opacity?: number; origin?: string }> = ({ src, dx = 0, dy = 0, scale = 1, opacity = 1, origin = '50% 50%' }) => (
  <Img src={src} style={{ ...FILL, opacity, transformOrigin: origin, transform: `translate3d(${dx}px, ${dy}px, 0) scale(${scale})` }} />
);

// ---------- SHOT A (0–4 dtk): tracking lateral + parallax; tanpa zoom, tanpa partikel ----------
const ShotA: React.FC = () => {
  const f = useCurrentFrame();
  const t = easeSine(interpolate(f, [0, 119], [0, 1]));
  const dx = interpolate(t, [0, 1], [-26, 26]);
  // bg paling lambat, lapisan dekat paling cepat (benda dekat bergerak lebih jauh)
  return (
    <AbsoluteFill style={{ background: '#bfc0c0', overflow: 'hidden' }}>
      <Plane src={P('s1_bg.jpg')} dx={dx * 0.15} scale={1.05} />
      <Plane src={P('s1_L2.png')} dx={dx * 0.35} scale={1.05} />
      <Plane src={P('s1_L1.png')} dx={dx * 0.7} scale={1.05} />
      <Plane src={P('s1_L0.png')} dx={dx * 1.2} scale={1.05} />
    </AbsoluteFill>
  );
};

// ---------- SHOT B (4–8 dtk): push-in lambat + rack focus + satu sapuan cahaya ----------
const ShotB: React.FC = () => {
  const f = useCurrentFrame(); // 0..119 lokal
  const t = ease(interpolate(f, [0, 119], [0, 1]));
  const sc = (k: number) => 1.04 + t * (0.035 * k);          // push-in; lapisan dekat lebih besar
  // rack focus: fokus awal di lapisan jauh/tengah, pindah ke dekat di akhir
  const farSharp = interpolate(f, [10, 55], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) * (1 - interpolate(f, [80, 115], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const nearSharp = interpolate(f, [70, 115], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const nearBlurStart = 1 - interpolate(f, [0, 40], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const nearSharpOp = Math.max(nearSharp, nearBlurStart * 0.0, 1 - nearBlurStart) * (f < 70 ? 1 - interpolate(f, [0, 50], [0, 0.9], { extrapolateRight: 'clamp' }) * 0 : 1);
  // sapuan cahaya: pita gradien miring melintas 2 dtk (alpha rendah, hangat netral)
  const sweepPos = interpolate(f, [25, 85], [-30, 130], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const sweepAlpha = interpolate(f, [25, 40, 70, 85], [0, 0.16, 0.16, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const pairs: [string, number, number][] = [['s2_L2', 0.85, 0.2], ['s2_L1', 1.15, 0.5], ['s2_L0', 1.6, 0.9]];
  return (
    <AbsoluteFill style={{ background: '#bfc0c0', overflow: 'hidden' }}>
      <Plane src={P('s2_bg_blur.jpg')} scale={sc(0.3)} opacity={1} />
      <Plane src={P('s2_bg.jpg')} scale={sc(0.3)} opacity={farSharp} />
      {pairs.map(([n, k, focusBias], i) => {
        const sharp = i === 2 ? nearSharp : farSharp * (i === 1 ? 0.9 : 1);
        return (
          <React.Fragment key={n}>
            <Plane src={P(`${n}_blur.png`)} scale={sc(k)} opacity={1} />
            <Plane src={P(`${n}.png`)} scale={sc(k)} opacity={sharp} />
          </React.Fragment>
        );
      })}
      <div style={{ ...FILL, mixBlendMode: 'soft-light', opacity: sweepAlpha, background: `linear-gradient(105deg, rgba(255,255,255,0) ${sweepPos - 14}%, rgba(255,244,228,1) ${sweepPos}%, rgba(255,255,255,0) ${sweepPos + 14}%)` }} />
    </AbsoluteFill>
  );
};

// ---------- SHOT C (8–12 dtk): kamera statis; kabut tipis + debu di berkas cahaya ----------
const ShotC: React.FC = () => {
  const f = useCurrentFrame();
  const fogX = interpolate(f, [0, 119], [-60, 40]);
  const dust = Array.from({ length: 70 }, (_, i) => {
    const bx = hash(i + 1) * 1080, by = hash(i + 91) * 1920, sp = 0.15 + hash(i + 7) * 0.35;
    const x = (bx + Math.sin(f * 0.02 * sp + i) * 22 + f * 0.12 * sp) % 1080;
    const y = (by - f * 0.35 * sp + 1920 * 4) % 1920;
    const r = 1.2 + hash(i + 33) * 1.8;
    const a = 0.12 + hash(i + 55) * 0.22;
    return <circle key={i} cx={x} cy={y} r={r} fill={`rgba(255,248,238,${a})`} />;
  });
  return (
    <AbsoluteFill style={{ background: '#bfc0c0', overflow: 'hidden' }}>
      <Plane src={P('s4_bg.jpg')} scale={1.0} />
      {/* kabut: dua gradien radial lambat, kontras sangat rendah */}
      <div style={{ ...FILL, opacity: 0.35, background: `radial-gradient(60% 35% at ${50 + fogX * 0.3}% 78%, rgba(235,238,240,0.55), rgba(235,238,240,0) 70%), radial-gradient(70% 30% at ${40 - fogX * 0.2}% 30%, rgba(235,238,240,0.35), rgba(235,238,240,0) 70%)` }} />
      {/* debu hanya di dalam berkas cahaya miring */}
      <svg width={1080} height={1920} style={{ ...FILL, WebkitMaskImage: 'linear-gradient(115deg, rgba(0,0,0,0) 18%, rgba(0,0,0,1) 42%, rgba(0,0,0,1) 58%, rgba(0,0,0,0) 82%)', maskImage: 'linear-gradient(115deg, rgba(0,0,0,0) 18%, rgba(0,0,0,1) 42%, rgba(0,0,0,1) 58%, rgba(0,0,0,0) 82%)' }}>{dust}</svg>
    </AbsoluteFill>
  );
};

// ---------- susunan 12 dtk: potong keras A→B, larut B→C ----------
export const Bench12: React.FC = () => {
  const f = useCurrentFrame();
  const dissolve = interpolate(f, [228, 240], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      <Sequence from={0} durationInFrames={120}><ShotA /></Sequence>
      <Sequence from={120} durationInFrames={120}><ShotB /></Sequence>
      <Sequence from={228} durationInFrames={132}><AbsoluteFill style={{ opacity: dissolve }}><ShotC /></AbsoluteFill></Sequence>
    </AbsoluteFill>
  );
};

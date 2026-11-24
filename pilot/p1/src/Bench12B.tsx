import React from 'react';
import { AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';

// ===== v2: plat berlapis dari 3D (latar bersih / tengah / subjek), rack focus yang benar, transisi bermotivasi =====
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const hash = (n: number) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const easeIO = Easing.inOut(Easing.cubic);
const easeSine = Easing.inOut(Easing.sin);
const P = (n: string) => staticFile(`plates2/${n}`);
const FILL: React.CSSProperties = { position: 'absolute', left: 0, top: 0, width: 1080, height: 1920 };

const Plane: React.FC<{ src: string; dx?: number; dy?: number; scale?: number; opacity?: number }> = ({ src, dx = 0, dy = 0, scale = 1, opacity = 1 }) => (
  <Img src={src} style={{ ...FILL, opacity, transform: `translate3d(${dx}px, ${dy}px, 0) scale(${scale})`, transformOrigin: '50% 55%' }} />
);

// ---------- A (0–3,8 dtk): tracking lateral, parallax 3 lapisan; tanpa zoom, tanpa partikel, tanpa blur ----------
const ShotA: React.FC = () => {
  const f = useCurrentFrame();
  const dx = interpolate(easeSine(interpolate(f, [0, 113], [0, 1])), [0, 1], [-24, 24]);
  return (
    <AbsoluteFill style={{ background: '#c8c9c9', overflow: 'hidden' }}>
      <Plane src={P('s1_BACK.jpg')} dx={dx * 0.5} scale={1.07} />
      <Plane src={P('s1_MID.png')} dx={dx * 0.68} scale={1.07} />
      <Plane src={P('s1_FRONT.png')} dx={dx * 0.85} scale={1.07} />
    </AbsoluteFill>
  );
};

// ---------- B (3,8–8,2 dtk): push-in lambat + rack focus (label → pipa) + sapuan cahaya halus ----------
const wt = (focus: number, depth: number) => Math.max(0, 1 - Math.abs(focus - depth)); // bobot ketajaman; selalu ada lapisan tajam
const ShotB: React.FC = () => {
  const f = useCurrentFrame(); // 0..131
  const t = easeIO(interpolate(f, [0, 131], [0, 1]));
  const focus = interpolate(easeIO(interpolate(f, [28, 100], [0, 1], clamp)), [0, 1], [0, 1]); // 0=latar(label) 1=pipa (cangkang depan tetap lembut: blur latar-depan)
  // keluar-fokus di 10 frame terakhir (transisi bermotivasi menuju C): fokus lepas ke luar subjek
  const out = interpolate(f, [121, 131], [0, 1], clamp);
  const layers: [string, number, number][] = [['BACK', 0, 0.05], ['MID', 1, 0.065], ['FRONT', 2, 0.08]]; // [nama, kedalaman, tambahan skala push-in]
  const sweepPos = interpolate(f, [14, 78], [-25, 125], clamp);
  const sweepA = interpolate(f, [14, 30, 62, 78], [0, 0.13, 0.13, 0], clamp);
  return (
    <AbsoluteFill style={{ background: '#c8c9c9', overflow: 'hidden' }}>
      {layers.map(([n, d, k]) => {
        const sc = 1.07 + t * k;
        const sharp = wt(focus, d) * (1 - out);
        const ext = n === 'BACK' ? 'jpg' : 'png';
        return (
          <React.Fragment key={n}>
            <Plane src={P(`s2_${n}_blur.${ext}`)} scale={sc} />
            <Plane src={P(`s2_${n}.${ext}`)} scale={sc} opacity={sharp} />
          </React.Fragment>
        );
      })}
      <div style={{ ...FILL, mixBlendMode: 'soft-light', opacity: sweepA, background: `linear-gradient(105deg, rgba(255,255,255,0) ${sweepPos - 16}%, rgba(255,246,232,1) ${sweepPos}%, rgba(255,255,255,0) ${sweepPos + 16}%)` }} />
    </AbsoluteFill>
  );
};

// ---------- C (8,2–12 dtk): kamera statis sudut tinggi; fokus mengendap; berkas cahaya + debu yang terbaca ----------
const ShotC: React.FC = () => {
  const f = useCurrentFrame(); // 0..113
  const settle = interpolate(f, [0, 22], [1, 0], { ...clamp, easing: Easing.out(Easing.cubic) }); // 1 = kabur, 0 = tajam
  const dust = Array.from({ length: 96 }, (_, i) => {
    const bx = hash(i + 1) * 1080, by = hash(i + 91) * 1920, sp = 0.2 + hash(i + 7) * 0.4;
    const x = (bx + Math.sin(f * 0.025 * sp + i * 1.7) * 18 + f * 0.1 * sp + 1080) % 1080;
    const y = (by - f * 0.3 * sp + 1920 * 4) % 1920;
    const r = 2.0 + hash(i + 33) * 2.6, a = 0.38 + hash(i + 55) * 0.34;
    return <circle key={i} cx={x} cy={y} r={r} fill={`rgba(255,250,242,${a})`} />;
  });
  const beam = 'linear-gradient(118deg, rgba(0,0,0,0) 14%, rgba(0,0,0,1) 40%, rgba(0,0,0,1) 60%, rgba(0,0,0,0) 86%)';
  return (
    <AbsoluteFill style={{ background: '#c8c9c9', overflow: 'hidden' }}>
      <Plane src={P('s4_blur.jpg')} scale={1.0} />
      <Plane src={P('s4.jpg')} scale={1.0} opacity={1 - settle} />
      {/* berkas cahaya jendela: gradien miring, kontras rendah (tanpa bloom) */}
      <div style={{ ...FILL, mixBlendMode: 'screen', opacity: 0.17, background: 'linear-gradient(118deg, rgba(255,246,232,0) 12%, rgba(255,246,232,1) 42%, rgba(255,246,232,1) 58%, rgba(255,246,232,0) 88%)' }} />
      <svg width={1080} height={1920} style={{ ...FILL, WebkitMaskImage: beam, maskImage: beam, opacity: 1 - settle * 0.6 }}>{dust}</svg>
    </AbsoluteFill>
  );
};

// ---------- susunan: A —potong keras→ B —potong pada lepas-fokus→ C (menetap dari kabur ke tajam) ----------
export const Bench12B: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Sequence from={0} durationInFrames={114}><ShotA /></Sequence>
    <Sequence from={114} durationInFrames={132}><ShotB /></Sequence>
    <Sequence from={246} durationInFrames={114}><ShotC /></Sequence>
  </AbsoluteFill>
);

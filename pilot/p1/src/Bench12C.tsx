import React from 'react';
import { AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';

// ===== v3: kamera ISOMETRIK (ortografik, azimuth 45, elevasi 35,264) yang bergerak =====
// A: truck kiri-kanan (ortografik: translasi kaku, TANPA parallax = benar secara fisik; satu plat overscan lebar)
// B: push-in ortografik + rack focus (cangkang depan -> pipa), plat berlapis
// C: orbit isometrik kecil (reproyeksi kedalaman dari 5 keyframe, dicampur) yang menetap dari kabur ke tajam
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
const easeIO = Easing.inOut(Easing.cubic);
const easeSine = Easing.inOut(Easing.sin);
const I = (n: string) => staticFile(`iso/${n}`);

// ---------- A (0-3,8 dtk) ----------
const PW = 3240, PH = 2112;
const ShotA: React.FC = () => {
  const f = useCurrentFrame();
  const t = easeSine(interpolate(f, [0, 113], [0, 1]));
  const xc = interpolate(t, [0, 1], [-930, 930]);   // pusat jendela relatif pusat plat (px)
  const yc = interpolate(t, [0, 1], [50, -50]);     // sedikit pedestal agar tidak datar
  return (
    <AbsoluteFill style={{ background: '#c9c7c2', overflow: 'hidden' }}>
      <Img src={I('A.jpg')} style={{ position: 'absolute', width: PW, height: PH, left: 540 - (PW / 2 + xc), top: 960 - (PH / 2 + yc) }} />
    </AbsoluteFill>
  );
};

// ---------- B (3,8-8,2 dtk) ----------
const BW = 1361, BH = 2419;
const wt = (focus: number, depth: number) => Math.max(0, 1 - Math.abs(focus - depth));
const ShotB: React.FC = () => {
  const f = useCurrentFrame(); // 0..131
  const z = interpolate(easeIO(interpolate(f, [0, 131], [0, 1])), [0, 1], [0.794, 1.0]); // zoom ortografik 1,26x
  const focus = interpolate(easeIO(interpolate(f, [20, 96], [0, 1])), [0, 1], [2, 1]);      // 2=cangkang depan -> 1=pipa
  const out = interpolate(f, [121, 131], [0, 1], clamp);
  const layers: [string, number, string][] = [['BACK', 0, 'jpg'], ['MID', 1, 'png'], ['FRONT', 2, 'png']];
  const st: React.CSSProperties = { position: 'absolute', width: BW, height: BH, left: 540 - BW / 2, top: 960 - BH / 2, transform: `scale(${z})`, transformOrigin: '50% 50%' };
  return (
    <AbsoluteFill style={{ background: '#c9c7c2', overflow: 'hidden' }}>
      {layers.map(([n, d, ext]) => (
        <React.Fragment key={n}>
          <Img src={I(`B_${n}_blur.${ext}`)} style={st} />
          <Img src={I(`B_${n}.${ext}`)} style={{ ...st, opacity: wt(focus, d) * (1 - out) }} />
        </React.Fragment>
      ))}
    </AbsoluteFill>
  );
};

// ---------- C (8,2-12 dtk): orbit isometrik 41 -> 49 derajat ----------
const NF = 114;
const easeQ = (x: number) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2);
const pad = (n: number) => String(n).padStart(3, '0');
const ShotC: React.FC = () => {
  const f = useCurrentFrame(); // 0..113
  const az = 41 + 8 * easeQ(f / (NF - 1));
  const i = Math.min(3, Math.max(0, Math.floor((az - 41) / 2)));
  const w = Math.min(1, Math.max(0, (az - (41 + 2 * i)) / 2));
  const blur = interpolate(f, [0, 20], [14, 0], { ...clamp, easing: Easing.out(Easing.cubic) });
  const full: React.CSSProperties = { position: 'absolute', left: 0, top: 0, width: 1080, height: 1920 };
  return (
    <AbsoluteFill style={{ background: '#c9c7c2', overflow: 'hidden', filter: blur > 0.3 ? `blur(${blur}px)` : undefined }}>
      <Img src={I(`orbit/f${pad(f)}_a.jpg`)} style={full} />
      <Img src={I(`orbit/f${pad(f)}_b.jpg`)} style={{ ...full, opacity: w }} />
    </AbsoluteFill>
  );
};

export const Bench12C: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Sequence from={0} durationInFrames={114}><ShotA /></Sequence>
    <Sequence from={114} durationInFrames={132}><ShotB /></Sequence>
    <Sequence from={246} durationInFrames={114}><ShotC /></Sequence>
  </AbsoluteFill>
);

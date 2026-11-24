import React from 'react';
import { Composition, Loop } from 'remotion';
import { Bench12 } from './Bench12';
import { Bench12B } from './Bench12B';
import { Bench12C } from './Bench12C';

export const FPS = 30;
const Bench60: React.FC = () => (
  <Loop durationInFrames={12 * FPS} times={5}><Bench12 /></Loop>
);

export const Root: React.FC = () => (
  <>
    <Composition id="Bench12" component={Bench12} durationInFrames={12 * FPS} fps={FPS} width={1080} height={1920} />
    <Composition id="Bench12B" component={Bench12B} durationInFrames={12 * FPS} fps={FPS} width={1080} height={1920} />
    <Composition id="Bench12C" component={Bench12C} durationInFrames={12 * FPS} fps={FPS} width={1080} height={1920} />
    <Composition id="Bench60" component={Bench60} durationInFrames={60 * FPS} fps={FPS} width={1080} height={1920} />
  </>
);

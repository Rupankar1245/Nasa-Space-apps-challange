import type { Measurement } from "./health-analysis";

const seeded = (seed: number) => {
  const x = Math.sin(seed * 999) * 10000;
  return x - Math.floor(x);
};

export function createDemoRecords(days = 14): Measurement[] {
  return Array.from({ length: days }, (_, i) => ({
    date: `D-${days - i - 1}`,
    heartRate: Math.round(65 + seeded(i + 1) * 11),
    sleep: Number((7.1 + seeded(i + 20) * 1.1 - i * 0.025).toFixed(1)),
    systolic: Math.round(111 + seeded(i + 40) * 13),
    mood: Math.min(5, Math.max(1, Math.round(3.5 + seeded(i + 60) * 1.5))),
    stress: Math.min(5, Math.max(1, Math.round(2.2 + seeded(i + 80) * 1.8)))
  })).reverse();
}

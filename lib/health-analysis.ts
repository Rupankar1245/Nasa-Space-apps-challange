export type Measurement = { date: string; heartRate: number; sleep: number; systolic: number; mood: number; stress: number };

export function median(values: number[]) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}

export function personalBaseline(records: Measurement[]) {
  if (records.length < 5) return { sufficient: false, sampleSize: records.length };
  return {
    sufficient: true,
    sampleSize: records.length,
    heartRate: median(records.map((r) => r.heartRate)),
    sleep: median(records.map((r) => r.sleep)),
    systolic: median(records.map((r) => r.systolic))
  };
}

export function classifyMeasurement(value: number, baseline: number | null | undefined) {
  if (baseline == null) return { level: "AMBER" as const, reason: "Personal baseline not yet established." };
  const deviation = Math.abs(value - baseline) / baseline;
  return deviation > 0.15
    ? { level: "AMBER" as const, reason: "Measurement deviates from the personal reference baseline; reassess and review context." }
    : { level: "GREEN" as const, reason: "No concerning deviation from the personal reference baseline detected." };
}

"use client";

import { useMemo, useState } from "react";
import { Activity, AlertTriangle, ArrowUpRight, BookOpen, CheckCircle2, ClipboardCheck, Clock3, Dumbbell, HeartPulse, Home, Info, LineChart, Moon, Orbit, ShieldCheck, UserRound, Wind } from "lucide-react";
import { Line, LineChart as RechartsLineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { createDemoRecords } from "@/lib/demo-data";
import { personalBaseline } from "@/lib/health-analysis";

const nav = [
  ["Overview", Home], ["Health check", ClipboardCheck], ["Analytics", LineChart],
  ["Body map", UserRound], ["Risk assessment", ShieldCheck], ["Mission", Orbit], ["Guidance", BookOpen], ["Research", Info]
] as const;

export function CrewPulseApp() {
  const [records, setRecords] = useState(createDemoRecords());
  const [active, setActive] = useState("Overview");
  const [tasks, setTasks] = useState([false, true, false, false]);
  const baseline = useMemo(() => personalBaseline(records), [records]);
  const latest = records[records.length - 1];
  const handleHealthCheck = () => {
    const next = { ...latest, date: "NOW", heartRate: latest.heartRate + 1, sleep: 7.4, mood: 4, stress: 2 };
    setRecords([...records, next]);
    setActive("Overview");
  };

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark" /><strong>CrewPulse</strong></div>
      <p className="nav-label">Mission console</p>
      {nav.map(([label, Icon]) => <button key={label} className={`nav-item ${active === label ? "active" : ""}`} onClick={() => setActive(label)}><Icon size={16} /><span>{label}</span></button>)}
      <div className="side-footer"><div className="status">LOCAL / OFFLINE READY</div><br />Prototype decision support<br />No clinical diagnosis</div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="mission-meta"><div><b>MARS-EX SIM // AURORA</b><span>Long-duration mission simulation</span></div><div><b>DAY 120</b><span>of 540</span></div></div><div className="profile"><div className="status">SIMULATED DATA</div><div className="avatar">CP</div><span>CP-001</span></div></header>
      {active === "Overview" ? <Dashboard latest={latest} records={records} baseline={baseline} tasks={tasks} setTasks={setTasks} onHealthCheck={handleHealthCheck} /> : <ModulePage active={active} onHealthCheck={handleHealthCheck} />}
    </main>
  </div>;
}

function Dashboard({ latest, records, baseline, tasks, setTasks, onHealthCheck }: { latest: ReturnType<typeof createDemoRecords>[number]; records: ReturnType<typeof createDemoRecords>; baseline: ReturnType<typeof personalBaseline>; tasks: boolean[]; setTasks: (v: boolean[]) => void; onHealthCheck: () => void }) {
  const chartData = records.map((r) => ({ day: r.date, HR: r.heartRate, Sleep: r.sleep, Mood: r.mood }));
  const metrics = [["Heart rate", latest.heartRate, "BPM", HeartPulse], ["Blood pressure", `${latest.systolic}/72`, "mmHg", Activity], ["SpO₂", "98", "%", Wind], ["Temperature", "36.7", "°C", Activity], ["Sleep", latest.sleep, "hours", Moon], ["Mood", `${latest.mood}/5`, "score", UserRound]] as const;
  return <>
    <section className="hero"><div><div className="eyebrow">PERSONAL HEALTH CONSOLE / OVERVIEW</div><h1>Your health.<br />Your mission. <em style={{color:"var(--cyan)",fontStyle:"normal"}}>Your control.</em></h1><p className="lede">A calm, evidence-informed view of your current physiological state.</p></div><div className="hero-right"><div className="mission-day">120 <small>MISSION DAY</small></div><span className="status">ALL SYSTEMS MONITORED</span></div></section>
    <div className="grid metrics">{metrics.map(([label, value, unit, Icon]) => <div className="card metric" key={label}><div className="metric-head"><span>{label}</span><Icon size={15} /></div><div className="metric-value">{value} <span className="unit">{unit}</span></div><div className="metric-foot good">● Within monitoring criteria</div></div>)}</div>
    <div className="grid split"><div className="card"><div className="card-title"><h2>Health attention summary</h2><span>UPDATED JUST NOW</span></div><div className="summary-row"><div className="summary-pill"><b>06</b><span>within criteria</span></div><div className="summary-pill warn"><b>01</b><span>reassessment</span></div><div className="summary-pill"><b>00</b><span>medical review</span></div></div><div className="card-title"><h2>Recent health trends</h2><span>14 DAY WINDOW · SIMULATED</span></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><RechartsLineChart data={chartData}><XAxis dataKey="day" tick={{fill:"#718894",fontSize:10}} axisLine={false} tickLine={false}/><YAxis yAxisId="left" tick={{fill:"#718894",fontSize:10}} axisLine={false} tickLine={false}/><YAxis yAxisId="right" orientation="right" tick={{fill:"#718894",fontSize:10}} axisLine={false} tickLine={false}/><Tooltip contentStyle={{background:"#0b1922",border:"1px solid #29414d",fontSize:11}}/><Line yAxisId="left" type="monotone" dataKey="HR" stroke="#57d9d4" strokeWidth={2} dot={false}/><Line yAxisId="right" type="monotone" dataKey="Sleep" stroke="#f4b860" strokeWidth={2} dot={false}/><Line yAxisId="right" type="monotone" dataKey="Mood" stroke="#8ca7ff" strokeWidth={2} dot={false}/></RechartsLineChart></ResponsiveContainer></div></div>
      <div className="grid" style={{gap:14}}><div className="card"><div className="card-title"><h2>Daily tasks</h2><span>{tasks.filter(Boolean).length}/4 COMPLETE</span></div>{["Complete health check-in","Record sleep & recovery","Complete scheduled exercise","Review guidance brief"].map((task, i) => <label className="task" key={task}><input type="checkbox" checked={tasks[i]} onChange={() => { const copy=[...tasks]; copy[i]=!copy[i]; setTasks(copy); }} /><span>{task}</span><small>{i === 0 ? "2 min" : i === 2 ? "42 min" : "Today"}</small></label>)}<button className="action" onClick={onHealthCheck}><ClipboardCheck size={14}/> Open health check</button></div><div className="card"><div className="card-title"><h2>Recent events</h2><span>LIVE LOG</span></div><div className="event"><div className="event-icon"><CheckCircle2 size={14}/></div><div><p>Morning vitals recorded</p><small>Today · 08:42 · SIMULATED</small></div></div><div className="event"><div className="event-icon"><Dumbbell size={14}/></div><div><p>Exercise session completed</p><small>Yesterday · 17:20 · 42 min</small></div></div><div className="event"><div className="event-icon"><AlertTriangle size={14}/></div><div><p>Sleep trend flagged for review</p><small>Yesterday · 09:00 · AMBER</small></div></div></div></div>
    </div><div className="disclaimer"><strong>Prototype boundary:</strong> CrewPulse is a research-oriented decision-support prototype. It does not diagnose illness, replace mission medical protocols, or provide clinical advice. RED escalation thresholds are intentionally not configured without an approved protocol. Personal baseline: {baseline.sufficient ? `${baseline.sampleSize} valid observations` : "insufficient history"}.</div>
  </>;
}

export function ModulePage({ active, onHealthCheck = () => undefined }: { active: string; onHealthCheck?: () => void }) {
  const copy: Record<string, [string,string,string]> = {
    "Health check": ["Daily health check", "Record a local measurement set and keep your mission log current.", "Enter a new check-in"],
    "Analytics": ["Mission analytics", "Compare trends against your personal reference baseline. Simulated records are clearly labelled.", "View trend window"],
    "Body map": ["Body systems explorer", "Select a system to review spaceflight-related physiology, indicators, and monitoring methods.", "Explore systems"],
    "Risk assessment": ["Risk & attention review", "Deterministic prototype rules explain unusual observations without diagnosing disease.", "Review attention items"],
    "Mission": ["Mission environment", "Track mission context and sensor provenance. No exposure is inferred without a measurement source.", "Review environment"],
    "Guidance": ["Preventive guidance", "Short, evidence-linked briefs for sleep, exercise, stress, hydration, and escalation.", "Open guidance library"],
    "Research": ["Research library", "Starting points from official NASA research programs. Verify scope and currency before use.", "Browse references"]
  };
  const [title, body, cta] = copy[active];
  return <><section className="hero"><div><div className="eyebrow">CREWPULSE MODULE / {active.toUpperCase()}</div><h1>{title}</h1><p className="lede">{body}</p></div></section>{active === "Health check" ? <HealthCheckForm onSaved={onHealthCheck} /> : <div className="card module-card"><div className="module-icon"><Orbit size={24}/></div><h2>Module ready for your mission context</h2><p>{active === "Research" ? "NASA Human Research Program · NASA Open Science Data Repository · Human Research Roadmap" : "This prototype keeps records on this device and labels generated records as SIMULATED. Connect an approved data source before operational use."}</p><button className="action"><ArrowUpRight size={14}/>{cta}</button></div>}<div className="disclaimer"><strong>Scientific boundary:</strong> Educational guidance is not medical advice. Use the approved flight medical protocol for urgent or ambiguous situations.</div></>;
}

function HealthCheckForm({ onSaved }: { onSaved: () => void }) {
  const [saved, setSaved] = useState(false);
  return <form className="card module-card" onSubmit={(event) => { event.preventDefault(); setSaved(true); onSaved(); }}>
    <div className="module-icon"><ClipboardCheck size={24}/></div><h2>Capture a new check-in</h2>
    <div className="form-grid">
      <label>Heart rate <span>BPM</span><input type="number" min="1" max="250" defaultValue="68" required /></label>
      <label>Blood pressure <span>mmHg</span><input type="text" defaultValue="112/72" required /></label>
      <label>SpO₂ <span>%</span><input type="number" min="1" max="100" defaultValue="98" required /></label>
      <label>Sleep duration <span>hours</span><input type="number" min="0" max="24" step="0.1" defaultValue="7.4" required /></label>
      <label>Mood <span>1–5</span><input type="number" min="1" max="5" defaultValue="4" required /></label>
      <label>Stress <span>1–5</span><input type="number" min="1" max="5" defaultValue="2" required /></label>
    </div>
    <button className="action" type="submit"><CheckCircle2 size={14}/>{saved ? "Saved locally" : "Save simulated check-in"}</button>
    {saved && <p className="saved-note">Check-in saved with a local timestamp. This record is labelled SIMULATED and is not synchronized.</p>}
  </form>;
}

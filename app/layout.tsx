import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CrewPulse | Astronaut health decision support",
  description: "A local-first health monitoring prototype for long-duration missions."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}

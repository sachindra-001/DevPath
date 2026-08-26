import Link from "next/link";
import { Compass, ShieldCheck, Cpu, Code2 } from "lucide-react";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-border/80 bg-background/90 py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <div className="space-y-3 md:col-span-2">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-brand text-white">
                <Compass className="h-4 w-4" />
              </div>
              <span className="font-bold text-foreground">CPGS — Career Path Guidance System</span>
            </div>
            <p className="max-w-md text-sm text-muted-foreground leading-relaxed">
              Interactive structured learning roadmaps with an AI-powered resource discovery
              pipeline. Researched by AI, verified and curated by human experts.
            </p>
            <div className="flex items-center gap-4 pt-2 text-xs text-muted-foreground">
              <span className="flex items-center gap-1">
                <Cpu className="h-3.5 w-3.5 text-primary" /> OpenAI gpt-4o-mini
              </span>
              <span className="flex items-center gap-1">
                <ShieldCheck className="h-3.5 w-3.5 text-teal-600" /> Human in the loop
              </span>
              <span className="flex items-center gap-1">
                <Code2 className="h-3.5 w-3.5 text-indigo-600" /> FastAPI + Next.js
              </span>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-foreground">
              Roadmaps
            </h4>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/roadmaps/frontend-developer" className="hover:text-primary transition-colors">
                  Frontend Developer
                </Link>
              </li>
              <li>
                <Link href="/roadmaps/data-analyst" className="hover:text-primary transition-colors">
                  Data Analyst
                </Link>
              </li>
              <li>
                <Link href="/roadmaps" className="hover:text-primary transition-colors">
                  Browse All Roadmaps
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-foreground">
              Platform
            </h4>
            <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
              <li>
                <span className="text-xs px-2 py-0.5 rounded bg-teal-500/10 text-teal-700 font-mono">
                  Phase 2: Roadmap Engine
                </span>
              </li>
              <li className="text-xs text-muted-foreground pt-1">
                Seed version: 1.0.0 (DAG Verified)
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t border-border/60 pt-6 text-center text-xs text-muted-foreground">
          &copy; {new Date().getFullYear()} CPGS DevPath. Built for modern engineers.
        </div>
      </div>
    </footer>
  );
}

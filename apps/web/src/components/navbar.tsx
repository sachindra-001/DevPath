"use client";

import Link from "next/link";
import { Compass, Sparkles, BookOpen, Layers, LogIn } from "lucide-react";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/70 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 transition-transform hover:scale-[1.02]">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-brand shadow-sm shadow-indigo-500/20 text-white">
            <Compass className="h-5 w-5 animate-pulse" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-foreground">
              DevPath <span className="text-xs font-semibold text-primary">CPGS</span>
            </span>
            <span className="text-[10px] font-medium tracking-wide text-muted-foreground uppercase">
              AI-Curated Roadmaps
            </span>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <Link
            href="/roadmaps"
            className="flex items-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-muted hover:text-foreground"
          >
            <Layers className="h-4 w-4 text-primary" />
            <span>Catalog</span>
          </Link>

          <Link
            href="/roadmaps/frontend-developer"
            className="hidden sm:flex items-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-muted hover:text-foreground"
          >
            <BookOpen className="h-4 w-4 text-teal-600" />
            <span>Frontend</span>
          </Link>

          <Link
            href="/roadmaps/data-analyst"
            className="hidden md:flex items-center gap-2 rounded-lg px-3.5 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-muted hover:text-foreground"
          >
            <Sparkles className="h-4 w-4 text-indigo-600" />
            <span>Data Analyst</span>
          </Link>
        </nav>

        {/* Action button */}
        <div className="flex items-center gap-3">
          <Link
            href="/roadmaps"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-brand px-4 py-2 text-sm font-semibold text-white shadow-md shadow-indigo-500/25 transition-all hover:opacity-95 hover:shadow-lg active:scale-[0.98]"
          >
            <span>Explore Roadmaps</span>
          </Link>
        </div>
      </div>
    </header>
  );
}

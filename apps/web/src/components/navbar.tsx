"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export function Navbar() {
  const pathname = usePathname();

  const isRoadmapsActive = pathname.startsWith("/roadmaps");

  return (
    <header className="sticky top-4 z-50 px-4 sm:px-6 lg:px-8">
      <div className="max-w-container-max mx-auto bg-paper-bg border border-ink-primary rounded-xl h-16 flex items-center justify-between px-6 shadow-editorial transition-all">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group">
          <img
            alt="DevPath Logo"
            className="h-8 w-auto object-contain transition-transform group-hover:scale-105"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuAZnA8cueS_29iU4ekKGAPOfO3fbsexi9l6Rt61Vo907MCsL4THl7CO82a6bKh7PweIm6owYFyAafXwCKC3UJ3qUqBc5Qfqfp2_nVoTge8E-MofMRLbMSG0CUp_7KtNxp8kF6yxfVwb1YaFHuuL2E5fwfD7fJsfPN8gD2sjz9am88KVbnc_bAHbOUBlPhMWbmuS1DQ8ewYWF1VpPFwnZcPVR6OBSKAVplEGaAs-S4WjsFgocnRUFNlc"
          />
          <span className="font-headline font-bold text-xl text-ink-primary hidden sm:block">
            DevPath
          </span>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-8">
          <Link
            href="/roadmaps"
            className={`font-label-mono transition-colors tracking-wider ${
              isRoadmapsActive
                ? "text-ink-primary font-bold border-b-2 border-ink-primary pb-0.5"
                : "text-on-surface-variant hover:text-ink-primary"
            }`}
          >
            Roadmaps
          </Link>
          <Link
            href="/roadmaps/frontend-developer"
            className="font-label-mono text-on-surface-variant hover:text-ink-primary transition-colors tracking-wider"
          >
            Frontend
          </Link>
          <Link
            href="/roadmaps/data-analyst"
            className="font-label-mono text-on-surface-variant hover:text-ink-primary transition-colors tracking-wider"
          >
            Data Analyst
          </Link>
        </nav>

        {/* Search & Actions */}
        <div className="flex items-center gap-4">
          <Link
            href="/roadmaps"
            className="hidden lg:flex items-center gap-2 bg-surface-container border border-ink-primary px-3 py-1.5 rounded-lg text-on-surface-variant hover:bg-highlight-yellow transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">search</span>
            <span className="font-label-mono text-[11px]">Cmd+K</span>
          </Link>

          <Link
            href="/roadmaps"
            className="font-label-mono border border-ink-primary px-4 py-1.5 rounded bg-surface-container-lowest hover:bg-highlight-yellow transition-all shadow-editorial-sm hover:-translate-y-0.5"
          >
            CATALOG
          </Link>

          <div className="w-8 h-8 rounded-full bg-ink-primary flex items-center justify-center border border-ink-primary text-white">
            <span className="material-symbols-outlined text-[18px]">person</span>
          </div>
        </div>
      </div>
    </header>
  );
}

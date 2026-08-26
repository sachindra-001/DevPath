import Link from "next/link";
import { fetchRoadmaps } from "@/lib/api";
import { RoadmapCard } from "@/components/roadmap-card";
import {
  Compass,
  Sparkles,
  ShieldCheck,
  Zap,
  ArrowRight,
  GitBranch,
  Target,
  CheckCircle2,
} from "lucide-react";

export const revalidate = 60;

export default async function HomePage() {
  const roadmaps = await fetchRoadmaps();

  return (
    <div className="flex flex-col gap-16 pb-20 sm:gap-24">
      {/* Hero Section */}
      <section className="relative overflow-hidden border-b border-border/70 bg-gradient-to-b from-white via-[#FAF8F5] to-[#FAF8F5] py-20 lg:py-28">
        {/* Subtle grid backdrop */}
        <div className="absolute inset-0 bg-[radial-gradient(#4f46e5_1px,transparent_1px)] [background-size:24px_24px] opacity-[0.04]" />

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-50/70 px-4 py-1.5 text-xs font-semibold text-indigo-800 shadow-sm">
            <Sparkles className="h-4 w-4 text-indigo-600" />
            <span>AI Resource Discovery · Human Quality Curation</span>
          </div>

          {/* Heading */}
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Learn Tech with <span className="text-gradient">Clarity</span>. <br />
            No Noise. Only Proven Paths.
          </h1>

          {/* Subtitle */}
          <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground leading-relaxed sm:text-xl">
            Structured step-by-step career roadmaps powered by an AI discovery engine. Every resource
            evaluated, scored, and verified before publish.
          </p>

          {/* Actions */}
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/roadmaps"
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-brand px-6 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:scale-[1.02] hover:shadow-xl active:scale-[0.98]"
            >
              <span>Explore Roadmaps</span>
              <ArrowRight className="h-5 w-5" />
            </Link>

            <Link
              href="/roadmaps/frontend-developer"
              className="inline-flex items-center gap-2 rounded-xl border border-border/80 bg-white px-6 py-3.5 text-base font-semibold text-foreground shadow-sm transition-all hover:bg-muted active:scale-[0.98]"
            >
              <span>View Frontend Path</span>
            </Link>
          </div>

          {/* Value props ticker */}
          <div className="mt-14 flex flex-wrap items-center justify-center gap-6 text-xs sm:text-sm font-medium text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-teal-600" />
              Topological Pre-requisites
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-indigo-600" />
              100% Free & Open Access
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              Zero Outdated Content
            </span>
          </div>
        </div>
      </section>

      {/* Value Pillars Section */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-primary">
            Engineered for Mastery
          </h2>
          <p className="mt-2 text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            Why CPGS is different
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div className="rounded-2xl border border-border/70 bg-white p-7 shadow-sm transition-all hover:shadow-md">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
              <GitBranch className="h-6 w-6" />
            </div>
            <h3 className="mt-5 text-lg font-bold text-foreground">Topological Dependency DAG</h3>
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
              No circular logic. Topics strictly declare prerequisites so you always know what
              to learn first, unlocking seamless knowledge compounding.
            </p>
          </div>

          <div className="rounded-2xl border border-border/70 bg-white p-7 shadow-sm transition-all hover:shadow-md">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-teal-50 text-teal-600">
              <Zap className="h-6 w-6" />
            </div>
            <h3 className="mt-5 text-lg font-bold text-foreground">AI Discovery Pipeline</h3>
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
              Autonomous crawlers discover tutorials, documentation, and videos across the web,
              evaluating relevance against concrete learning objectives.
            </p>
          </div>

          <div className="rounded-2xl border border-border/70 bg-white p-7 shadow-sm transition-all hover:shadow-md">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <h3 className="mt-5 text-lg font-bold text-foreground">Human-in-the-Loop Gate</h3>
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
              AI proposes; human domain experts review, score, and verify before publishing. No spam,
              no broken links, no hallucinated guides.
            </p>
          </div>
        </div>
      </section>

      {/* Featured Roadmaps Section */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <h2 className="text-xs font-semibold uppercase tracking-wider text-primary">
              Curated Career Paths
            </h2>
            <p className="mt-2 text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
              Featured Roadmaps
            </p>
          </div>
          <Link
            href="/roadmaps"
            className="flex items-center gap-1 text-sm font-semibold text-primary hover:underline"
          >
            <span>View All Roadmaps</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {roadmaps.map((rm) => (
            <RoadmapCard key={rm.id} roadmap={rm} featured={rm.slug === "frontend-developer"} />
          ))}
        </div>
      </section>
    </div>
  );
}

import Link from "next/link";
import { fetchRoadmaps } from "@/lib/api";
import { RoadmapCard } from "@/components/roadmap-card";

export const revalidate = 60;

export default async function HomePage() {
  const roadmaps = await fetchRoadmaps();

  return (
    <div className="flex flex-col w-full relative">
      {/* Decorative Grid Background */}
      <div className="absolute inset-0 pointer-events-none opacity-20 bg-notebook-grid" />

      {/* Hero Section */}
      <section className="w-full max-w-container-max mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-24 relative z-10 flex flex-col lg:flex-row items-center gap-16 border-b border-ink-primary">
        {/* Hero Text */}
        <div className="flex-1 flex flex-col items-start text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ink-primary bg-highlight-yellow mb-8 shadow-editorial-sm">
            <span className="w-2 h-2 rounded-full bg-ink-primary animate-pulse" />
            <span className="font-label-mono text-ink-primary text-xs uppercase tracking-wider">
              v2.0 Beta Live
            </span>
          </div>

          <h1 className="font-headline text-5xl sm:text-6xl font-extrabold text-ink-primary mb-6 leading-tight">
            Build your <br />
            <span className="relative inline-block">
              path.
              <span className="absolute bottom-1 left-0 w-full h-[10px] bg-secondary-fixed -z-10 transform -rotate-1" />
            </span>
          </h1>

          <p className="font-body text-lg text-on-surface-variant max-w-xl mb-10 leading-relaxed border-l-2 border-ink-primary pl-6">
            Structured developer roadmaps with resources discovered, evaluated, and curated by DevPath AI.
            Skip the noise, follow the blueprint.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <Link
              href="/roadmaps"
              className="group relative inline-flex items-center justify-center gap-2 px-8 py-4 bg-ink-primary text-white font-label-mono text-xs uppercase tracking-wider rounded border border-ink-primary overflow-hidden transition-transform hover:-translate-y-1 shadow-editorial"
            >
              <span className="relative z-10">Explore Roadmaps</span>
              <span className="material-symbols-outlined text-[18px] relative z-10 group-hover:translate-x-1 transition-transform">
                arrow_forward
              </span>
            </Link>

            <Link
              href="/roadmaps/frontend-developer"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-surface-container-lowest text-ink-primary font-label-mono text-xs uppercase tracking-wider rounded border border-ink-primary transition-all hover:bg-secondary-fixed shadow-editorial hover:-translate-y-1"
            >
              <span className="material-symbols-outlined text-[18px]">account_tree</span>
              <span>See Frontend Path</span>
            </Link>
          </div>
        </div>

        {/* Hero Visual: Technical Diagram Blueprint */}
        <div className="flex-1 w-full relative">
          <div className="absolute inset-0 bg-secondary-fixed/40 rounded-xl transform rotate-2 border border-ink-primary" />
          <div className="relative bg-paper-bg border-2 border-ink-primary rounded-xl p-8 shadow-editorial-lg flex flex-col gap-6">
            {/* Header */}
            <div className="flex justify-between items-center border-b border-ink-primary pb-4">
              <span className="font-label-mono text-xs text-ink-primary uppercase tracking-widest">
                Blueprint: Frontend DAG
              </span>
              <span className="material-symbols-outlined text-ink-primary opacity-60">
                drafts
              </span>
            </div>

            {/* Diagram Flow */}
            <div className="relative flex flex-col items-center gap-4 py-2">
              {/* Node 1 */}
              <div className="w-full flex items-center gap-4 bg-highlight-yellow border border-ink-primary rounded p-4 relative z-10 shadow-editorial-sm transition-shadow">
                <div className="w-8 h-8 rounded-full border border-ink-primary bg-white flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined text-[16px] text-ink-primary">code</span>
                </div>
                <div>
                  <h3 className="font-headline font-bold text-sm text-ink-primary">HTML Fundamentals</h3>
                  <p className="font-body text-xs text-on-surface-variant">Structure &amp; Semantics</p>
                </div>
                <span className="material-symbols-outlined text-[20px] text-emerald-600 absolute right-4 top-1/2 -translate-y-1/2">
                  check_circle
                </span>
              </div>

              {/* Connector */}
              <div className="w-[2px] h-5 bg-ink-primary" />

              {/* Node 2 */}
              <div className="w-full flex items-center gap-4 bg-white border border-ink-primary rounded p-4 relative z-10 shadow-editorial-sm transition-shadow">
                <div className="w-8 h-8 rounded-full border border-ink-primary bg-white flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined text-[16px] text-ink-primary">css</span>
                </div>
                <div>
                  <h3 className="font-headline font-bold text-sm text-ink-primary">CSS Styling</h3>
                  <p className="font-body text-xs text-on-surface-variant">Flexbox, Grid &amp; Responsive</p>
                </div>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 rounded-full border-2 border-ink-primary bg-highlight-yellow animate-pulse" />
              </div>

              {/* Connector */}
              <div className="w-[2px] h-5 bg-ink-primary" />

              {/* Node 3 */}
              <div className="w-full flex items-center gap-4 bg-surface-container-high border border-ink-primary border-dashed rounded p-4 relative z-10 opacity-75">
                <div className="w-8 h-8 rounded-full border border-ink-primary border-dashed bg-white flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined text-[16px] text-ink-primary">javascript</span>
                </div>
                <div>
                  <h3 className="font-headline font-bold text-sm text-ink-primary">JavaScript Core</h3>
                  <p className="font-body text-xs text-on-surface-variant">DOM, Async &amp; APIs</p>
                </div>
                <span className="material-symbols-outlined text-[18px] text-outline absolute right-4 top-1/2 -translate-y-1/2">
                  lock
                </span>
              </div>
            </div>

            {/* Bottom decoration dots */}
            <div className="flex justify-end gap-1.5 pt-2">
              <div className="w-2.5 h-2.5 rounded-full border border-ink-primary" />
              <div className="w-2.5 h-2.5 rounded-full border border-ink-primary bg-ink-primary" />
              <div className="w-2.5 h-2.5 rounded-full border border-ink-primary" />
            </div>
          </div>
        </div>
      </section>

      {/* Featured Blueprints Section */}
      <section className="w-full max-w-container-max mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10" id="roadmaps">
        <div className="flex flex-col md:flex-row justify-between items-end mb-12 border-b border-ink-primary pb-4">
          <div>
            <h2 className="font-headline text-3xl font-bold text-ink-primary mb-2">
              Featured Blueprints
            </h2>
            <p className="font-label-mono text-on-surface-variant uppercase tracking-widest">
              Select your discipline
            </p>
          </div>

          <Link
            href="/roadmaps"
            className="group hidden md:inline-flex items-center gap-2 font-label-mono text-ink-primary hover:text-secondary transition-colors uppercase tracking-wider"
          >
            <span>View All</span>
            <span className="material-symbols-outlined text-[16px] group-hover:translate-x-1 transition-transform">
              arrow_forward
            </span>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
          {roadmaps.map((rm) => (
            <RoadmapCard key={rm.id} roadmap={rm} featured={rm.slug === "frontend-developer"} />
          ))}
        </div>
      </section>
    </div>
  );
}

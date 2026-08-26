import { fetchRoadmaps } from "@/lib/api";
import { RoadmapCard } from "@/components/roadmap-card";

export const revalidate = 60;

export default async function CatalogPage() {
  const roadmaps = await fetchRoadmaps();

  return (
    <div className="flex flex-col w-full relative">
      <div className="absolute inset-0 pointer-events-none opacity-20 bg-notebook-grid" />

      <div className="w-full max-w-container-max mx-auto px-4 sm:px-6 lg:px-8 py-16 relative z-10">
        {/* Header */}
        <div className="mb-12 border-b-2 border-ink-primary pb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ink-primary bg-highlight-yellow mb-4 shadow-editorial-sm">
            <span className="w-2 h-2 rounded-full bg-ink-primary" />
            <span className="font-label-mono text-xs text-ink-primary uppercase tracking-wider">
              Catalog
            </span>
          </div>

          <h1 className="font-headline text-4xl font-extrabold text-ink-primary mb-3">
            Developer Roadmaps &amp; Blueprints
          </h1>

          <p className="font-body text-base text-on-surface-variant max-w-2xl">
            Choose your learning path. Every roadmap follows strict prerequisite DAG rules with
            resources curated and verified for accuracy.
          </p>
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
          {roadmaps.map((rm) => (
            <RoadmapCard key={rm.id} roadmap={rm} />
          ))}
        </div>
      </div>
    </div>
  );
}

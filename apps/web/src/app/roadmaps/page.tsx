import { fetchRoadmaps } from "@/lib/api";
import { RoadmapCard } from "@/components/roadmap-card";
import { Layers, Search, Sparkles } from "lucide-react";

export const revalidate = 60;

export default async function CatalogPage() {
  const roadmaps = await fetchRoadmaps();

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Catalog Header */}
      <div className="flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-teal-500/20 bg-teal-50/70 px-3.5 py-1 text-xs font-semibold text-teal-800">
          <Layers className="h-3.5 w-3.5 text-teal-600" />
          <span>Curated Learning Catalog</span>
        </div>
        <h1 className="mt-4 text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
          Explore Developer Roadmaps
        </h1>
        <p className="mt-3 max-w-2xl text-base text-muted-foreground">
          Step-by-step career blueprints. Choose your focus area, learn fundamentals first, and
          master modern engineering workflows with zero guesswork.
        </p>
      </div>

      {/* Grid of Roadmaps */}
      <div className="mt-12">
        <div className="flex items-center justify-between border-b border-border/70 pb-4">
          <span className="text-sm font-semibold text-foreground">
            Available Roadmaps ({roadmaps.length})
          </span>
          <span className="text-xs font-mono text-muted-foreground">
            Seed-Verified v1.0.0
          </span>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {roadmaps.map((rm) => (
            <RoadmapCard key={rm.id} roadmap={rm} />
          ))}
        </div>
      </div>
    </div>
  );
}

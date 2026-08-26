import Link from "next/link";
import { RoadmapSummary } from "@/types/api";
import { ArrowRight, Clock, BookOpen, Layers, CheckCircle2 } from "lucide-react";

interface RoadmapCardProps {
  roadmap: RoadmapSummary;
  featured?: boolean;
}

export function RoadmapCard({ roadmap, featured = false }: RoadmapCardProps) {
  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case "beginner":
        return "bg-emerald-500/10 text-emerald-700 border-emerald-500/20";
      case "intermediate":
        return "bg-indigo-500/10 text-indigo-700 border-indigo-500/20";
      case "advanced":
        return "bg-purple-500/10 text-purple-700 border-purple-500/20";
      default:
        return "bg-gray-500/10 text-gray-700 border-gray-500/20";
    }
  };

  return (
    <div
      className={`group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-border/80 bg-white p-6 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:shadow-xl ${
        featured ? "ring-1 ring-primary/20 bg-gradient-subtle" : ""
      }`}
    >
      <div>
        {/* Top Badges */}
        <div className="flex items-center justify-between gap-2">
          <span
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wider capitalize ${getDifficultyBadge(
              roadmap.difficulty
            )}`}
          >
            {roadmap.difficulty}
          </span>
          <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
            <CheckCircle2 className="h-3.5 w-3.5 text-teal-600" />
            Verified Seed
          </span>
        </div>

        {/* Title */}
        <h3 className="mt-4 text-xl font-bold tracking-tight text-foreground transition-colors group-hover:text-primary">
          {roadmap.title}
        </h3>

        {/* Description */}
        <p className="mt-2 text-sm text-muted-foreground line-clamp-3 leading-relaxed">
          {roadmap.description || "Master essential technical concepts step by step."}
        </p>
      </div>

      {/* Footer Info & Action */}
      <div className="mt-6 border-t border-border/60 pt-4">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span className="flex items-center gap-1.5 font-medium">
            <Layers className="h-4 w-4 text-primary" />
            Structured DAG
          </span>
          <span className="flex items-center gap-1.5 font-medium">
            <Clock className="h-4 w-4 text-teal-600" />
            Flexible Pace
          </span>
        </div>

        <Link
          href={`/roadmaps/${roadmap.slug}`}
          className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-muted py-2.5 text-sm font-semibold text-foreground transition-all duration-200 group-hover:bg-gradient-brand group-hover:text-white group-hover:shadow-md group-hover:shadow-indigo-500/20"
        >
          <span>View Roadmap</span>
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
        </Link>
      </div>
    </div>
  );
}

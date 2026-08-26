"use client";

import { useState } from "react";
import Link from "next/link";
import { TopicSummary } from "@/types/api";
import { Clock, ChevronRight, CheckCircle, Circle, Link as LinkIcon, Sparkles } from "lucide-react";

interface TopicCardProps {
  topic: TopicSummary;
  roadmapSlug: string;
  index: number;
}

export function TopicCard({ topic, roadmapSlug, index }: TopicCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  const getDifficultyColor = (diff: string) => {
    switch (diff) {
      case "beginner":
        return "text-emerald-700 bg-emerald-50 border-emerald-200";
      case "intermediate":
        return "text-indigo-700 bg-indigo-50 border-indigo-200";
      case "advanced":
        return "text-purple-700 bg-purple-50 border-purple-200";
      default:
        return "text-slate-700 bg-slate-50 border-slate-200";
    }
  };

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="group relative flex flex-col rounded-xl border border-border/70 bg-white p-4.5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-primary/50 hover:shadow-md"
    >
      <div className="flex items-start justify-between gap-3">
        {/* Left Indicator & Topic Title */}
        <div className="flex items-start gap-3">
          <div className="mt-0.5 flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 font-semibold text-xs">
            {index + 1}
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <Link
                href={`/roadmaps/${roadmapSlug}/${topic.slug}`}
                className="font-bold text-foreground transition-colors hover:text-primary"
              >
                {topic.title}
              </Link>

              {/* Difficulty badge */}
              <span
                className={`rounded-md border px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wider capitalize ${getDifficultyColor(
                  topic.difficulty
                )}`}
              >
                {topic.difficulty}
              </span>
            </div>

            {/* Prerequisites tags */}
            {topic.depends_on && topic.depends_on.length > 0 && (
              <div className="mt-2 flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
                <span className="flex items-center gap-1 font-medium text-slate-500">
                  <LinkIcon className="h-3 w-3" /> Requires:
                </span>
                {topic.depends_on.map((dep) => (
                  <Link
                    key={dep}
                    href={`/roadmaps/${roadmapSlug}/${dep}`}
                    className="inline-flex items-center rounded-md bg-muted px-2 py-0.5 font-mono text-[11px] text-foreground hover:bg-primary/10 hover:text-primary transition-colors"
                  >
                    {dep}
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Info: Est Hours & Action */}
        <div className="flex flex-col items-end gap-2 flex-shrink-0">
          <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
            <Clock className="h-3.5 w-3.5 text-teal-600" />
            {topic.estimated_hours || 4} hrs
          </span>

          <Link
            href={`/roadmaps/${roadmapSlug}/${topic.slug}`}
            className="flex items-center gap-1 text-xs font-semibold text-primary transition-all group-hover:translate-x-0.5"
          >
            <span>Learn</span>
            <ChevronRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}

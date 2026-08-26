import Link from "next/link";
import { TopicSummary } from "@/types/api";

interface TopicCardProps {
  topic: TopicSummary;
  roadmapSlug: string;
  index: number;
}

export function TopicCard({ topic, roadmapSlug, index }: TopicCardProps) {
  const isFirst = index === 0;

  return (
    <div
      className={`group flex flex-col md:flex-row items-start md:items-center gap-4 border border-ink-primary p-4.5 rounded-lg relative transition-all duration-200 hover:shadow-editorial hover:-translate-y-0.5 ${
        isFirst
          ? "bg-surface-container-lowest border-2 shadow-editorial"
          : "bg-paper-bg"
      }`}
    >
      {/* Icon Indicator */}
      <div
        className={`flex items-center justify-center w-8 h-8 rounded-full border border-ink-primary text-ink-primary flex-shrink-0 font-label-mono text-xs ${
          isFirst ? "bg-highlight-yellow animate-pulse" : "bg-surface-container"
        }`}
      >
        {isFirst ? (
          <span className="material-symbols-outlined text-[18px]">play_arrow</span>
        ) : (
          <span>{index + 1}</span>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <div className="flex flex-wrap items-center gap-2">
          <Link
            href={`/roadmaps/${roadmapSlug}/${topic.slug}`}
            className="font-headline font-bold text-base text-ink-primary hover:text-secondary transition-colors"
          >
            {topic.title}
          </Link>
          <span className="font-label-mono text-[10px] bg-accent-lavender border border-ink-primary px-2 py-0.5 rounded capitalize">
            {topic.difficulty}
          </span>
        </div>

        {/* Prerequisites */}
        {topic.depends_on && topic.depends_on.length > 0 && (
          <div className="mt-1.5 flex flex-wrap items-center gap-1.5 font-label-mono text-[11px] text-on-surface-variant">
            <span>Requires:</span>
            {topic.depends_on.map((dep) => (
              <Link
                key={dep}
                href={`/roadmaps/${roadmapSlug}/${dep}`}
                className="bg-surface-container border border-ink-primary/40 px-1.5 py-0.2 rounded hover:bg-highlight-yellow text-ink-primary transition-colors"
              >
                {dep}
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end pt-2 md:pt-0 border-t md:border-t-0 border-ink-primary/20">
        <span className="font-label-mono text-xs text-on-surface-variant">
          ~{topic.estimated_hours || 4}h
        </span>

        <Link
          href={`/roadmaps/${roadmapSlug}/${topic.slug}`}
          className="font-label-mono text-xs bg-ink-primary text-white px-3.5 py-1.5 rounded border border-ink-primary hover:bg-on-surface-variant transition-colors flex items-center gap-1 shadow-editorial-sm"
        >
          <span>Learn</span>
          <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
        </Link>
      </div>
    </div>
  );
}

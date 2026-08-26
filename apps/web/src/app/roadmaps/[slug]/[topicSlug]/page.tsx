import { notFound } from "next/navigation";
import Link from "next/link";
import { fetchTopicBySlug, fetchRoadmapBySlug } from "@/lib/api";
import {
  ArrowLeft,
  Clock,
  CheckCircle2,
  ListChecks,
  Link as LinkIcon,
  ExternalLink,
  BookOpen,
  Sparkles,
  ChevronRight,
  Video,
  FileText,
} from "lucide-react";

export const revalidate = 60;

interface PageProps {
  params: Promise<{ slug: string; topicSlug: string }>;
}

export default async function TopicDetailPage({ params }: PageProps) {
  const { slug, topicSlug } = await params;

  const [roadmap, topic] = await Promise.all([
    fetchRoadmapBySlug(slug),
    fetchTopicBySlug(slug, topicSlug),
  ]);

  if (!topic) {
    notFound();
  }

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
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Breadcrumbs */}
      <nav className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
        <Link href="/roadmaps" className="hover:text-foreground transition-colors">
          Roadmaps
        </Link>
        <ChevronRight className="h-3 w-3" />
        <Link
          href={`/roadmaps/${slug}`}
          className="hover:text-foreground transition-colors font-medium"
        >
          {roadmap?.title || slug}
        </Link>
        <ChevronRight className="h-3 w-3" />
        <span className="text-foreground font-semibold">{topic.title}</span>
      </nav>

      {/* Main Topic Header */}
      <div className="mt-6 rounded-3xl border border-border/80 bg-white p-6 shadow-sm sm:p-10">
        <div className="flex flex-wrap items-center gap-3">
          <span
            className={`rounded-full border px-3 py-1 text-xs font-bold uppercase tracking-wider capitalize ${getDifficultyColor(
              topic.difficulty
            )}`}
          >
            {topic.difficulty}
          </span>
          <span className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
            <Clock className="h-3.5 w-3.5 text-teal-600" />
            Estimated: ~{topic.estimated_hours || 4} hours
          </span>
        </div>

        <h1 className="mt-4 text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
          {topic.title}
        </h1>

        <p className="mt-3 text-base text-muted-foreground leading-relaxed">
          {topic.description ||
            `Comprehensive module covering ${topic.title} principles, syntax, and real-world patterns.`}
        </p>

        {/* Action button back to roadmap */}
        <div className="mt-6 border-t border-border/60 pt-4">
          <Link
            href={`/roadmaps/${slug}`}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary hover:underline"
          >
            <ArrowLeft className="h-3.5 w-3.5" />
            <span>Return to full {roadmap?.title || "Roadmap"} outline</span>
          </Link>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-8 md:grid-cols-3">
        {/* Left Column: Learning Objectives & Prerequisites (2 cols) */}
        <div className="space-y-8 md:col-span-2">
          {/* Learning Objectives Checklist */}
          <section className="rounded-2xl border border-border/70 bg-white p-6 shadow-sm">
            <h2 className="flex items-center gap-2 text-lg font-bold text-foreground">
              <ListChecks className="h-5 w-5 text-indigo-600" />
              Learning Objectives
            </h2>
            <p className="mt-1 text-xs text-muted-foreground">
              By the end of this module, you should be able to:
            </p>

            <ul className="mt-5 space-y-3">
              {topic.learning_objectives && topic.learning_objectives.length > 0 ? (
                topic.learning_objectives.map((obj, i) => (
                  <li key={i} className="flex items-start gap-3 text-sm text-foreground/90">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-teal-600" />
                    <span>{obj}</span>
                  </li>
                ))
              ) : (
                <li className="text-sm text-muted-foreground italic">
                  No specific learning objectives listed for this topic yet.
                </li>
              )}
            </ul>
          </section>

          {/* Curated Resources */}
          <section className="rounded-2xl border border-border/70 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="flex items-center gap-2 text-lg font-bold text-foreground">
                <BookOpen className="h-5 w-5 text-teal-600" />
                Curated Resources
              </h2>
              <span className="text-xs font-mono text-muted-foreground">
                {topic.resources.length} verified
              </span>
            </div>

            <div className="mt-5 space-y-3.5">
              {topic.resources && topic.resources.length > 0 ? (
                topic.resources.map((res) => (
                  <a
                    key={res.id}
                    href={res.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex flex-col justify-between rounded-xl border border-border/70 bg-muted/40 p-4 transition-all hover:border-primary/40 hover:bg-white hover:shadow-sm"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2">
                        {res.resource_type === "video" ? (
                          <Video className="h-4 w-4 text-rose-600" />
                        ) : (
                          <FileText className="h-4 w-4 text-indigo-600" />
                        )}
                        <span className="font-bold text-sm text-foreground group-hover:text-primary transition-colors">
                          {res.title}
                        </span>
                      </div>
                      <ExternalLink className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors flex-shrink-0" />
                    </div>

                    {res.summary && (
                      <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                        {res.summary}
                      </p>
                    )}

                    <div className="mt-3 flex items-center gap-3 text-[11px] text-muted-foreground">
                      <span className="font-mono text-foreground/80">{res.source_domain}</span>
                      <span className="capitalize">{res.access_type}</span>
                      {res.is_recommended && (
                        <span className="inline-flex items-center gap-0.5 font-semibold text-teal-700 bg-teal-50 px-1.5 py-0.5 rounded">
                          <Sparkles className="h-3 w-3" /> Recommended
                        </span>
                      )}
                    </div>
                  </a>
                ))
              ) : (
                <div className="rounded-xl border border-dashed border-border/80 bg-muted/20 p-6 text-center">
                  <Sparkles className="mx-auto h-6 w-6 text-muted-foreground/60" />
                  <p className="mt-2 text-sm font-semibold text-foreground">
                    No resources attached yet
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground max-w-sm mx-auto">
                    The autonomous AI discovery pipeline will crawl and score web resources for this
                    topic in upcoming phases.
                  </p>
                </div>
              )}
            </div>
          </section>
        </div>

        {/* Right Column: Prerequisites & Context (1 col) */}
        <div className="space-y-6">
          <div className="rounded-2xl border border-border/70 bg-white p-6 shadow-sm">
            <h3 className="flex items-center gap-2 text-sm font-bold uppercase tracking-wider text-foreground">
              <LinkIcon className="h-4 w-4 text-primary" />
              Prerequisites
            </h3>

            <div className="mt-4 space-y-2">
              {topic.prerequisites && topic.prerequisites.length > 0 ? (
                topic.prerequisites.map((prereq) => (
                  <Link
                    key={prereq}
                    href={`/roadmaps/${slug}/${prereq}`}
                    className="flex items-center justify-between rounded-xl border border-border/70 bg-muted/30 p-3 text-xs font-semibold text-foreground transition-all hover:bg-muted hover:text-primary"
                  >
                    <span>{prereq}</span>
                    <ChevronRight className="h-3.5 w-3.5" />
                  </Link>
                ))
              ) : (
                <p className="text-xs text-muted-foreground italic">
                  None. This is an introductory starting topic.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

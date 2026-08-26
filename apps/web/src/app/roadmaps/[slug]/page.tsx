import { notFound } from "next/navigation";
import Link from "next/link";
import { fetchRoadmapBySlug } from "@/lib/api";
import { TopicCard } from "@/components/topic-card";
import {
  Clock,
  Layers,
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  ListTree,
  ChevronRight,
} from "lucide-react";

export const revalidate = 60;

interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function RoadmapDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const roadmap = await fetchRoadmapBySlug(slug);

  if (!roadmap) {
    notFound();
  }

  // Calculate totals
  const totalTopics = roadmap.sections.reduce(
    (acc, sec) => acc + sec.topics.length,
    0
  );
  const totalHours = roadmap.sections.reduce(
    (acc, sec) =>
      acc +
      sec.topics.reduce((tAcc, top) => tAcc + (top.estimated_hours || 4), 0),
    0
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Back Link & Breadcrumbs */}
      <nav className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
        <Link href="/roadmaps" className="flex items-center gap-1 hover:text-foreground transition-colors">
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>All Roadmaps</span>
        </Link>
        <ChevronRight className="h-3.5 w-3.5" />
        <span className="text-foreground font-semibold">{roadmap.title}</span>
      </nav>

      {/* Hero Header */}
      <div className="mt-6 rounded-3xl border border-border/80 bg-white p-6 shadow-sm sm:p-10">
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex items-center rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-indigo-700 capitalize">
            {roadmap.difficulty}
          </span>
          <span className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground">
            <CheckCircle2 className="h-4 w-4 text-teal-600" />
            Verified Seed v{roadmap.seed_version}
          </span>
        </div>

        <h1 className="mt-4 text-3xl font-extrabold tracking-tight text-foreground sm:text-4xl">
          {roadmap.title} Roadmap
        </h1>

        <p className="mt-3 max-w-3xl text-base text-muted-foreground leading-relaxed">
          {roadmap.description || "Follow this structured step-by-step path to master all key competencies."}
        </p>

        {/* Roadmap Stats Bar */}
        <div className="mt-8 flex flex-wrap items-center gap-6 border-t border-border/60 pt-6 text-sm">
          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-primary" />
            <span className="font-semibold text-foreground">{roadmap.sections.length}</span>
            <span className="text-muted-foreground">Sections</span>
          </div>

          <div className="flex items-center gap-2">
            <ListTree className="h-4 w-4 text-teal-600" />
            <span className="font-semibold text-foreground">{totalTopics}</span>
            <span className="text-muted-foreground">Topics</span>
          </div>

          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4 text-indigo-600" />
            <span className="font-semibold text-foreground">~{totalHours} hrs</span>
            <span className="text-muted-foreground">Estimated Total</span>
          </div>
        </div>
      </div>

      {/* Main Roadmap Outline & Sidebar Layout */}
      <div className="mt-10 grid grid-cols-1 gap-10 lg:grid-cols-4">
        {/* Sticky Table of Contents on Large Screens */}
        <aside className="hidden lg:block lg:col-span-1">
          <div className="sticky top-24 rounded-2xl border border-border/80 bg-white p-5 shadow-sm">
            <h3 className="text-xs font-bold uppercase tracking-wider text-foreground flex items-center gap-1.5">
              <BookOpen className="h-4 w-4 text-primary" />
              Table of Contents
            </h3>
            <ul className="mt-4 space-y-2 text-sm">
              {roadmap.sections.map((sec, idx) => (
                <li key={sec.id}>
                  <a
                    href={`#section-${sec.id}`}
                    className="flex items-center gap-2 rounded-lg px-2.5 py-1.5 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                  >
                    <span className="flex h-5 w-5 items-center justify-center rounded-md bg-indigo-50 font-mono text-[11px] font-bold text-indigo-700">
                      {idx + 1}
                    </span>
                    <span className="truncate">{sec.title}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </aside>

        {/* Vertical Section Outline */}
        <div className="space-y-12 lg:col-span-3">
          {roadmap.sections.map((section, secIdx) => (
            <section
              key={section.id}
              id={`section-${section.id}`}
              className="scroll-mt-24 rounded-3xl border border-border/70 bg-white p-6 shadow-sm sm:p-8"
            >
              {/* Section Header */}
              <div className="flex items-start justify-between gap-4 border-b border-border/60 pb-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-brand text-white font-bold text-sm shadow-sm">
                    {secIdx + 1}
                  </div>
                  <div>
                    <h2 className="text-xl font-bold tracking-tight text-foreground">
                      {section.title}
                    </h2>
                    <span className="text-xs text-muted-foreground">
                      {section.topics.length} topic{section.topics.length === 1 ? "" : "s"}
                    </span>
                  </div>
                </div>
              </div>

              {/* Topics List */}
              <div className="mt-6 space-y-3.5">
                {section.topics.map((topic, topicIdx) => (
                  <TopicCard
                    key={topic.id}
                    topic={topic}
                    roadmapSlug={roadmap.slug}
                    index={topicIdx}
                  />
                ))}
              </div>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
}

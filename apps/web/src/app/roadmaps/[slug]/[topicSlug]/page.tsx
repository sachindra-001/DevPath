import { notFound } from "next/navigation";
import Link from "next/link";
import { fetchTopicBySlug, fetchRoadmapBySlug } from "@/lib/api";

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

  return (
    <div className="flex flex-col w-full relative">
      <div className="absolute inset-0 pointer-events-none opacity-20 bg-notebook-grid" />

      <div className="max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12 relative z-10">
        {/* Breadcrumbs */}
        <nav className="flex items-center gap-2 mb-6 font-label-mono text-on-surface-variant uppercase tracking-wider text-xs">
          <Link href="/roadmaps" className="hover:text-ink-primary transition-colors">
            Roadmaps
          </Link>
          <span className="material-symbols-outlined text-[16px]">chevron_right</span>
          <Link
            href={`/roadmaps/${slug}`}
            className="hover:text-ink-primary transition-colors font-bold text-ink-primary"
          >
            {roadmap?.title || slug}
          </Link>
          <span className="material-symbols-outlined text-[16px]">chevron_right</span>
          <span>{topic.title}</span>
        </nav>

        {/* Header Section */}
        <div className="bg-paper-bg border-2 border-ink-primary rounded-xl p-8 shadow-editorial-lg mb-10">
          <div className="flex flex-wrap gap-2.5 mb-4">
            <span className="font-label-mono text-xs bg-highlight-yellow border border-ink-primary px-2.5 py-1 rounded text-ink-primary font-bold shadow-editorial-sm">
              {topic.difficulty}
            </span>
            <span className="font-label-mono text-xs bg-surface-container border border-ink-primary px-2.5 py-1 rounded text-on-surface flex items-center gap-1">
              <span className="material-symbols-outlined text-[16px]">schedule</span>
              ~{topic.estimated_hours || 4} hours
            </span>
          </div>

          <h1 className="font-headline text-3xl sm:text-4xl font-extrabold text-ink-primary mb-3">
            {topic.title}
          </h1>

          <p className="font-body text-base text-on-surface-variant leading-relaxed">
            {topic.description ||
              `In-depth learning module covering ${topic.title} concepts, syntax, and hands-on patterns.`}
          </p>
        </div>

        {/* Learning Objectives & Resources */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Main Column */}
          <div className="md:col-span-2 space-y-8">
            {/* Objectives */}
            <section className="bg-surface-container-lowest border border-ink-primary rounded-xl p-6 shadow-editorial">
              <h2 className="font-headline font-bold text-lg text-ink-primary mb-4 flex items-center gap-2 border-b border-ink-primary pb-3">
                <span className="material-symbols-outlined text-teal-600">checklist</span>
                Learning Objectives
              </h2>

              <ul className="space-y-3">
                {topic.learning_objectives && topic.learning_objectives.length > 0 ? (
                  topic.learning_objectives.map((obj, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-sm text-ink-primary font-body">
                      <span className="material-symbols-outlined text-emerald-600 text-[18px] mt-0.5 flex-shrink-0">
                        check_circle
                      </span>
                      <span>{obj}</span>
                    </li>
                  ))
                ) : (
                  <li className="text-sm text-on-surface-variant italic">
                    Objectives will be populated automatically by the AI pipeline.
                  </li>
                )}
              </ul>
            </section>

            {/* Curated Resources */}
            <section className="bg-surface-container-lowest border border-ink-primary rounded-xl p-6 shadow-editorial">
              <h2 className="font-headline font-bold text-lg text-ink-primary mb-4 flex items-center justify-between border-b border-ink-primary pb-3">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-indigo-600">menu_book</span>
                  <span>Curated Resources</span>
                </div>
                <span className="font-label-mono text-xs text-on-surface-variant">
                  {topic.resources.length} verified
                </span>
              </h2>

              <div className="space-y-3.5">
                {topic.resources && topic.resources.length > 0 ? (
                  topic.resources.map((res) => (
                    <a
                      key={res.id}
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group flex flex-col justify-between rounded-lg border border-ink-primary bg-paper-bg p-4 transition-all hover:bg-highlight-yellow/20 hover:shadow-editorial-sm"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="material-symbols-outlined text-[18px] text-ink-primary">
                            {res.resource_type === "video" ? "movie" : "article"}
                          </span>
                          <span className="font-headline font-bold text-sm text-ink-primary group-hover:text-secondary transition-colors">
                            {res.title}
                          </span>
                        </div>
                        <span className="material-symbols-outlined text-[16px] text-on-surface-variant group-hover:translate-x-0.5 transition-transform flex-shrink-0">
                          open_in_new
                        </span>
                      </div>

                      {res.summary && (
                        <p className="font-body text-xs text-on-surface-variant mt-2 line-clamp-2">
                          {res.summary}
                        </p>
                      )}

                      <div className="mt-3 flex items-center gap-3 font-label-mono text-[10px] text-on-surface-variant border-t border-ink-primary/20 pt-2">
                        <span>{res.source_domain}</span>
                        <span className="capitalize">{res.access_type}</span>
                        {res.is_recommended && (
                          <span className="bg-accent-lavender text-ink-primary px-1.5 py-0.5 rounded border border-ink-primary">
                            RECOMMENDED
                          </span>
                        )}
                      </div>
                    </a>
                  ))
                ) : (
                  <div className="border border-dashed border-ink-primary/60 rounded-lg p-6 text-center bg-surface-container">
                    <span className="material-symbols-outlined text-on-surface-variant text-3xl mb-2">
                      travel_explore
                    </span>
                    <p className="font-headline font-bold text-sm text-ink-primary">
                      No resources published yet
                    </p>
                    <p className="font-body text-xs text-on-surface-variant max-w-xs mx-auto mt-1">
                      The autonomous AI pipeline will crawl and index verified resources in Phase 5.
                    </p>
                  </div>
                )}
              </div>
            </section>
          </div>

          {/* Sidebar Column: Prerequisites & Nav */}
          <div className="space-y-6">
            <div className="bg-surface-container-lowest border border-ink-primary rounded-xl p-5 shadow-editorial">
              <h3 className="font-label-mono text-xs text-ink-primary uppercase tracking-wider mb-3 flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[16px]">account_tree</span>
                Prerequisites
              </h3>

              <div className="space-y-2">
                {topic.prerequisites && topic.prerequisites.length > 0 ? (
                  topic.prerequisites.map((prereq) => (
                    <Link
                      key={prereq}
                      href={`/roadmaps/${slug}/${prereq}`}
                      className="flex items-center justify-between bg-paper-bg border border-ink-primary px-3 py-2 rounded text-xs font-headline font-bold text-ink-primary hover:bg-highlight-yellow transition-all"
                    >
                      <span>{prereq}</span>
                      <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
                    </Link>
                  ))
                ) : (
                  <p className="font-body text-xs text-on-surface-variant italic">
                    None. This is an introductory starting module.
                  </p>
                )}
              </div>
            </div>

            <Link
              href={`/roadmaps/${slug}`}
              className="flex items-center justify-center gap-2 font-label-mono text-xs bg-paper-bg border border-ink-primary p-3 rounded text-ink-primary hover:bg-highlight-yellow transition-colors shadow-editorial-sm"
            >
              <span className="material-symbols-outlined text-[16px]">arrow_back</span>
              <span>Back to {roadmap?.title || "Roadmap"} Outline</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

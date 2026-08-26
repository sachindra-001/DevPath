import { notFound } from "next/navigation";
import Link from "next/link";
import { fetchRoadmapBySlug } from "@/lib/api";
import { TopicCard } from "@/components/topic-card";

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
    <div className="flex flex-col w-full relative">
      {/* Grid Background Overlay for Notebook Feel */}
      <div className="absolute inset-0 pointer-events-none opacity-20 bg-notebook-grid" />

      <div className="max-w-container-max mx-auto w-full px-4 sm:px-6 lg:px-8 py-12 relative z-10">
        {/* Header Section */}
        <div className="mb-12">
          <nav className="flex items-center gap-2 mb-6 font-label-mono text-on-surface-variant uppercase tracking-wider text-xs">
            <Link href="/roadmaps" className="hover:text-ink-primary transition-colors">
              Roadmaps
            </Link>
            <span className="material-symbols-outlined text-[16px]">chevron_right</span>
            <span className="text-ink-primary font-bold">{roadmap.title}</span>
          </nav>

          <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-8 border-b-2 border-ink-primary pb-8">
            <div className="max-w-3xl">
              <h1 className="font-headline text-4xl sm:text-5xl font-extrabold text-ink-primary mb-4">
                {roadmap.title}
              </h1>
              <p className="font-body text-base sm:text-lg text-on-surface-variant max-w-2xl leading-relaxed">
                {roadmap.description ||
                  "Step-by-step developer blueprint with curated resources and prerequisite DAG structure."}
              </p>
            </div>

            <div className="flex flex-wrap gap-3 font-label-mono text-xs">
              <div className="flex items-center gap-2 border border-ink-primary bg-surface-container px-3 py-1.5 rounded text-on-surface">
                <span className="material-symbols-outlined text-[18px]">signal_cellular_alt</span>
                <span className="uppercase">{roadmap.difficulty}</span>
              </div>
              <div className="flex items-center gap-2 border border-ink-primary bg-surface-container px-3 py-1.5 rounded text-on-surface">
                <span className="material-symbols-outlined text-[18px]">schedule</span>
                <span>~{totalHours} HOURS</span>
              </div>
              <div className="flex items-center gap-2 border border-ink-primary bg-highlight-yellow px-3 py-1.5 rounded text-ink-primary font-bold shadow-editorial-sm">
                <span className="material-symbols-outlined text-[18px]">menu_book</span>
                <span>{totalTopics} TOPICS</span>
              </div>
            </div>
          </div>
        </div>

        {/* Main Layout: Sticky Sidebar + Roadmap Path */}
        <div className="flex flex-col lg:flex-row gap-12 relative">
          {/* Sticky Navigation Sidebar */}
          <aside className="hidden lg:block w-64 flex-shrink-0">
            <div className="sticky top-28 flex flex-col gap-4 border border-ink-primary bg-paper-bg p-6 rounded-xl shadow-editorial">
              <h3 className="font-label-mono text-xs text-on-surface-variant uppercase mb-2">
                Sections
              </h3>
              <nav className="flex flex-col gap-3 font-body text-sm">
                {roadmap.sections.map((sec, idx) => (
                  <a
                    key={sec.id}
                    href={`#section-${sec.id}`}
                    className="flex items-center justify-between font-medium text-on-surface-variant hover:text-ink-primary transition-colors group"
                  >
                    <span>
                      0{idx + 1}. {sec.title}
                    </span>
                    <span className="w-2 h-2 rounded-full bg-highlight-yellow border border-ink-primary opacity-0 group-hover:opacity-100 transition-opacity" />
                  </a>
                ))}
              </nav>

              <div className="mt-6 pt-6 border-t border-ink-primary">
                <h3 className="font-label-mono text-xs text-on-surface-variant uppercase mb-3">
                  Your Progress
                </h3>
                <div className="h-2 w-full bg-surface-container border border-ink-primary rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 w-[0%] border-r border-ink-primary" />
                </div>
                <div className="flex justify-between mt-2 font-label-mono text-[11px] text-on-surface-variant">
                  <span>0 / {totalTopics} Completed</span>
                  <span>0%</span>
                </div>
              </div>
            </div>
          </aside>

          {/* Roadmap Sections */}
          <div className="flex-1 max-w-4xl pb-24 space-y-16">
            {roadmap.sections.map((section, secIdx) => (
              <section key={section.id} id={`section-${section.id}`} className="scroll-mt-28 relative">
                {/* Section Header */}
                <div className="flex items-baseline gap-4 mb-6">
                  <span className="font-headline text-3xl font-extrabold text-ink-primary/20 hidden lg:block">
                    0{secIdx + 1}
                  </span>
                  <h2 className="font-headline font-bold text-2xl text-ink-primary bg-surface-container-lowest inline-block px-4 py-2 border border-ink-primary shadow-editorial-sm">
                    {section.title}
                  </h2>
                </div>

                {/* Section Topics */}
                <div className="flex flex-col gap-4 pl-0 lg:pl-8">
                  {section.topics.map((topic, topicIdx) => (
                    <div key={topic.id} className="flex flex-col">
                      <TopicCard
                        topic={topic}
                        roadmapSlug={roadmap.slug}
                        index={topicIdx}
                      />
                      {topicIdx < section.topics.length - 1 && (
                        <div className="w-[2px] h-4 bg-ink-primary ml-6 my-1" />
                      )}
                    </div>
                  ))}
                </div>
              </section>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

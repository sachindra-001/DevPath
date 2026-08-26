import Link from "next/link";
import { RoadmapSummary } from "@/types/api";

interface RoadmapCardProps {
  roadmap: RoadmapSummary;
  featured?: boolean;
}

export function RoadmapCard({ roadmap }: RoadmapCardProps) {
  const isFrontend = roadmap.slug === "frontend-developer";
  const bgImg = isFrontend
    ? "https://lh3.googleusercontent.com/aida-public/AB6AXuBiplp18IlJakOMj7b4MAcPhq95xww1gdw0iLaVoa3cbu3JMTyRsfCdGGjIHcSC5oKhemgcGj4Ak-wFDep-E1Kig2Urzs2ir7nRhghFoPCXAru7SWXTGf5aTxKezHokyyIPi6oBf3Yy28XvwXgpHV34tuMXSnfdjhvH6Z2NgRPld2NzgzwlqcuLYIr26PhoMaTC79NtxrQY1rGgxquO8UtIIOaRDzmFWpKjgkoURLi1uJagyd7QFo38"
    : "https://lh3.googleusercontent.com/aida-public/AB6AXuBUZ90kf4-7Jauzcvm1obu3qrhQfYA_yP44vtPzZuzRYrXZZ-2hehBhW39L4CB8c82ZBH0hhly2TyR5Ew4eD-D4gQHLy6pmfQ8eQOvtBTj5qvWZ-75Cu2xVSR2x8MsmUldHPmjYNMKerLtkaTwKtdGlB_GiK2ABTNA_x7JrGOo_Ue48FjxmZJ15LoqBpATGCDyu-PP1PDmMqKMH7xymMvt1AmYjgV1YQZCga83iuNnLA0IDpVAGmIEx";

  return (
    <Link
      href={`/roadmaps/${roadmap.slug}`}
      className="group flex flex-col bg-surface-container-lowest border border-ink-primary rounded-xl overflow-hidden hover:shadow-editorial-lg hover:-translate-y-1 transition-all duration-300 shadow-editorial"
    >
      {/* Header Image with Technical Illustration */}
      <div className="h-48 border-b border-ink-primary relative overflow-hidden bg-secondary-fixed-dim">
        <div
          className="absolute inset-0 bg-cover bg-center mix-blend-multiply opacity-80 transition-transform duration-500 group-hover:scale-105"
          style={{ backgroundImage: `url('${bgImg}')` }}
        />
        <div className="absolute top-4 left-4 bg-paper-bg border border-ink-primary px-2.5 py-1 rounded font-label-mono text-[10px] text-ink-primary uppercase tracking-widest">
          Seed v{roadmap.seed_version} · {roadmap.difficulty}
        </div>
      </div>

      {/* Card Content */}
      <div className="p-6 flex flex-col flex-1">
        <div className="flex items-center gap-2 mb-3">
          <span className="w-3 h-3 rounded-full bg-highlight-yellow border border-ink-primary" />
          <span className="font-label-mono text-on-surface-variant uppercase tracking-wider">
            {isFrontend ? "Web Dev" : "Data & Analytics"}
          </span>
        </div>

        <h3 className="font-headline font-bold text-xl text-ink-primary mb-2 group-hover:text-secondary transition-colors">
          {roadmap.title}
        </h3>

        <p className="font-body text-sm text-on-surface-variant mb-6 flex-1 line-clamp-3 leading-relaxed">
          {roadmap.description || "Step-by-step developer roadmap with curated resources and prerequisites."}
        </p>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-ink-primary pt-4 mt-auto">
          <div className="flex -space-x-2">
            <div className="w-7 h-7 rounded-full border border-ink-primary bg-surface-container-high flex items-center justify-center text-ink-primary">
              <span className="material-symbols-outlined text-[14px]">
                {isFrontend ? "code" : "database"}
              </span>
            </div>
            <div className="w-7 h-7 rounded-full border border-ink-primary bg-surface-container-high flex items-center justify-center text-ink-primary">
              <span className="material-symbols-outlined text-[14px]">
                {isFrontend ? "css" : "bar_chart"}
              </span>
            </div>
            <div className="w-7 h-7 rounded-full border border-ink-primary bg-surface-container-high flex items-center justify-center text-ink-primary">
              <span className="material-symbols-outlined text-[14px]">
                {isFrontend ? "javascript" : "table_view"}
              </span>
            </div>
          </div>

          <span className="font-label-mono text-ink-primary group-hover:underline flex items-center gap-1">
            Start Path <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
          </span>
        </div>
      </div>
    </Link>
  );
}

import Link from "next/link";

export function Footer() {
  return (
    <footer className="bg-surface-container-low border-t border-ink-primary mt-16 py-12">
      <div className="max-w-container-max mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="flex flex-col items-center md:items-start">
          <div className="flex items-center gap-3 mb-3">
            <img
              alt="DevPath Logo"
              className="h-6 w-auto opacity-70"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAZnA8cueS_29iU4ekKGAPOfO3fbsexi9l6Rt61Vo907MCsL4THl7CO82a6bKh7PweIm6owYFyAafXwCKC3UJ3qUqBc5Qfqfp2_nVoTge8E-MofMRLbMSG0CUp_7KtNxp8kF6yxfVwb1YaFHuuL2E5fwfD7fJsfPN8gD2sjz9am88KVbnc_bAHbOUBlPhMWbmuS1DQ8ewYWF1VpPFwnZcPVR6OBSKAVplEGaAs-S4WjsFgocnRUFNlc"
            />
            <span className="font-headline font-bold text-ink-primary">DevPath CPGS</span>
          </div>
          <p className="font-label-mono text-[11px] text-on-surface-variant">
            DOCUMENTING THE FUTURE OF DEVELOPER ROADMAPS · POWERED BY STITCH
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-8 font-label-mono text-xs">
          <Link href="/roadmaps" className="text-on-surface-variant hover:text-ink-primary transition-colors">
            All Roadmaps
          </Link>
          <Link href="/roadmaps/frontend-developer" className="text-on-surface-variant hover:text-ink-primary transition-colors">
            Frontend
          </Link>
          <Link href="/roadmaps/data-analyst" className="text-on-surface-variant hover:text-ink-primary transition-colors">
            Data Analyst
          </Link>
          <span className="text-ink-primary font-bold">
            &copy; {new Date().getFullYear()}
          </span>
        </div>
      </div>
    </footer>
  );
}

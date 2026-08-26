import { RoadmapDetail, RoadmapSummary, TopicDetail } from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const FALLBACK_ROADMAPS: RoadmapSummary[] = [
  {
    id: "11111111-1111-1111-1111-111111111111",
    slug: "frontend-developer",
    title: "Frontend Developer",
    description: "Step-by-step guide to becoming a modern frontend engineer in 2026.",
    difficulty: "beginner",
    is_published: true,
    seed_version: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "22222222-2222-2222-2222-222222222222",
    slug: "data-analyst",
    title: "Data Analyst",
    description: "Master SQL, Python, data visualization, and statistical modeling in 2026.",
    difficulty: "beginner",
    is_published: true,
    seed_version: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

const FALLBACK_FRONTEND_DETAIL: RoadmapDetail = {
  ...FALLBACK_ROADMAPS[0],
  sections: [
    {
      id: "sec-1",
      title: "Internet & Foundations",
      order_index: 1,
      topics: [
        {
          id: "top-1",
          slug: "how-the-internet-works",
          title: "How the Internet Works",
          difficulty: "beginner",
          estimated_hours: 4,
          order_index: 1,
          depends_on: [],
        },
        {
          id: "top-2",
          slug: "html-basics",
          title: "HTML Basics",
          difficulty: "beginner",
          estimated_hours: 6,
          order_index: 2,
          depends_on: ["how-the-internet-works"],
        },
        {
          id: "top-3",
          slug: "css-fundamentals",
          title: "CSS Fundamentals",
          difficulty: "beginner",
          estimated_hours: 8,
          order_index: 3,
          depends_on: ["html-basics"],
        },
      ],
    },
    {
      id: "sec-2",
      title: "JavaScript Core",
      order_index: 2,
      topics: [
        {
          id: "top-4",
          slug: "js-basics",
          title: "JavaScript Basics",
          difficulty: "beginner",
          estimated_hours: 10,
          order_index: 1,
          depends_on: ["html-basics", "css-fundamentals"],
        },
        {
          id: "top-5",
          slug: "async-javascript",
          title: "Asynchronous JavaScript",
          difficulty: "intermediate",
          estimated_hours: 8,
          order_index: 2,
          depends_on: ["js-basics"],
        },
      ],
    },
  ],
};

const FALLBACK_DATA_ANALYST_DETAIL: RoadmapDetail = {
  ...FALLBACK_ROADMAPS[1],
  sections: [
    {
      id: "sec-da-1",
      title: "SQL & Relational Databases",
      order_index: 1,
      topics: [
        {
          id: "top-da-1",
          slug: "sql-fundamentals",
          title: "SQL Fundamentals",
          difficulty: "beginner",
          estimated_hours: 8,
          order_index: 1,
          depends_on: [],
        },
        {
          id: "top-da-2",
          slug: "sql-advanced-analytics",
          title: "Advanced SQL & Window Functions",
          difficulty: "intermediate",
          estimated_hours: 10,
          order_index: 2,
          depends_on: ["sql-fundamentals"],
        },
      ],
    },
    {
      id: "sec-da-2",
      title: "Python for Data Analysis",
      order_index: 2,
      topics: [
        {
          id: "top-da-3",
          slug: "python-basics-data",
          title: "Python for Data Analytics",
          difficulty: "beginner",
          estimated_hours: 10,
          order_index: 1,
          depends_on: ["sql-fundamentals"],
        },
      ],
    },
  ],
};

export async function fetchRoadmaps(): Promise<RoadmapSummary[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/roadmaps`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    const data = await res.json();
    return data.length > 0 ? data : FALLBACK_ROADMAPS;
  } catch (error) {
    console.warn("Falling back to local static roadmaps:", error);
    return FALLBACK_ROADMAPS;
  }
}

export async function fetchRoadmapBySlug(slug: string): Promise<RoadmapDetail | null> {
  try {
    const res = await fetch(`${API_BASE_URL}/roadmaps/${slug}`, {
      next: { revalidate: 60 },
    });
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn(`Falling back to local static roadmap for slug: ${slug}`, error);
    if (slug === "frontend-developer") return FALLBACK_FRONTEND_DETAIL;
    if (slug === "data-analyst") return FALLBACK_DATA_ANALYST_DETAIL;
    return null;
  }
}

export async function fetchTopicBySlug(
  roadmapSlug: string,
  topicSlug: string
): Promise<TopicDetail | null> {
  try {
    const res = await fetch(
      `${API_BASE_URL}/topics/by-slug/${roadmapSlug}/${topicSlug}`,
      { next: { revalidate: 60 } }
    );
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn(`Falling back to static topic for ${roadmapSlug}/${topicSlug}:`, error);
    const roadmap =
      roadmapSlug === "frontend-developer"
        ? FALLBACK_FRONTEND_DETAIL
        : roadmapSlug === "data-analyst"
        ? FALLBACK_DATA_ANALYST_DETAIL
        : null;

    if (!roadmap) return null;

    for (const section of roadmap.sections) {
      const topic = section.topics.find((t) => t.slug === topicSlug);
      if (topic) {
        return {
          id: topic.id,
          roadmap_slug: roadmapSlug,
          section_id: section.id,
          slug: topic.slug,
          title: topic.title,
          description: `Detailed learning module for ${topic.title}. Follow the structured objectives and curated resources below.`,
          difficulty: topic.difficulty,
          estimated_hours: topic.estimated_hours,
          learning_objectives: [
            `Master foundational concepts of ${topic.title}`,
            `Apply best practices in production environments`,
            `Build hands-on practical exercises and projects`,
          ],
          prerequisites: topic.depends_on,
          resources: [
            {
              id: "res-1",
              title: `Official Documentation & Guides: ${topic.title}`,
              url: "https://developer.mozilla.org",
              resource_type: "documentation",
              access_type: "free",
              difficulty: topic.difficulty,
              source_domain: "developer.mozilla.org",
              summary: "Comprehensive developer reference and interactive examples.",
              is_recommended: true,
              display_order: 1,
            },
          ],
          status: null,
          is_suggested_next: topic.depends_on.length === 0,
        };
      }
    }
    return null;
  }
}

export type DifficultyLevel = "beginner" | "intermediate" | "advanced";

export type ProgressStatus = "not_started" | "in_progress" | "completed" | "skipped";

export type ResourceType =
  | "documentation"
  | "article"
  | "video"
  | "course"
  | "book"
  | "interactive"
  | "repo";

export type AccessType = "free" | "freemium" | "paid" | "unknown";

export interface TopicSummary {
  id: string;
  slug: string;
  title: string;
  difficulty: DifficultyLevel;
  estimated_hours: number;
  order_index: number;
  depends_on: string[];
}

export interface SectionSummary {
  id: string;
  title: string;
  order_index: number;
  topics: TopicSummary[];
}

export interface RoadmapSummary {
  id: string;
  slug: string;
  title: string;
  description: string | null;
  difficulty: DifficultyLevel;
  is_published: boolean;
  seed_version: number;
  created_at: string;
  updated_at: string;
}

export interface RoadmapDetail extends RoadmapSummary {
  sections: SectionSummary[];
}

export interface ResourceSummary {
  id: string;
  title: string;
  url: string;
  resource_type: ResourceType;
  access_type: AccessType;
  difficulty: DifficultyLevel;
  source_domain: string;
  summary: string | null;
  is_recommended: boolean;
  display_order: number;
}

export interface TopicDetail {
  id: string;
  roadmap_slug: string;
  section_id: string;
  slug: string;
  title: string;
  description: string | null;
  difficulty: DifficultyLevel;
  estimated_hours: number;
  learning_objectives: string[];
  prerequisites: string[];
  resources: ResourceSummary[];
  status: ProgressStatus | null;
  is_suggested_next: boolean;
}

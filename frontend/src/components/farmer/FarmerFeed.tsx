/** TikTok-style vertical content feed for farmers. */

import { useState, useEffect } from "react";
import { authClient } from "@/api/auth";
import { ContentCard } from "./common/ContentCard";

interface FeedItem {
  id: string;
  content_type: string;
  title: string;
  title_mm: string | null;
  body: string;
  body_mm: string | null;
  audio_url: string | null;
  published_at: string | null;
}

/** Personalized content feed for farmers. */
export function FarmerFeed() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    authClient
      .get<FeedItem[]>("/feed/")
      .then((r) => setItems(r.data))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  const handleView = (contentId: string) => {
    authClient.post(`/feed/${contentId}/view`).catch(() => {});
  };

  const handleHelpful = (contentId: string, helpful: boolean) => {
    authClient.post(`/feed/${contentId}/helpful`, { helpful }).catch(() => {});
  };

  return (
    <div className="space-y-4 max-w-lg mx-auto">
      <h1 className="text-xl font-display text-text-primary font-myanmar">
        သတင်းအချက်အလက်
      </h1>

      {loading ? (
        <p className="text-text-tertiary text-center py-8">Loading...</p>
      ) : items.length === 0 ? (
        <div className="rounded-xl bg-surface-elevated border border-border p-8 text-center">
          <svg
            className="w-12 h-12 mx-auto text-primary/30 mb-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            strokeWidth={1}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"
            />
          </svg>
          <p className="text-text-secondary font-myanmar">
            အကြောင်းအရာ မရှိသေးပါ
          </p>
          <p className="text-text-tertiary text-sm mt-1">
            Content will appear here when published
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div key={item.id} onMouseEnter={() => handleView(item.id)}>
              <ContentCard
                title={item.title}
                titleMm={item.title_mm}
                body={item.body}
                bodyMm={item.body_mm}
                contentType={item.content_type}
                audioUrl={item.audio_url}
                publishedAt={item.published_at}
                onHelpful={(h) => handleHelpful(item.id, h)}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

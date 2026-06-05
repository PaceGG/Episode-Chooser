export default interface Session {
  game: string;
  gameGroup?: string;
  datetime: number;
  episodes: Episode[];
}

interface Episode {
  number: number | null;
  title: string;
  description: string;
  publishedAt: string;
  videoId?: string;
  duration?: number;
}

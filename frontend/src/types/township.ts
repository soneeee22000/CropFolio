/** A Myanmar township with geographic coordinates. */
export interface Township {
  id: string;
  name: string;
  name_mm: string;
  region: string;
  latitude: number;
  longitude: number;
}

/** API response for listing townships. */
export interface TownshipListResponse {
  count: number;
  townships: Township[];
}

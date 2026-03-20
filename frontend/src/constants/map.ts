/** Myanmar geographic center. */
export const MYANMAR_CENTER: [number, number] = [19.75, 96.13];

/** Default zoom for country view. */
export const DEFAULT_ZOOM = 6;

/** Zoom level when focused on a township. */
export const TOWNSHIP_ZOOM = 12;

/** Buffer radius around township center in meters. */
export const BUFFER_RADIUS_M = 5000;

/** Buffer circle color. */
export const BUFFER_COLOR = "#1b7a4a";

/** OpenStreetMap tile URL and attribution. */
export const OSM_TILE_URL =
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
export const OSM_ATTRIBUTION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>';

/** Field monitor plot marker radius in pixels. */
export const PLOT_MARKER_RADIUS = 8;

/** Compliance status colors for field monitor map. */
export const COMPLIANCE_COLORS: Record<string, string> = {
  compliant: "#1B7A4A",
  warning: "#D4940A",
  deviation: "#C43B3B",
};

/** Esri World Imagery (free satellite basemap) tile URL and attribution. */
export const ESRI_SATELLITE_TILE_URL =
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";
export const ESRI_ATTRIBUTION =
  "Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics";

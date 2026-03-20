import { useEffect, useRef } from "react";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import {
  TOWNSHIP_ZOOM,
  PLOT_MARKER_RADIUS,
  COMPLIANCE_COLORS,
  ESRI_SATELLITE_TILE_URL,
  ESRI_ATTRIBUTION,
} from "@/constants/map";
import type { MonitoredPlot } from "@/types/field-monitor";

interface FieldMonitorMapProps {
  plots: MonitoredPlot[];
  centerLat: number;
  centerLon: number;
  onSelectPlot?: (plotId: string) => void;
  selectedPlotId?: string | null;
}

/** Flies to new coordinates when center changes. */
function FlyToCenter({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap();
  const prevRef = useRef<string>("");

  useEffect(() => {
    const key = `${lat},${lng}`;
    if (key !== prevRef.current) {
      prevRef.current = key;
      map.flyTo([lat, lng], TOWNSHIP_ZOOM, { duration: 1.2 });
    }
  }, [lat, lng, map]);

  return null;
}

/** Leaflet map with color-coded CircleMarkers for each monitored plot. */
export function FieldMonitorMap({
  plots,
  centerLat,
  centerLon,
  onSelectPlot,
  selectedPlotId,
}: FieldMonitorMapProps) {
  return (
    <MapContainer
      center={[centerLat, centerLon]}
      zoom={TOWNSHIP_ZOOM}
      scrollWheelZoom={false}
      className="h-64 sm:h-80 lg:h-96 w-full rounded-lg z-0"
    >
      <TileLayer url={ESRI_SATELLITE_TILE_URL} attribution={ESRI_ATTRIBUTION} />

      {plots.map((plot) => {
        const color = COMPLIANCE_COLORS[plot.compliance.status] ?? "#888";
        const isSelected = plot.plot_id === selectedPlotId;

        return (
          <CircleMarker
            key={plot.plot_id}
            center={[plot.location.latitude, plot.location.longitude]}
            radius={isSelected ? PLOT_MARKER_RADIUS + 3 : PLOT_MARKER_RADIUS}
            pathOptions={{
              color: isSelected ? "#fff" : color,
              fillColor: color,
              fillOpacity: 0.85,
              weight: isSelected ? 3 : 2,
            }}
            eventHandlers={{
              click: () => onSelectPlot?.(plot.plot_id),
            }}
          >
            <Popup>
              <div className="text-xs">
                <div className="font-medium">{plot.farmer_name}</div>
                <div>
                  {plot.recommended_crop.replace("_", " ")} &middot;{" "}
                  {plot.area_ha} ha
                </div>
                <div className="capitalize">{plot.compliance.status}</div>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}

      <FlyToCenter lat={centerLat} lng={centerLon} />
    </MapContainer>
  );
}

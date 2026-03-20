import { useEffect, useRef } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Circle,
  Popup,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  TOWNSHIP_ZOOM,
  BUFFER_RADIUS_M,
  BUFFER_COLOR,
  ESRI_SATELLITE_TILE_URL,
  ESRI_ATTRIBUTION,
} from "@/constants/map";

/* Fix Leaflet default marker icons missing in Vite bundled builds. */
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

interface SARMapViewProps {
  latitude: number;
  longitude: number;
  townshipName: string;
  geeOverlayUrl?: string;
}

/** Flies the map to new coordinates when the township changes. */
function FlyToTownship({ lat, lng }: { lat: number; lng: number }) {
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

/** Interactive Leaflet map showing the selected township with a buffer circle. */
export function SARMapView({
  latitude,
  longitude,
  townshipName,
  geeOverlayUrl,
}: SARMapViewProps) {
  return (
    <MapContainer
      center={[latitude, longitude]}
      zoom={TOWNSHIP_ZOOM}
      scrollWheelZoom={false}
      className="h-64 sm:h-80 lg:h-96 w-full rounded-lg z-0"
    >
      {/* Base layers */}
      <TileLayer url={ESRI_SATELLITE_TILE_URL} attribution={ESRI_ATTRIBUTION} />

      {/* GEE overlay — Phase 2 */}
      {geeOverlayUrl && <TileLayer url={geeOverlayUrl} opacity={0.6} />}

      {/* Township marker */}
      <Marker position={[latitude, longitude]}>
        <Popup>{townshipName}</Popup>
      </Marker>

      {/* 5km buffer circle */}
      <Circle
        center={[latitude, longitude]}
        radius={BUFFER_RADIUS_M}
        pathOptions={{
          color: BUFFER_COLOR,
          fillColor: BUFFER_COLOR,
          fillOpacity: 0.12,
          weight: 2,
        }}
      />

      <FlyToTownship lat={latitude} lng={longitude} />
    </MapContainer>
  );
}

import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function PolandMap({ children }) {
  return (
    <MapContainer center={[52.0, 15.5]} zoom={7} style={{ height: '750px', width: '70%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {children}
    </MapContainer>
  );
}

export default PolandMap;

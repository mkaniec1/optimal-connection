import { Polyline } from 'react-leaflet';

function CityLine({ positions, onClick }) {
  return (
    <Polyline
      positions={positions}
      color="blue"
      weight={2}
      eventHandlers={{
        click: onClick,
      }}
    />
  );
}

export default CityLine;

import { Polyline } from 'react-leaflet';

function CityLine({ positions, onClick, highlight, x }) {
  let color = "blue";
  let weight = 2;
  if (highlight){
    color = "red";
    weight = "10";
  }
  return (
    <Polyline
      positions={positions}
      color={color}
      weight={weight}
      eventHandlers={{
        click: onClick,
      }}
    />
  );
}

export default CityLine;

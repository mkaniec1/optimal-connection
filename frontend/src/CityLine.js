import { Polyline } from 'react-leaflet';

function CityLine({ positions, onClick, highlight, displayingInfo }) {
  let color = "blue";
  let weight = 4;
  if (highlight){
    color = "red";
    weight = "10";
  }
  if (displayingInfo){
    color = "black";
    weight = "6";
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

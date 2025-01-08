import { Marker } from 'react-leaflet';
import L from 'leaflet';

const CityMarker = ({ position, id, path, onClick, orangePurple }) => {
  let color = 'blue';
  if (id === path[0]){
    color = 'green';
  } else if (id === path[1]){
    color = 'red';
  }
  if (id === orangePurple[0]){
    color = 'orange';
  } else if (id === orangePurple[1]){
    color = 'purple';
  }
  const cityIcon = L.divIcon({
    className: 'custom-city-icon',
    html: `<div style="width: 20px; height: 20px; background-color: ${color}; border-radius: 50%;"></div>`,
    iconSize: [20, 20],
  });

  return <Marker position={position} icon={cityIcon} eventHandlers={{ click: onClick }} />;
};

export default CityMarker;

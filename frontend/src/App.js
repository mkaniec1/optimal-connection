import React, { useState, useEffect, useRef } from 'react';
import CityLine from './CityLine';
import CityMarker from './CityMarker';
import RouteSelector from './RouteSelector';
import ReserveSpaceButton from './ReserveSpaceButton';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function App() {
  const backend_address = 'http://localhost:8000';
  const [cities, setCities] = useState({});
  const [connections, setConnections] = useState([]);
  const [startEndPath, setStartEndPath] = useState([undefined, undefined]);
  const [pathToModify, setPathToModify] = useState(0);
  const [bestRoute, setBestRoute] = useState([]);
  const [map, setMap] = useState(null);
  const [uniqueRoutes, setUniqueRoutes] = useState([]);
  const mapRef = useRef();
  const inputGHzRef = useRef();


  useEffect(() => {
    const fetchConnectionsData = async () => {
      try {
        const response = await fetch(backend_address + '/api/connections', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await response.json();
        const cityData = {};
        data.cities.forEach(city => {
          cityData[city[0]] = [city[1], city[2]];
        });
        setCities(cityData);
        setConnections(
          data.connections.map(conn => ({
            id: conn[0],
            starting_node_id: conn[1],
            ending_node_id: conn[2],
            total_capacity: conn[3],
            provisioned_capacity: conn[4]
          }))
        );

      } catch (error) {
        console.error('Error fetching city coordinates', error);
      }
    };
    fetchConnectionsData();
  }, []);

  const handleLineClick = (conn) => {
    alert(`Conn busy in ${conn.provisioned_capacity}%`);
  };

  const handleCityClick = (id) => {
    setStartEndPath((prevPath) => {
      const updatedPath = [...prevPath];
      updatedPath[pathToModify] = id;
      return updatedPath;
    });
    setPathToModify(pathToModify === 0 ? 1 : 0);
  };

  const handleReserveSpaceClick = async () => {
    if (startEndPath[0] === startEndPath[1] || !startEndPath[0] || !startEndPath[1]){
      alert('invalid cities!');
      return
    }
    const csrfToken = getCookie('csrftoken');
    try {
      const response = await fetch(backend_address + '/api/reserve', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          startNode: startEndPath[0],
          endNode: startEndPath[1],
          space: inputGHzRef.current.value,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setBestRoute(data.bestRoutes[0].route);
        setUniqueRoutes(data.bestRoutes);
      } else {
        const data = await response.json();
        alert(data.error);
        console.warn('Invalid response from server');
      }
    } catch (error) {
      console.error('Error requesting reservation: ', error);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px', display: 'flex', flexDirection: 'row' }}>
      <MapContainer
        center={[52.0, 15.5]}
        zoom={7}
        style={{ height: '850px', width: '70%' }}
        whenReady={setMap}
        ref={mapRef}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {connections.map((conn, index) => (
          <CityLine
            key={`${conn.id}-${bestRoute.includes(conn.id)}`}
            positions={[cities[conn.starting_node_id], cities[conn.ending_node_id]]}
            onClick={() => handleLineClick(conn)}
            highlight={bestRoute.includes(conn.id)}
            x={index}
          />
        ))}
        {Object.entries(cities).map(([id, coords]) => (
          <CityMarker
            key={id}
            position={coords}
            id={id}
            path={startEndPath}
            onClick={() => handleCityClick(id)}
          />
        ))}
      </MapContainer>
      <div style={{width: '25%'}}>
        <div style={{ textAlign: 'center' }}>
          <p>From <span style={{color:'green'}}>{startEndPath[0] ? startEndPath[0] : '.......'}</span>
            &nbsp; to <span style={{color:'red'}}>{startEndPath[1] ? startEndPath[1] : '.......'}</span></p>
          <p>GHz:  <input ref={inputGHzRef} type='number' style={{width: '50px'}}></input></p>
          <ReserveSpaceButton onClick={handleReserveSpaceClick} />
        </div>
        {uniqueRoutes.map((uniqueRoute, index) => (
          <RouteSelector
           key={index}
           route={uniqueRoute.route}
           count={uniqueRoute.count}
           onClick={() => setBestRoute(uniqueRoute.route)}
           highlight={uniqueRoute.route === bestRoute}
          />
        ))}
      </div>
    </div>
  );
}

function getCookie(name) {
  const cookieValue = document.cookie
    .split('; ')
    .find((row) => row.startsWith(name + '='))
    ?.split('=')[1];
  return cookieValue || '';
}

export default App;
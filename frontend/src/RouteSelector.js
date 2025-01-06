function RouteSelector({ route, count, onClick, highlight }) {
    let borderColor = "black";
    if (highlight){
        borderColor = "red";
    }
  return (
    <div
    style={{
        borderColor:borderColor,
        borderWidth:'1px',
        borderStyle:'solid',
        cursor:'pointer',
        padding:'10px}',
        margin:'10px',
        borderRadius:'10px'}}
    onClick={onClick}>
        <p>
            {route.map((connId) => (
                <span> {connId} </span>
            ))}
        </p>
        <p>
            Count: {count}
        </p>
    </div>
  );
}

export default RouteSelector;
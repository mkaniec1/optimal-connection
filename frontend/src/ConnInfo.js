
// example of channels:
import React from "react";
import "./ConnInfo.css"; // External CSS file for better organization

function ConnInfo({ capacityPercent, orangePurpleId, purpleOrangeId, channels = {
    "12.5": 0,
    "50.0": 0,
    "75.0": 0,
    "112.5": 0
}}) {
    return (
    <div className="connInfoContainer">
      <div className="capacityContainer">
        <p className="capacityText">Used capacity: {capacityPercent}%</p>
      </div>
      <div>
        <div className="connGraphicsContainer">
          <div className="circle" style={{ backgroundColor: "orange" }}></div>
          <div className="arrow">----------&gt;</div>
          <div className="circle" style={{ backgroundColor: "purple" }}></div>
          <span className="idLabel">id: {orangePurpleId}</span>
        </div>
        <div className="connGraphicsContainer">
          <div className="circle" style={{ backgroundColor: "purple" }}></div>
          <div className="arrow">----------&gt;</div>
          <div className="circle" style={{ backgroundColor: "orange" }}></div>
          <span className="idLabel">id: {purpleOrangeId}</span>
        </div>
      </div>
      <div>
        <p className="channelsTitle">Channels:</p>
        <table className="channelsTable">
          <thead>
            <tr>
              <th>Width</th>
              <th>Count</th>
              <th>GHz</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>12.5</td>
              <td>{channels["12.5"]}</td>
              <td>{channels["12.5"] * 12.5}</td>
            </tr>
            <tr>
              <td>50</td>
              <td>{channels["50.0"]}</td>
              <td>{channels["50.0"] * 50}</td>
            </tr>
            <tr>
              <td>75</td>
              <td>{channels["75.0"]}</td>
              <td>{channels["75.0"] * 75}</td>
            </tr>
            <tr>
              <td>112.5</td>
              <td>{channels["112.5"]}</td>
              <td>{channels["112.5"] * 112.5}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ConnInfo;

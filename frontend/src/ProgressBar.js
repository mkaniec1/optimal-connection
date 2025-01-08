import React, { useState, useEffect } from 'react';

const ProgressBar = ({ progress }) => {

    // useEffect(() => {
    //     if (isCalculating) {
    //         const eventSource = new EventSource(`${backendAddress}/api/reserve`);

    //         eventSource.onmessage = (event) => {
    //             setProgress(Number(event.data)); // Update progress
    //             if (Number(event.data) === 100) {
    //                 setIsCalculating(false); // Stop when complete
    //             }
    //         };

    //         eventSource.onerror = () => {
    //             eventSource.close(); // Close connection on error
    //             setIsCalculating(false); // Reset calculating state
    //         };

    //         return () => eventSource.close(); // Cleanup
    //     }
    // }, [isCalculating, backendAddress, setIsCalculating]);

    // if (!isCalculating) {
    //     return null; // Do not render if not calculating
    // }
    return (
        <div style={{
                position: 'fixed',
                top: '20px',
                left: '50%',
                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                color: 'white',
                zIndex: 1000,
                transform:'translateX(-50%)',
                width: '300px',
                height: '20px'
            }}>
            <p style={{
                margin:'0px',
                padding: '0px',
                position: 'fixed',
                top: '2px',
                left: '50%',
                transform: 'translateX(-50%)',
                backgroundColor: 'rgba(0,0,0,0)',
                fontSize: '15px'

              }}>{progress}%</p>
            <div style={{ width: '100%', border: '1px solid white' }}>
                <div
                    style={{
                        width: `${progress}%`,
                        backgroundColor: 'green',
                        height: '20px',
                    }}
                />
            </div>
        </div>
    );
};

export default ProgressBar;

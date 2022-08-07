import React, { Component } from 'react';
import CanvasDraw from 'react-canvas-draw';
import { w3cwebsocket as W3CWebSocket } from "websocket";

function onMessage() {
  window.saveableCanvas.loadSaveData();
}

function onChange() {
  console.log(window.saveableCanvas.getSaveData());
}

class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <CanvasDraw
                ref={canvasDraw => (window.saveableCanvas = canvasDraw)}
                onChange={onChange}
                canvasWidth={window.innerWidth}
                canvasHeight={window.innerHeight}
                hideGrid={true}
                brushRadius={1}
                lazyRadius={0}
              />
        );
    }
}

export default App;
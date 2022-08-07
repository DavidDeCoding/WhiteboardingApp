import React, { Component } from 'react';
import CanvasDraw from 'react-canvas-draw';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import { v4 as uuidv4 } from 'uuid';

const url = "wss://5d4l39qktg.execute-api.us-west-1.amazonaws.com/dev";
const ws = new W3CWebSocket(url);

function onMessage(message) {
    const lines = JSON.parse(message.data);


}

function onChange(event) {
    console.log(event);
    const message = window.saveableCanvas.getSaveData();
    ws.send(JSON.stringify({
        action: "onMessage",
        message: JSON.stringify(message)
    }));
}

class App extends Component {
    constructor(props) {
        super(props);
    }

    componentWillMount() {
        ws.onopen = (event) => {
            console.log(`Connected to ${url}}`);
        };

        ws.onmessage = (message) => {
            onMessage(message);
        };
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
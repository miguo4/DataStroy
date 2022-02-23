import React from 'react';
import { Progress } from "antd";

export default class ProgressBarView extends React.Component {

    render() {
        const { percent, isActive } = this.props
        return (<Progress
            percent={percent}
            status={isActive ? "active" : ""}
            showInfo={false}
            strokeColor="#EB6331"
            style={{
                position: "absolute", top: "-10px", zIndex: "9999",
                display: isActive ? "block" : "none"
            }} />)
    }
}
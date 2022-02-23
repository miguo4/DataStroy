import React, { Component } from 'react';
import { AutoVis } from "calliope-chart";

export default class Chart extends Component {

    componentDidMount() {
        const { id } = this.props.spec.chart;
        let spec = this.props.spec;
        let container = id ? `#vischart_${id}` : "#demo-chart";
        this.autovis = new AutoVis();
        this.autovis = new AutoVis();
        this.autovis.container(container);
        this.autovis.load(spec);
        this.autovis.generate();
    }

    componentDidUpdate(preProps) {
        const { id } = this.props.spec.chart;
        let spec = this.props.spec;
        let container = id ? `#vischart_${id}` : "#demo-chart";
        this.autovis = new AutoVis();
        this.autovis = new AutoVis();
        this.autovis.container(container);
        this.autovis.load(spec);
        this.autovis.generate();
    }

    render() {
        let height = 640, width = 640;
        if (this.props.spec.chart) {
            let { size, type } = this.props.spec.chart;
            if (type === 'vegalite') {
                let vega_w = this.props.spec.chart.width,
                    vega_h = this.props.spec.chart.height;
                height = vega_h * 0.5
                width = vega_w * 0.5
            } else {
                switch (size) {
                    case 'wide':
                        height = 220;
                        width = 560;
                        break;
                    case 'middle':
                        height = 200;
                        width = 360;
                        break;
                    case 'small':
                        height = 150;
                        width = 235;
                        break;

                    default:
                        break;
                }
            }

        }
        //console.log("render", width, height);
        const { id } = this.props.spec.chart ? this.props.spec.chart : { id: "demo-chart" };
        return (
            // <div id='frame'
            //     style={{
            //         // marginLeft: 60,
            //         // marginTop: 60,
            //         height: height,
            //         width: width,
            //         borderStyle: 'solid',
            //         borderWidth: 1,
            //         borderColor: 'red'
            //     }}
            // >
            //     <div id={id ? `vischart_${id}` : 'demo-chart'} style={{ height: height, width: width }} />
            // </div>
            <div id={id ? `vischart_${id}` : 'demo-chart'} style={{ height: "640", width: "640", display: "flex", alignItems: "center", justifyContent: "center", visibility: "hidden" }} />
        )
    }
}

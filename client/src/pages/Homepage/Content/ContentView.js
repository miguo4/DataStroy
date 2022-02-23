import React from 'react';
import { Layout, Divider, Upload } from 'antd';
import "./ContentView.less";

export default class ContentView extends React.Component {

    render() {
        const { intl, initDone } = this.props;

        const BoxView = ({ isLast, num, isActive, url, text }) => {
            return (
                <>
                    <div className='step-box'>
                        <div className='index' style={{ background: isActive ? "#FDBE31" : '#5D5C64' }}>{num}</div>
                        <div className='box' >
                            <div style={{ backgroundImage: 'url(' + require("../../../images/icon/" + url) + ')' }}></div>
                            <div>{text}</div>
                        </div>
                    </div>
                    {
                        !isLast && <div className='arrow'></div>
                    }
                </>
            )
        }

        const SloganView = () => {
            return (
                <div className="SloganView">
                    <div className="decorationImage">
                        <span >{initDone && intl.get("calliope-talk")}</span>
                        <span></span>
                        <ul>
                            <li>{initDone && intl.get("future_1")}</li>
                        </ul>
                        <div className='steps'>
                            <BoxView isActive={true} num={1} text={initDone && intl.get("Upload")} url={'upload.png'} />
                            <BoxView isActive={false} num={2} text={initDone && intl.get("Ask Data")} url={'voice.png'} />
                            <BoxView isActive={false} num={3} text={initDone && intl.get("Visualize")} url={'vis.png'} isLast={true} />
                        </div>
                    </div>
                    <div className="custom"></div>
                </div>
            )
        };

        return (
            <div className='ContentView' >
                <SloganView />
                <Layout style={{ marginTop: "23px", width: "100%", backgroundColor: "white" }}>
                    {
                        this.props.children
                    }
                </Layout>
            </div>
        )
    }
}
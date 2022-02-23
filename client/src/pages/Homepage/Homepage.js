import React from 'react';
import { Layout, Divider } from "antd";
import HeadBarView from "@/components/HeadBar/index";
import ContentView from "./Content/ContentView";
import PannelView from "./PannelView/index";
import "./Homepage.less";

const { Header, Footer, Content } = Layout;

const FooterView = ({ intl, initDone }) => {
    return (<div className="footerWrapper">
        <div></div>
        <span>{initDone && intl.get("calliope-talk")}</span>
        <div ></div>
        <span>{initDone && intl.get("slogan")}</span>
        <a href='https://calliope@idvxlab.com' target="_blank" rel="noopener noreferrer"> {initDone && intl.get("Contact us")} </a>
    </div>)
}

export default class Homepage extends React.Component {

    render() {
        return (
            <Layout style={{ height: "100%" }}>
                <Header style={{ height: "50px" }}>
                    <HeadBarView isLogIn={false} {...this.props} />
                </Header>
                <Divider className="customDivider" />
                <Content className="pageWrapper">
                    <ContentView {...this.props}>
                        <PannelView {...this.props}></PannelView>
                    </ContentView>
                </Content>
                {/* <Footer style={{ padding: "35px 0px", height: "60px", width: "100%", margin: "0 auto" }}>
                    <FooterView {...this.props} />
                </Footer> */}
            </Layout >
        )
    }
}
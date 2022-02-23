
import React from 'react'
import { Spin } from 'antd';
import './SpiningView.less'

export default class SpiningView extends React.Component {

    render() {
        const { isSpining, initDone, intl } = this.props
        return <>
            <Spin tip={initDone && intl.get("downloading")} spinning={isSpining} />
        </>
    }
}
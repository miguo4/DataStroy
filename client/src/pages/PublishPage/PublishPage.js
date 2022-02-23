import React from 'react'
import { Button } from "antd";

import './PublishPage.less'

export default class PublishPage extends React.Component {

    save = () => {

    }


    render() {
        return (<div className="publish-page-wrapper">
            PublishPage
            <Button onClick={this.save}>share</Button>
        </div>)
    }
}
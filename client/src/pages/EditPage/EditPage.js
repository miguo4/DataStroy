import React from 'react'
import { Layout, Divider, Button, Input } from "antd"
// import HeadBarView from "@/components/HeadBar/index"
import TalkBottom from '@/components/TalkBottomView/index';
import Dashboard from './Dashboard/index'
import config from '@/axios/config';
import * as d3 from 'd3';

import './EditPage.less'

// const { Header } = Layout;

export default class EditPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            toggle: false,
            question: this.props.question,
            enableEdit: false
        };
    }

    componentDidMount() {
        const { data, fileName } = this.props
        // this.getQuestion()
        if (this.props.data.length === 0) {
            this.loadData(fileName)
        }
    }
    loadData = (fileName) => {
        let fileURL = `${config.url.uploadPrefix}/data/${fileName}`
        //this._processData(fileURL, fileName, this._getSchema(fileName))
        this._processData(fileURL, fileName, this.props.schema)
    }
    // _getSchema = (fileName) => {
    //     let schema = require('../DataPage/shema/' + fileName.split('.csv')[0] + '.json').fields
    //     return schema
    // }
    _processData = (fileURL, fileName, schema) => {
        let numericalFields = []
        let numerical = schema.filter(d => d.type === "numerical")
        numericalFields = numerical.map(d => d.field)
        let _that = this
        d3.csv(fileURL)
            .then(function (data) {
                data.forEach((d, i) => {
                    for (let key in d) {
                        if (numericalFields.indexOf(key) !== -1) {
                            d[key] = parseFloat(d[key])
                        }
                    }
                })
                _that.props.uploadData(fileName, schema, data);
            }).catch(function (error) {
                console.log(error)
            })
    }
    generate = (question) => {
        this.setState({
            question
        })
    }

    componentWillReceiveProps(nextProps) {
        // console.log("EditPage componentWillReceiveProps", nextProps.question, this.state.question);
        if (nextProps.question !== this.state.question) {
            this.setState({
                question: nextProps.question
            })
        }
    }
    enableEdit = (isEnable) => {
        this.setState({
            enableEdit: isEnable
        })
    }
    touch = () => {
        if (!this.state.enableEdit) {
            this.props.closePannel(true)
        }
    }
    render() {
        const { intl, initDone, history } = this.props;
        const { question, enableEdit } = this.state

        return <Layout style={{ height: '100%', backgroundColor: '#f1f2f5' }} >
            {/* <Header style={{ height: "50px" }}>
                <HeadBarView isLogIn={false} {...this.props} />
            </Header>
            <Divider className="customDivider" /> */}
            <div className="talk-main" onClick={this.touch}>
                <div className="talk-content">
                    <div className="content-right">
                        <Dashboard
                            question={question}
                            isEdit={enableEdit}
                            initDone={initDone}
                            intl={intl} />
                    </div>
                </div>
            </div>
            <div className="talk-bottom">
                <TalkBottom initDone={initDone} intl={intl} generate={this.generate} history={history}
                    isEditPage={true}
                    enableEdit={this.enableEdit} />
            </div>
        </Layout >
    }
}

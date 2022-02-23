import React, { PureComponent } from 'react'
import TalkBottom from '@/components/TalkBottomView/index';
import QuestionList from './questionList/index'
import FieldView from './fieldView/FieldView'
import TableView from './tableView/index';
import config from '@/axios/config';

import * as d3 from 'd3';

import './DataPage.less'



export default class DataPage extends PureComponent {


    componentDidMount() {
        if (this.props.data.length === 0) {
            this.loadData(this.props.fileName)
        }
    }
    generate = (question) => {
        this.props.updateQuestion(question)
        this.props.history.push('/edit')
    }
    loadData = (fileName) => {
        let fileURL = `${config.url.uploadPrefix}/data/${fileName}`
        this._processData(fileURL, fileName, this._getSchema(fileName))
    }

    onChange = (e) => {
        let fileName = e.target.value
        this.loadData(fileName)
    }
    _getSchema = (fileName) => {
        let schema = require('./shema/' + fileName.split('.csv')[0] + '.json').fields
        return schema
    }
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

    touch = () => {
        this.props.closePannel(true)
    }
    render() {
        //const { intl, initDone } = this.props;

        const { intl, initDone, fileName, history } = this.props;

        return (
            <div className='data-page' >
                <div className="left" >
                    <div className='dataset-selector'>
                        <select defaultValue={fileName} onChange={this.onChange}>
                            <option value='BestsellingBook.csv'>BestsellingBook.csv</option>
                            <option value='CarSales.csv'>CarSales.csv</option>
                            <option value='CanadaEmissions.csv'>CanadaEmissions.csv</option>
                            <option value='USElection.csv'>USElection.csv</option>
                        </select>
                    </div>
                    <div className='table-box' onClick={this.touch}>
                        <TableView />
                    </div>
                    <TalkBottom initDone={initDone} intl={intl} generate={this.generate} isEditPage={false} history={history} />
                </div>
                <div className="right">
                    <QuestionList intl={intl} initDone={initDone} history={history} />
                    <FieldView />
                </div>
            </div>
        )
    }
}
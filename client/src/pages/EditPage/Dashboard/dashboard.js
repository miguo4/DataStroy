import React, { Component } from 'react'
import { Spin } from 'antd';
import LayoutView from './Layout/layout'
import { getFactChartType } from '@/tool/fact2vis/fact2vis';
// import BlankView from './blank'
// import demoResponse from '../assets/json/demoResponse'
import * as api from '@/axios/api'
import './dashboard.less'


export default class Dashboard extends Component {

    state = {
        question: this.props.question,
        decomposedQA: [],
        loading: false
    }

    componentDidMount() {
        // this.setState({
        //     decomposedQA: this.addParams(demoResponse.story),
        // })
        const { cachedQA, question } = this.props
        if (cachedQA) {
            this.setState({
                decomposedQA: cachedQA
            })
        } else {
            this.getData(question)
        }
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.question !== this.state.question) {
            this.setState({
                question: nextProps.question
            })
            this.getData(nextProps.question)
        } else {
            const { cachedQA } = nextProps
            if (!cachedQA) return null
            this.setState({
                decomposedQA: cachedQA
            })
        }
    }

    getData = async (question) => {
        const { fileName } = this.props
        let data = {
            file_name: fileName,
            question,
            model: ''
        }
        this.setState({
            loading: true
        })
        this.props.updateQuestion(question)
        let response = await api.generate(data)
        if (!response.data || response.data === 'talk-generator error') {
            this.setState({
                loading: false,
                decomposedQA: []
            })
            return
        }
        let decomposedQA = this.addParams(response.data.story)
        this.setState({
            loading: false,
            decomposedQA
        })
        this.props.saveCachedDecomposedQA(decomposedQA)
    }

    constructGroupBy = (breakdown) => {
        return breakdown.map(d => d.field)
    }
    addParams = (story) => {
        return story.map((d, id) => {
            return {
                question: d.question,
                id,
                facts: d.facts.map(fact => {
                    if (!fact.chart || fact.chart === "") {
                        fact.groupby = this.constructGroupBy(fact.breakdown)
                        fact.chart = getFactChartType(this.props.schema, fact);
                    }
                    return {
                        ...fact,
                        groupby: fact.breakdown[0] ? [fact.breakdown[0].field] : []
                    }
                })
            }
        })
    }
    render() {
        const { decomposedQA, question, loading } = this.state
        const { initDone, intl } = this.props

        return (
            <div className='Dashboard spin-center'>
                {
                    loading && <Spin tip={initDone && intl.get("Coverting")} ></Spin>
                }
                <LayoutView
                    loading={loading}
                    askedQuestion={question}
                    decomposedQA={decomposedQA}
                    {...this.props} />
            </div>
        )
    }
}

import React, { Component } from 'react'
import { Spin } from 'antd';
import * as api from '@/axios/api'

import './QuestionList.less'


export default class QuestionList extends Component {

    state = {
        questions: [],
        isLoading: false
    }

    componentWillMount() {
        this.getQuestion(this.props.columName)
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.columName !== this.props.columName) {
            this.getQuestion(nextProps.columName)
        }
    }
    getQuestion = async (columName) => {
        const { fileName, schema } = this.props

        this.setState({
            isLoading: true
        })

        let data = {
            file_name: fileName,
            column_name: columName || ' ',
        }
        let response = await api.getQuestions(data)

        this.setState({
            isLoading: false,
            questions: response.data.length > 0 ? response.data : []
        })
    }
    generate = (question) => {
        this.props.updateQuestion(question)
        this.props.history.push('/edit')
    }
    render() {
        const { intl, initDone } = this.props;
        let { questions, isLoading } = this.state

        return (
            <>
                <div className="Question">{initDone && intl.get('qa')}</div>
                <div className="QuestArray">
                    {
                        isLoading ? <Spin tip={initDone && intl.get("Loading")} ></Spin>
                            :
                            questions.map((q, id) => {
                                const time = 0.2 + 0.1 * id;
                                return <p key={id} className={`p-${id}`} style={{ animationDuration: `${time}s` }} onClick={() => this.generate(q)} >{q}</p>
                            })
                    }
                </div>
            </>
        )
    }
}
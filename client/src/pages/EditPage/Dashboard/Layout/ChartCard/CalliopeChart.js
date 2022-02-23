import React, { Component } from 'react'
import { fact2chart } from '@/tool/fact2vis/fact2vis'


export default class CalliopeChart extends Component {
    shouldRender = false

    componentWillMount() {
        //console.log("CalliopeChart componentWillMount");
        this.shouldRender = true
    }

    shouldComponentUpdate() {
        if (this.shouldRender) {
            this.shouldRender = false//only render once 
            return true
        }
        return false
    }


    getSize = () => {
        return "large"
    }

    render() {
        //console.log("CalliopeChart render");
        const { schema, fact, data } = this.props
        return (
            <>
                {
                    fact2chart({ schema }, fact.id, fact, data, this.getSize())
                }
            </>)
    }
}
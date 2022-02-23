import React, { Component } from 'react'
import './dashboard.less'

export default class BlankView extends Component {
    render() {
        const { initDone, intl } = this.props

        const StepViewBox = (props) => {
            return <>
                <span className='step-box'>
                    <p className='num_style'>{props.num}</p>
                    {
                        props.children
                    }
                </span>
                <br></br>
            </>
        }
        return (
            <div className='blank' >
                <div className='Talk2Data'>
                    <h1>{initDone && intl.get("calliope-talk")}</h1>
                    <StepViewBox num={1}><span>{initDone && intl.get("step11")}</span> </StepViewBox>
                    <StepViewBox num={2}><span>{initDone && intl.get("clickThe")}<p style={{ padding: '0px 4px' }}>{`"${initDone && intl.get("OK")}"`}</p>{initDone && intl.get("step22")}</span> </StepViewBox>
                    <StepViewBox num={3}><span>{initDone && intl.get("step33")}</span> </StepViewBox>
                </div>
                <div className='undraw_card'></div>
            </div>
        )
    }
}
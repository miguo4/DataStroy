
import React from 'react'
import './ButtonBoxView.less'


export default class ButtonBoxView extends React.Component {

    render() {
        const { iconUrl, text } = this.props
        return <div className='button-box' onClick={() => this.props.onClickListener()}>
            <div style={{ backgroundImage: `url(${iconUrl})` }}></div>
            <p>{text}</p>
        </div>

    }
}
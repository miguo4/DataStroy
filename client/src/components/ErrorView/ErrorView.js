import React, { PureComponent } from 'react'
import './ErrorView.less'

export default class ErrorView extends PureComponent {

    render() {
        const { initDone, intl } = this.props
        return (
            <div className='ErrorView'>
                <div />
                <p>{initDone && intl.get('empty')}</p>
            </div>
        )
    }
}
import React, { PureComponent } from 'react'
import Color from '@/constant/Color'
import './FieldView.less'

const RowView = ({ background, type, url }) => {
    return (
        <div className='rowView' style={{ backgroundColor: background }}>
            <div className='icon'>
                <img src={require("../../../images/" + url)}></img>
            </div>
            <div className='text'>{type}</div>
        </div >
    )
}

export default class FieldView extends PureComponent {
    render() {
        return (
            <div className="field-type" >
                <RowView background={Color.Numerical} type={"Numerical"} url='icon/numerical.png' />
                <RowView background={Color.Categorical} type={"Categorical"} url='icon/categorical.png' />
                <RowView background={Color.Temporal} type={"Temporal"} url='icon/temporal.png' />
                <RowView background={Color.Geographical} type={"Geographical"} url='icon/geographical.png' />
                <RowView background={Color.Identification} type={"Identification"} url='icon/identification.png' />
            </div>
        )
    }
}
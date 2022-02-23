
import React from 'react'
import SpiningView from '../Spining/SpiningView';
import './CommonSlotView.less'
import '../../common.less'


/**** 定义组件的外观***/
export default class CommonSlotView extends React.Component {
    render() {
        const { fileName, initDone, intl, columnCount, form, isSpining } = this.props
        let pdfName = fileName && fileName.split(".csv")[0]

        const FileTypeAndNameView = () => {
            return <div className='fileTypeAndNameView' style={{ justifyContent: isSpining ? "flex-start" : "center" }}>
                <div className='fileType-icon'></div>
                <span style={{ marginBottom: "0px" }} >{form === "H5" ? '' : `${pdfName}.pdf`}</span>
            </div>
        }

        return <div className={this.props.myClassName ? `generated-view-dox ${this.props.myClassName}` : 'generated-view-dox'}>
            <span >{initDone && intl.get(form === "H5" ? "convertedTxtH5" : "convertedTxt")}</span>
            <FileTypeAndNameView />
            <div className="FuntionView" style={{ columnCount }}>
                <div className='download-box'>
                    <SpiningView isSpining={isSpining} {...this.props} />
                </div>
                {
                    this.props.children
                }
            </div>
            <span >{initDone && intl.get("Visit")}<a style={{ padding: '0px 5px' }} href='https://datacalliope.com' target="_blank" rel="noopener noreferrer">Calliope · Data</a>{initDone && intl.get("VisitCalliope")}</span>
        </div>
    }
}
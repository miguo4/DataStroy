import React from 'react'
import ConvertForms from '@/constant/config'
import OperationType from '@/constant/OperationType'
import ButtonBoxView from '../Components/ButtonBox/ButtonBoxView'
import CommonSlotView from '../Components/commonSlot/CommonSlotView'
import AliCloud from '@/constant/imageUrl'
import * as api from '@/axios/api'
import './ToFactsheet.less'
import '../common.less'


export default class ToFactsheet extends React.Component {

    state = {
        isDownloading: false
    }

    download = () => {
        this.setState({
            isDownloading: true
        })
        //pdf下载功能
        let data = {

        }
        api.generatePDF(data).then(() => { })
    }

    reUpload = () => {
        this.props.updateOperation(OperationType.BEFORE_UPLOAD)
    }
    reGnerate = () => {
        this.props.reGnerate(ConvertForms[0])
    }
    editPage = () => {
        this.props.history.push('/edit/factsheet')
    }
    click = (text) => {
        const { intl, initDone } = this.props;
        switch (text) {
            case initDone && intl.get("Upload"):
                this.reUpload()
                break;
            case initDone && intl.get("Regnerate"):
                this.reGnerate()
                break;
            case initDone && intl.get("Download"):
                this.download()
                break;
            case initDone && intl.get("Edit"):
                this.editPage()
                break;
            default:
                break;
        }
    }

    render() {
        const { intl, initDone, fileName } = this.props;
        const { isDownloading } = this.state
        //add your button here
        const supportedButton = [
            {
                iconUrl: `${AliCloud}/upload_white.png`,
                text: initDone && intl.get("Upload")
            },
            {
                iconUrl: `${AliCloud}/download/regenerate.png`,
                text: initDone && intl.get("Regnerate")
            },
            {
                iconUrl: `${AliCloud}/download/download.png`,
                text: initDone && intl.get("Download")
            }
        ]
        return (
            <CommonSlotView myClassName={"toFactsheet"} fileName={fileName} isSpining={isDownloading} columnCount={supportedButton.length} {...this.props}>
                {
                    supportedButton.map((button, index) => {
                        return <ButtonBoxView key={"index_" + index} iconUrl={button.iconUrl} text={button.text} onClickListener={() => this.click(button.text)} />
                    })
                }
            </CommonSlotView >
        )
    }
}
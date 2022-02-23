import React from 'react';
import { Upload } from 'antd';
import ProgressBarView from '@/components/ProgressBar/ProgressBarView'
import OperationType from '@/constant/OperationType'
import config from '@/axios/config';
import * as api from '@/axios/api';
import * as d3 from 'd3';

import "./UploadPannel.less";

const { Dragger } = Upload;

export default class UploadPannel extends React.Component {
    state = {
        originFileOb: {},
        operateState: this.props.operateState,
        errorMessage: this.props.initDone && this.props.intl.get("upload failed")
    }

    uploadDataToCloud = (formData) => {
        return new Promise((reslove, reject) => {
            api.uploadData(formData, config.url.uploadData).then((response) => {
                this.setState({ operateState: OperationType.GENERATING }); //加快页面交互的响应
                if (response.status === 'error') {
                    let { intl } = this.props
                    this.setState({
                        operateState: OperationType.FAILED,
                        errorMessage: intl.options.currentLocale === 'zh-CN' ? response.message_zh : response.message_en
                    })
                    reject();
                    return null;
                }
                reslove(response);
            }, fail => {
                this.setState({
                    operateState: OperationType.FAILED,
                    errorMessage: this.props.initDone && this.props.intl.get("upload failed")
                })
                reject();
            })
        })
    }

    processData = (response) => {
        if (!response.schema || !response.file_url || !response.file_name) {
            //this.props.updateOperation(OperationType.UPLOADED)//更新UI
            return
        }
        let schema = response.schema.fields
        let fileURL = config.url.uploadPrefix + response.file_url
        let fileName = response.file_name
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
                _that.props.uploadData(fileName, schema, data); //更新数据到redux中
                // _that.props.updateOperation(OperationType.UPLOADED)//更新UI
                _that.props.history.push('/data');
            }).catch(function (error) {
                console.log(error)
            })
    }

    onUploadChange = (info) => {
        /**** update UI ****/
        this.setState({
            operateState: OperationType.UPLOADIND,
        })
        if (info.event) {
            this.props.updateProgress(info.event.total, (info.event.total - info.event.loaded));
        }
        /**** update UI  the end ****/

        const { status } = info.file;
        if (status !== 'uploading') {
            let fileObj = info.file.originFileObj;
            let formData = new FormData();
            formData.append("file", fileObj);
            //step:1 upload data
            this.uploadDataToCloud(formData)
                //step 2:process data
                .then((response) => this.processData(response))
        }
    }
    beforeUpload = (info) => {
        return new Promise((resolve, reject) => {
            if (info.size <= 1048576 * 5) {
                return resolve(true);
            } else {
                this.setState({
                    operateState: OperationType.FILE_LARGE
                })
                reject(false);
            }
        });
    }

    getPannelClassName = () => {
        const { operateState } = this.state;
        switch (operateState) {
            case OperationType.BEFORE_UPLOAD:
                return "draggerPannelCommon yellowPannel";
            case OperationType.UPLOADED:
                return "pannelWithConvertType whitePannel";

            default:
                return "";
        }
    }

    isShowProgressbar = () => {
        const { operateState } = this.state;
        if (operateState === OperationType.UPLOADIND || operateState === OperationType.GENERATING) {
            return true;
        }
        return false;
    }


    render() {
        const { intl, initDone, generateProgress } = this.props;
        const { operateState } = this.state;


        /***
            上传失败或者文件过大的情况下，点击此按钮可以重新上传
            ***/
        const ClickToUploadView = () => {
            return (
                <div className="ClickToUpload">
                    <div ></div>
                    <p> {initDone && intl.get("Click to upload")}</p>
                </div>
            )
        };

        let PannelContentView;
        switch (operateState) {
            case OperationType.BEFORE_UPLOAD:
                PannelContentView = <>
                    {/* <div className="CSVFileImage">
                        <div className='csvIconWhite'></div>
                    </div> */}
                    <div className="uploadView">
                        <div className="uploadBtn">
                            <div></div>
                            {initDone && intl.get("Click to upload")}
                        </div>
                        <span>{initDone && intl.get("or drag a csv file here")} </span>
                    </div>
                </>
                break;
            case OperationType.UPLOADIND:
                PannelContentView = <div className="uploading">
                    <div className='uploadImage'></div>
                    <span>{initDone && intl.get("Uploading file")}</span>
                    <div className='dot'>...</div>
                </div>
                break;
            case OperationType.FAILED:
                PannelContentView = <>
                    <div className='errorFailImage'>
                        <div className="iconFailed"></div>
                        <p className="hintText">{this.state.errorMessage}</p>
                    </div>
                    <ClickToUploadView />
                </>
                break;
            case OperationType.FILE_LARGE: //large than 5MB
                PannelContentView = <>
                    <div className="largeFileView">
                        <div></div>
                        <span>{initDone && intl.get("larger than 5MB")}</span>
                    </div>
                    <ClickToUploadView />
                </>
                break;
            default:
                break;
        }

        return (
            <div className={this.getPannelClassName()} style={{ position: 'relative' }}>
                <ProgressBarView percent={generateProgress} isActive={this.isShowProgressbar()} />
                <div style={{ flex: 1 }}>
                    <Dragger
                        beforeUpload={this.beforeUpload}
                        onChange={this.onUploadChange}
                        showUploadList={false}
                        accept=".csv, .json">
                        <div className="pannelContent">
                            {
                                PannelContentView
                            }
                        </div>
                    </Dragger>
                </div>
            </div >
        )
    }
}
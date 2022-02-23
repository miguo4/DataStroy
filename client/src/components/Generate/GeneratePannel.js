import React, { Suspense } from 'react'
import { Spin } from 'antd';
import OperationType from '@/constant/OperationType'
import ConvertType from '@/constant/ConvertType'
import ConvertForms from '@/constant/config'
import Fact from '@/model/fact'
import ToFactsheet from '@/components/Generate/ToFactsheet/ToFactsheet'
import Color from '@/constant/Color'
import ProgressBarView from '@/components/ProgressBar/ProgressBarView'
import config from '@/axios/config';
import * as api from '@/axios/api';
import './GeneratePannel.less';


export default class GeneratePannel extends React.Component {

    state = {
        operateState: this.props.operateState,
        convertingType: ConvertForms[0]
    }

    UNSAFE_componentWillReceiveProps(nextProps) {
        if (nextProps.operateState !== this.props.operateState) {
            this.setState({
                operateState: nextProps.operateState
            })
        }
    }
    generate = (url) => {
        return new Promise(async (resolve, reject) => {
            let fileName = this.props.fileName;
            this.props.generateStory([], [], '');
            this.props.updateProgress(this.props.maxStoryLength, this.props.maxStoryLength);//reset progress bar
            //setTimeout 8s
            let max_iteration = 8,
                count = max_iteration;//inital

            let timer = setInterval(() => {
                if (count === 0) {
                    clearInterval(timer)
                    this.setState({
                        operateState: OperationType.GENERATED
                    })
                    this.props.history.push('/edit')
                }
                count--;
                this.props.updateProgress(max_iteration, count < 0 ? 0 : count);
            }, 1500)

            const { storyParameter } = this.props;

            let data = {
                file_name: fileName,
                max_story_length: storyParameter.maxStoryLength
            }
            const response = await api.generate(url, data)
            clearInterval(timer);
            if (response.data.fail) {
                this.setState({
                    operateState: OperationType.FAILED,
                    errorMessage: response.data.fail
                })
                reject();
            }
            if (response.data.error) {
                this.setState({
                    operateState: OperationType.FAILED,
                    errorMessage: response.data.error
                })
                reject();
            }
            this.props.updateProgress(max_iteration, 0);//100%
            this.setState({
                operateState: OperationType.GENERATED
            })
            resolve(response)
        })
    }

    getPannelClassName = () => {
        const { operateState } = this.state;
        switch (operateState) {
            case OperationType.UPLOADED:
                return "pannelWithConvertType whitePannel"
            case OperationType.GENERATING:
            case OperationType.GENERATED:
                return "draggerPannelCommon whitePannel"
            default:
                return "";
        }
    }

    isShowProgressbar = () => {
        const { operateState } = this.state
        if (operateState === OperationType.GENERATING) {
            return true;
        }
        return false;
    }

    clickGenerate = (typeForm) => {
        this.setState({
            convertingType: typeForm,
            operateState: OperationType.GENERATING
        })
        let type = typeForm.name
        this.generate(config.url.generate).then(response => {
            const facts = response.data.story.facts;
            let tempFacts = [];
            switch (type) {
                default:
                    for (let factDict of facts) {
                        let fact = new Fact(
                            factDict['type'],
                            factDict['measure'],
                            factDict['subspace'],
                            factDict['groupby'],
                            factDict['focus'],
                            factDict['parameter'],
                            "", // chart
                            factDict['score'],
                            factDict['information'],
                            factDict['significance']
                        )
                        tempFacts.push(fact);
                    }
                    this.props.generateStory(tempFacts.slice(), [
                        "none",
                        "similarity",
                        "similarity",
                        "similarity",
                        "similarity",
                        "similarity"
                    ], 1);
                    this.props.history.push('/edit')
                    break;
            }
        })
    }

    render() {
        const { intl, initDone, generateProgress } = this.props;
        const { operateState, convertingType } = this.state


        const ConvertingArrow = ({ operateState }) => {
            return (<div className="arrowLineDiv" >
                <p> {this.props.generateProgress + "%"}</p>
                <div className="arrowLine"></div>
                {
                    operateState === OperationType.GENERATED ?
                        <p> {initDone && intl.get("Success")}</p>
                        :
                        <p> {initDone && intl.get("Coverting")}</p>
                }
            </div>)
        }

        const FileNameView = ({ fileName }) => {
            return <div className='CSVFileImage'>
                <div className='csvIconBlack'></div>
                <span className="fileName">{fileName}</span>
            </div>
        }

        let PannelContentView;
        switch (operateState) {
            case OperationType.UPLOADED:
                PannelContentView = <>
                    <div style={{ height: "245px", flex: 1 }}>
                        <div className='pannel-box'>
                            <FileNameView fileName={this.props.fileName} />
                        </div>
                    </div>
                    <div className='ConvertFormsDiv' style={{ columnCount: Math.ceil(ConvertForms.length / 2) }}>
                        {
                            ConvertForms.map((type, idx) => {
                                return <div className='convert-box'
                                    key={idx}
                                    style={{ height: ConvertForms.length === 1 ? "100%" : "50%", backgroundColor: Color.CONVERT[idx] }}
                                    onClick={() => this.clickGenerate(type)}>
                                    <div className='icon'
                                        style={{ backgroundImage: `url(${type.iconUrl})` }}
                                    />
                                    <span>{initDone && intl.get(`To${type.name}`)}</span>
                                </div>
                            })
                        }
                        {
                            ConvertForms.length !== 1 && ConvertForms.length % 2 !== 0 ?
                                <div style={{ height: "50%", visibility: "none", backgroundColor: "transparent" }}></div>
                                : null
                        }
                    </div>
                </>
                break;
            case OperationType.GENERATING:
                PannelContentView = <div style={{ height: "245px", flex: 1 }}>
                    <div className='pannel-box'>
                        <div style={{ display: 'flex' }}>
                            <FileNameView fileName={this.props.fileName} />
                            <div className='VHCenter'>
                                <ConvertingArrow operateState={operateState} {...this.props} />
                                <div className='CSVFileImage'>
                                    <div className='GenerateIcon'
                                        style={{ backgroundImage: `url(${convertingType.generateIconUrl})` }}
                                    />
                                    <span className='fileName'>{initDone && intl.get(`To${convertingType.name}`)}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div >
                break;
            case OperationType.PUBLISHED:
                const Loading = () => {
                    return (<div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', marginTop: "50px" }}>
                        <Spin />
                    </div>)
                }
                //dynamic load the supported button view according to the convert type
                let GeneratedPannel;
                switch (convertingType.name) {
                    case ConvertType.FACTSHEET:
                        GeneratedPannel = <ToFactsheet reGnerate={this.clickGenerate}  {...this.props} />
                        break;
                    default:
                        break;
                }

                PannelContentView = <div style={{ height: "245px", flex: 1 }}>
                    <div className='pannel-box'>
                        <div style={{ display: 'flex', flexDirection: "column", alignItems: "center", height: "100%" }}>
                            <Suspense fallback={<Loading />}>
                                {GeneratedPannel}
                            </Suspense>
                        </div>
                    </div>
                </div >
                break;
            default:
                break;
        }
        return <div className={this.getPannelClassName()}>
            <ProgressBarView percent={generateProgress} isActive={this.isShowProgressbar()} />
            {
                PannelContentView
            }
        </div>
    }
}
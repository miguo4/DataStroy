import React, { Component } from 'react'
import { Input } from 'antd';
import './TalkBottom.less'
import Artyom from 'artyom.js';

let timer = 0
let artyom = new Artyom();

const VoiceView = ({ isSentenceParsing, sentence, initDone, intl }) => {
    return (
        <div className='voice-active' >
            <div className='voice-icon' ></div>
            {
                isSentenceParsing && <div className='gif' ></div>
            }
            <span>{sentence || initDone && intl.get("voiceHint")}</span>
        </div>
    )
}

export default class TalkBottom extends Component {

    constructor(props) {
        super(props);
        this.voiceStart = false;
        this.state = {
            enableVoice: false,
            enableInput: false,
            enableEdit: false,
            isMouseMove: false,
            isSentenceParsing: false,
            sentence: '',
            inputValue: '',
            //追加语音输入的文字
            appendSen: "",
            //语音输入的设置项
            settings: {
                continuous: false, // Don't stop never because i have https connection
                onResult: this.textToInput,
                onStart: function () {
                },
                onEnd: function () {
                }
            }
        };
        //初始化语音设置
        this.UserDictation = artyom.newDictation(this.state.settings);
    }


    componentDidMount() {
        window.addEventListener("mousemove", () => {
            const { isMouseMove } = this.state;
            !isMouseMove && this.setState({
                isMouseMove: true
            })
        })
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.isClosePannel) {
            this.setState({
                enableVoice: false,
                enableInput: false,
                enableEdit: false,
                sentence: '',
                isSentenceParsing: false
            });
            // console.log(this.voiceStart);
            this.voiceStart = false;
            this.isChrome() && this.UserDictation.stop();
            this.props.closePannel(false)
        }
    }


    componentWillUnmount() {
        window.removeEventListener("mousemove", () => { })
    }
    isChrome = () => {
        return navigator.userAgent.indexOf("Chrome") !== -1
    }
    //将语音输入的文字在输入框中显示
    textToInput = (text, temporal) => {
        if (text !== "") {
            this.setState({
                sentence: this.state.appendSen + text
            });
            if (this.stopVoice) {
                clearTimeout(this.stopVoice);
                //this.voiceStart=false;
            }
        } else {
            this.setState({
                appendSen: this.state.sentence
            });
            //使用一个变量指向当前的this，以防访问不到
            let talkBottom = this;
            //3秒之后执行stop语音的操作,如果检测到有输入的话，那么会帮忙终止掉这个操作。
            this.stopVoice = setTimeout(function () {
                if (talkBottom.voiceStart) {
                    talkBottom.voiceStart = false;
                    talkBottom.UserDictation.stop();
                    talkBottom.props.generate(talkBottom.state.sentence);
                    talkBottom.setState({
                        isSentenceParsing: false,
                        enableVoice: false,
                        sentence: ""
                    })
                }
            }, 1500);
        }
    };

    enableVoice = () => {
        this.setState({ enableVoice: true })
        let { isSentenceParsing } = this.state;
        if (!isSentenceParsing && !this.voiceStart) {
            this.voiceStart = true;
            this.UserDictation.start();
            this.setState({
                appendSen: this.state.sentence,
            });
        }
        this.setState({
            isSentenceParsing: !this.state.isSentenceParsing
        });
    };


    onPressEnter = () => {
        this.setState({
            enableVoice: false,
            enableInput: false
        });
        this.props.generate(this.state.inputValue)
    };
    handleChange = (e) => {
        this.setState({
            inputValue: e.target.value
        })
    };
    enableEdit = () => {
        this.updateEdit(true)
    }
    stopEdit = () => {
        this.updateEdit(false)
    }
    updateEdit = (isCanEdit) => {
        this.setState({
            enableEdit: isCanEdit
        })
        this.props.enableEdit(isCanEdit)
    }
    goBack = () => {
        const { isEditPage } = this.props
        if (isEditPage) {
            this.props.history.push('/data')
        } else {
            this.props.history.push('/edit')
        }
    }


    render() {
        const { initDone, intl, isEditPage } = this.props
        const { enableVoice, enableInput, isMouseMove, sentence, isSentenceParsing, inputValue, enableEdit } = this.state
        //console.log("isSentenceParsing", isSentenceParsing);
        const TooBarView = () => {
            return (
                <div className='tool-bar'>
                    <button className='upload' onClick={() => this.props.history.push('/')}></button>
                    {
                        this.isChrome() && <button className='voice' onClick={this.enableVoice} ></button>
                    }
                    <button className='input' onClick={() => this.setState({ enableInput: true })}></button>

                    <button className={isEditPage ? "toDatabase" : 'toVis'} onClick={() => this.goBack()}></button>
                    {
                        isEditPage && <>
                            <button className='edit' onClick={this.enableEdit}></button>
                        </>
                    }
                </div>
            )
        }
        return (
            <div className='bottom-box' style={{ width: enableVoice || enableInput ? "100%" : "" }}>
                {
                    enableVoice ? <VoiceView isSentenceParsing={isSentenceParsing} sentence={sentence} initDone={initDone} intl={intl} />
                        :
                        enableInput ?
                            <div className='input-box'>
                                <div className='input-icon' ></div>
                                <div className='input-active' >
                                    <Input placeholder={initDone && intl.get("inputHint")}
                                        value={inputValue}
                                        onChange={(e) => this.handleChange(e)}
                                        onPressEnter={this.onPressEnter}
                                    ></Input>
                                </div>
                            </div>
                            :
                            enableEdit ?
                                <div className='edit-box'>
                                    <div className='edit-icon'></div>
                                    <div className='exit-active'>
                                        <div className='box' onClick={this.stopEdit}>
                                            <span>Exit</span>
                                            <div className='exit-icon'></div>
                                        </div>
                                    </div>
                                </div>
                                :
                                isMouseMove && <TooBarView />
                }
            </div >
        )
    }
}
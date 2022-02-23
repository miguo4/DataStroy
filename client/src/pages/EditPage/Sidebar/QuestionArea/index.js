import React, { Component } from 'react'
import "./index.less"
import { Input } from 'antd';
import { Button } from 'antd';
import generate from "@/images/question-area-icon/right.png"


export default class QuestionArea extends Component {
    constructor(props) {
        super(props);
        this.state = {
            sentence: "",
        };
    }
    inputSentenceChange = (e) => {
        this.setState({
            sentence: e.target.value
        })
    }
    handleSearchClick = () => {
        this.props.handleInputBtnClick(this.state.sentence);
    };
    change = (event) => {
        this.props.updateApiType(event.target.value)
    }
    render() {
        const { initDone, intl } = this.props
        const { sentence } = this.state
        return (
            <div className="question-area">
                <div className="question-area-input">
                    <div className='api'>
                        <select onChange={this.change} defaultValue={"talk"}>
                            <option value=''>talk</option>
                            <option value='nl4dv'>nl4dv</option>
                        </select>
                    </div>
                    <Input
                        className="question-area-input-box"
                        placeholder={initDone && intl.get("inputHint")}
                        onChange={(e) => this.inputSentenceChange(e)}
                        value={sentence}
                    />
                    <Button
                        className="question-area-input-btn"
                        icon={<Generate />}
                        onClick={this.handleSearchClick}>
                    </Button>
                </div>
            </div>
        )
    }
}
function Generate() {
    return (
        <img src={generate} alt="generate img" className="img-generate" />
    );
}

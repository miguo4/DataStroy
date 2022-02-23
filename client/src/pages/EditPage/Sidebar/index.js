import React, { Component } from 'react'
import QuestionArea from "./QuestionArea"
import SchemaPreview from "./SchemaPreview"
import "./index.less"
export default class Siderbar extends Component {
    constructor(props) {
        super(props);
    }
    handleInputChange = (sentence) => {
        this.props.handleInputChange(sentence);
    };
    //当点击菜单项时调用函数
    handleMenuClick = (item, key, keyPath, domEvent) => {
        this.props.handleMenuClick(item, key, keyPath, domEvent);
    };
    //点击输入按钮
    handleInputBtnClick = (sentence) => {
        //打印输入框中的语句
        this.props.handleInputBtnClick(sentence);
    };
    render() {
        const { initDone, intl } = this.props
        return (
            <div className="siderbar">
                <QuestionArea
                    initDone={initDone}
                    intl={intl}
                    handleInputBtnClick={this.handleInputBtnClick}
                    handleInputChange={this.handleInputChange}
                    className="siderbar-question-area" />
                <SchemaPreview
                    initDone={initDone}
                    intl={intl}
                    fileName={this.props.fileName}
                    handleMenuClick={this.handleMenuClick}
                    tableSchema={this.props.tableSchema}
                    className="siderbar-schema-preview" />
            </div>
        )
    }
}

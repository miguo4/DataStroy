import React from 'react';
import { Select } from 'antd';
import LocaleConfig from '../../../constant/LocaleConfig';
import './LocaleConfigView.less';
const { Option } = Select;

export default class LocaleConfigView extends React.Component {
    getLocal = (currentLang) => {
        if (currentLang === 'zh-CN') { //zh-CN
            return LocaleConfig.Chinese
        } else {
            return LocaleConfig.English
        }
    }
    onChange = (value) => {
        this.props.onChangeLocaleListener(this.getLocal(value))
    }
    render() {
        const { currentLocale } = this.props
        let lang;
        if (currentLocale) {
            if (currentLocale === 'zh-CN') {
                lang = "中 文"
            } else {
                lang = "EN"
            }
        }
        return (
            <Select className="LocaleDiv" defaultValue={lang} bordered={false} value={lang} onChange={this.onChange}>
                <Option key="en-US">EN</Option>
                <Option key="zh-CN">中 文</Option>
            </Select>
        )
    }
}
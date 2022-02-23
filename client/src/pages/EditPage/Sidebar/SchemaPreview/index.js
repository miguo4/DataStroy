import React, { Component } from 'react'
import "./index.less"
import { Menu } from 'antd';
const { SubMenu } = Menu;

import numerical from "@/images/schema-icon/numerical.svg"
import geographical from "@/images/schema-icon/geographical.svg"
import temporal from "@/images/schema-icon/temporal.svg"
import categorical from "@/images/schema-icon/categorical.svg"
import { Modal, Button } from 'antd';
import close from "@/images/schema-icon/close.svg"


export default class SchemaPreview extends Component {
    constructor(props) {
        super(props);
        //要改为获取父组件的数据
        // mock oriData
        this.initData(this.props.tableSchema);

        this.state = {
            isModalVisible: false
        }

    }
    initData = (data) => {
        const { initDone, intl } = this.props;
        //获取表格的对应的schema，构建treeData
        let schema = data["schema"];
        //根据数据类型进行分组
        let typeGroup = { "Numerical": [], "Geographical": [], "Categorical": [], "Temporal": [] };
        for (let i = 0; i < schema.length; i++) {
            let type = schema[i].type;
            let field = schema[i].field;
            switch (type) {
                case "categorical":
                    typeGroup.Categorical.push(field);
                    break;
                case "temporal":
                    typeGroup.Temporal.push(field);
                    break;
                case "numerical":
                    typeGroup.Numerical.push(field);
                    break;
                case "geographical":
                    typeGroup.Geographical.push(field);
                    break;
            }
        }
        let listParent = [];
        let tempIcon;
        let tempTitle = "";
        for (let typeKey in typeGroup) {
            switch (typeKey) {
                case "Categorical":
                    tempIcon = <Categorical />;
                    tempTitle = initDone && intl.get("dataTypeCate");
                    break;
                case "Temporal":
                    tempIcon = <Temporal />;
                    tempTitle = initDone && intl.get("dataTypeTem");
                    break;
                case "Numerical":
                    tempIcon = <Numerical />;
                    tempTitle = initDone && intl.get("dataTypeNum");
                    break;
                case "Geographical":
                    tempIcon = <Geographical />;
                    tempTitle = initDone && intl.get("dataTypeGeo");
                    break;
            }
            //先构建子菜单
            let listChild = [];
            let tempChild = typeGroup[typeKey];
            console.log(tempChild);
            if (tempChild.length!==0) {
                //如果子菜单不为空，则添加进菜单列表
                for (let i = 0; i < tempChild.length; i++) {
                    listChild.push(
                        <Menu.Item key={tempChild[i]}>{tempChild[i]}</Menu.Item>
                    )
                }
                listParent.push(
                    <SubMenu key={typeKey} icon={tempIcon} title={tempTitle}>
                        {listChild}
                    </SubMenu>
                );
            }
        }
        this.listTable = listParent;
    };
    //点击某一列数据时将弹出语句卡片
    handleClick = (item, key, keyPath, domEvent) => {
        this.props.handleMenuClick(item, key, keyPath, domEvent);
        //显示弹出框
        this.setState(
            {
                isModalVisible: true
            }
        );
    };
    //关闭弹出的卡片
    handleCancel = () => {
        //关闭弹出框
        this.setState(
            {
                isModalVisible: false
            }
        );
    };
    render() {
        return (
            <div className="schema-preview">
                <h3>{this.props.fileName}</h3>
                <div className="schema-preview-divider"> </div>
                <Menu
                    className="schema-preview-menu"
                    onClick={this.handleClick}
                    mode="inline">
                    {this.listTable}
                </Menu>
                <Modal title="Schema type"
                    visible={this.state.isModalVisible}
                    footer=""
                    centered={true}
                    className="schema-preview-card"
                    closeIcon={<CloseCard />}
                    onCancel={this.handleCancel}>
                    <div className="schema-preview-card-div">
                        <div className="schema-preview-card-question">
                            <div className="card-question-content">question1</div>
                            <Button className="card-question-btn"> </Button>
                        </div>
                        <div className="schema-preview-divider"> </div>
                        <div className="schema-preview-card-question">
                            <div className="card-question-content">question2</div>
                            <span><Button className="card-question-btn"> </Button></span>
                        </div>
                        <div className="schema-preview-divider"> </div>
                    </div>
                </Modal>
            </div>
        )
    }
}
function Numerical() {
    return (
        <img className="schema-icon-pic" src={numerical} alt="Numerical img" />
    )
}
function Geographical() {
    return (
        <img className="schema-icon-pic" src={geographical} alt="Geographical" />
    )
}
function Temporal() {
    return (
        <img className="schema-icon-pic" src={temporal} alt="Temporal" />
    )
}
function Categorical() {
    return (
        <img className="schema-icon-pic" src={categorical} alt="Categorical" />
    )
}
function CloseCard() {
    return (
        <img className="schema-icon-close" src={close} alt="close card img" />
    )
}


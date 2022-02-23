import React, { Component } from 'react'
import { Table, Tooltip } from 'antd';
import Color from '@/constant/Color'
import FieldType from '@/constant/FieldType'
import './TableView.less'

export default class TableView extends Component {
    tableRef = React.createRef()

    state = {
        tableHeight: 0
    }

    componentDidMount() {
        this.updateTableHeight()
        this.onResize()
    }
    onResize = () => {
        window.addEventListener('resize', () => {
            this.updateTableHeight()
        })
    }

    updateTableHeight = () => {
        if (this.tableRef.current) {
            const { clientHeight } = this.tableRef.current
            if (clientHeight !== this.state.tableHeight) {
                this.setState({
                    tableHeight: clientHeight
                })
            }
        }
    }

    getColumnIcon = (type) => {
        return (<div className={`field-icon field-${type}`} ></div>)
    }

    clickTitle = (columnName) => {
        this.props.updateColumnName(columnName)
    }

    editName = (e) => {
        let node = e.target
        node && node.setAttribute("contentEditable", true)
    }


    constructColumns = (schema) => {
        return schema.map(s => {
            let _s = {
                ...s,
                title:
                    <div className={`title ${s.type}`} onClick={() => this.clickTitle(s.field)} onDoubleClick={this.editName}>
                        {
                            this.getColumnIcon(s.type)
                        }
                        <p> {s.field}</ p>
                    </div>,
                dataIndex: s.field,
                ellipsis: true,
                filtered: true,
                align: 'center',
                className: s.type,
            }
            //add filter
            if (s.type === FieldType.CATEGORICAL || s.type === FieldType.TEMPORAL) {
                _s['filters'] = s.values.map(d => {
                    return {
                        text: d,
                        value: d
                    }
                })
                _s['onFilter'] = (value, record) => {
                    return record[s.field] && record[s.field].includes(value)
                }
            }
            //add sorter
            if (s.type !== FieldType.CATEGORICAL && s.type !== FieldType.TEMPORAL && s.type !== 'ID') {
                _s['sorter'] = (a, b) => {
                    return a[s.field] - b[s.field]
                }
            }
            return _s
        })
    }

    addKey = (data) => {
        const dataSource = data.slice(0, data.length - 1)
        return dataSource.map((d, i) => {
            return {
                ...d,
                key: i
            }
        })
    }
    // handleTableChange = (pagination, filters, sorter) => {
    //     console.log("filters",filters);     
    // };
    render() {
        const { data, schema } = this.props
        const { tableHeight } = this.state


        let rowHeight = tableHeight - 63 - 32 - 32
        let pageSize = parseInt(rowHeight / 35)

        return (
            <div className="TableView" ref={this.tableRef}>
                <Table
                    bordered={true}
                    dataSource={this.addKey(data)}
                    columns={this.constructColumns(schema)}
                    pagination={{ pageSize, showSizeChanger: false }}
                    onChange={this.handleTableChange}
                />
            </div>
        )
    }
}
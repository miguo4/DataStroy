import React, { Component } from 'react'
import { genFactSentence } from '@/sentencer/index'
import CalliopeChart from './CalliopeChart'
import { hightlight } from '@/tool/helper'
import * as d3 from 'd3'
import _ from 'lodash';
import './AnsweredFacts.less'


let testLayout = [1, 2, 3, 4, 5]
const defaultNum = testLayout[4]

let visNodes = new Map()
let captionNodes = new Map()
const maxNum = 5;

export default class AnsweredFacts extends Component {

    renderLayout = null

    constructor(props) {
        super(props);
        this.state = {
            renderNum: defaultNum,
            count: maxNum,
            clientWidth: 0,
            clientHeight: 0,
            facts: this.props.facts,
            containerSize: this.props.containerSize
        }
    }

    componentDidMount() {
        this.computeSizeAndRenderCharts()
    }
    componentWillReceiveProps(nextProps) {
        let newContainerW = nextProps.containerSize.width,
            newContainerH = nextProps.containerSize.height

        let { width, height } = this.state.containerSize
        //console.log("componentWillReceiveProps", nextProps.containerSize, this.state.containerSize);
        //update container size
        if (newContainerW !== width || newContainerH !== height) {
            this.setState({
                containerSize: {
                    width: newContainerW,
                    height: newContainerH
                }
            })
        }
        //update facts 
        if (nextProps.isUpdateLayout) {
            this.setState({
                facts: nextProps.facts
            }, () => {
                this.computeSizeAndRenderCharts()
            })
        }
    }

    componentDidUpdate() {
        //屏幕尺寸改变 需要更新
        let { width, height } = this.state.containerSize

        let cachedContainerSize = this.state.facts[0].preContainerSize
        if (cachedContainerSize) {
            if (cachedContainerSize.width !== width || cachedContainerSize.height !== height) {
                let facts = _.cloneDeep(this.state.facts)
                facts[0].preContainerSize = this.state.containerSize//update containerSize size 
                this.setState({
                    facts
                }, () => {
                    this.computeSizeAndRenderCharts()
                })
            }
        }

        //启动编辑后触发的更新
        if (this.props.isEdit) {
            this.renderCharts()
        }
    }

    /*
     *
     fact.width 记录的是计算的chart的宽度；fact.height记录的是计算的chart的高度
     批量一次更新后，先生成calliope-chart的dom,
     然后做缩放
     */
    computeSizeAndRenderCharts = () => {
        let facts = _.cloneDeep(this.state.facts)
        let newFacts = facts.map((fact, index) => {
            if (!captionNodes.get(fact.id)) return fact
            let captionNode = captionNodes.get(fact.id).current
            let visWidth = 0, visHeight = 0
            let captionH = 0;

            if (captionNode) {
                captionH = captionNode.clientHeight
            }
            if (this.renderLayout && this.renderLayout[index]) {
                let { x0, x1, y0, y1 } = this.renderLayout[index]
                visWidth = x1 - x0
                visHeight = y1 - y0 - captionH
            }

            if (visWidth === 0 || visHeight === 0) return fact
            fact.width = visWidth
            fact.height = visHeight
            fact.captionH = captionH
            //preContainerSize 只记在第一个数组里就可以了
            if (index === 0) {
                fact.preContainerSize = this.props.containerSize
            }
            return fact
        })

        this.setState({
            facts: newFacts
        }, () => {
            this.renderCharts()
        })
    }
    //由于calliope-chart异步返回,因此做了1000ms的延迟才可以获取visChart
    renderCharts = () => {
        setTimeout(() => {
            this.batchUpdateSvg()
        }, 1000)
    }

    batchUpdateSvg = () => {
        let facts = _.cloneDeep(this.state.facts)
        // console.log("newFacts", facts);
        facts.map(fact => {
            if (!visNodes.get(fact.id)) return fact
            let visNode = visNodes.get(fact.id).current
            if (visNode) {
                //console.log("visNodes", visNode, visNodes.get(fact.id));
                this.updateSvg(visNode, fact.width, fact.height)
            }
            return fact
        })
    }


    /*更新:
         可见状态
         设置缩放
     */
    updateSvg = (visNode, visWidth, visHeight) => {
        if (visNode) {
            let h_Margin = 15
            let visH = visHeight - h_Margin
            // let scaleX = visWidth / 640,
            //     scaleY = visHeight / 640;
            let scale = Math.min(visWidth, visH) / 640
            let marginRotio = 0.9
            let visChart = visNode.children && visNode.children[0]
            //console.log("updateSvg visNode", visNode, visWidth, visHeight,scale);
            if (visChart) {
                visChart.setAttribute("style", `transform:scale(${scale * marginRotio});visibility:"visible"`)
                visChart.onmouseenter = () => {
                    visChart.setAttribute("style", `transform:scale(${scale * marginRotio});border:${this.props.isEdit ? '1px dashed grey' : ' '} `)
                }
                visChart.onmouseleave = () => {
                    visChart.setAttribute("style", `transform:scale(${scale * marginRotio})`)
                }
            }
        }
    }


    _renderedFacts = (facts) => {
        const { renderNum, count } = this.state
        return facts.slice(0, renderNum >= count ? count : renderNum)
    }



    weightAdapter = (data, columnNum) => {
        let innerNum = data.children.length
        let weightTable = []
        switch (columnNum) {
            case 1:
                weightTable = [1]
                if (innerNum === 2) {
                    weightTable = [3, 2]
                } else if (innerNum === 3) {
                    weightTable = [3, 1.2, 0.8]
                }
                break;
            case 2:
                weightTable = [1]
                if (innerNum === 2) {
                    weightTable = [4, 3]
                } else if (innerNum === 3) {
                    weightTable = [6, 3, 2]
                }
                break;
            case 3:
                weightTable = [1]
                if (innerNum === 2) {
                    weightTable = [3, 2]
                } else if (innerNum === 3) {
                    weightTable = [3, 1.2, 0.8]
                }
                break;
            case 4:
                weightTable = [1]
                if (innerNum === 2) {
                    weightTable = [3, 2]
                } else if (innerNum === 3) {
                    weightTable = [4, 3, 2]
                }
                break;
            default:
                break;
        }
        return {
            "children": data.children.map((fact, index) => {
                return {
                    ...fact,
                    significance: weightTable[index]
                }
            })
        }
    }

    change = (event) => {
        this.setState({
            renderNum: event.target.value
        })
    }

    getTreemap = (width, height, data) => {
        let treemap = d3.treemap()
            .tile(d3.treemapResquarify.ratio(1))
            .size([width, height])
            .padding(3)
            .round(true)
            (d3.hierarchy(data)
                .sum(d => d.significance)
            )
        return treemap
    }

    sort = (data) => {
        return data.sort((a, b) => b.significance - a.significance)
    }

    setRef = (id) => {
        visNodes.set(id, React.createRef())
        return visNodes.get(id)
    }
    setCaptionRef = (id) => {
        captionNodes.set(id, React.createRef())
        return captionNodes.get(id)
    }
    endEdit = (visId, index) => {
        let captionNode = captionNodes.get(visId).current
        let { cachedQA, QAID } = this.props
        let newCachedQA = _.cloneDeep(cachedQA)
        newCachedQA[QAID].facts[index].script = captionNode.innerHTML
        this.props.saveCachedDecomposedQA(newCachedQA)
    }

    deleteCard = (index) => {
        let { cachedQA, QAID } = this.props
        let newCachedQA = _.cloneDeep(cachedQA)
        let parentId = QAID
        newCachedQA[parentId] && newCachedQA[parentId].facts.splice(index, 1)
        if (newCachedQA[parentId] && newCachedQA[parentId].facts.length === 0) {
            newCachedQA.splice(parentId, 1)
        }
        this.props.saveCachedDecomposedQA(newCachedQA)
    }

    render() {

        let { columnNum, isEdit, QAID, schema, data } = this.props
        let { containerSize } = this.state
        let { facts } = this.state
        let renderData = {
            children: this._renderedFacts(this.sort(facts))
        }
        let { width, height } = containerSize//屏幕尺寸改变后改变的参数
        this.renderLayout = this.getTreemap(width, height, this.weightAdapter(renderData, columnNum)).leaves()
        //console.log("facts render", this.props.QAID, facts, this.props.facts, this.renderLayout);

        return (
            <div className='inner-auto-layout' >
                {
                    this.renderLayout && this.renderLayout.map((layout, index) => {
                        const fact = layout.data
                        const { x0, x1, y0, y1 } = layout

                        let script = fact.script ? fact.script : genFactSentence(fact) || " "
                        fact.generatedScript = script
                        // console.log("render////", QAID, index, fact, layout);
                        return <div style={{ position: 'absolute', left: x0, top: y0, width: x1 - x0, height: y1 - y0 }}>
                            <div className='chart-card'>
                                {
                                    isEdit && <div className='delete' onClick={() => this.deleteCard(index)}></div>
                                }
                                <div className='wrapper'>
                                    <div className='vis-box' style={{ height: `calc(100% - ${fact.captionH}px)` }}>
                                        <div className='bound-box' id={fact.id} ref={this.setRef(fact.id)}
                                            //style={{ width: fact.width, height: fact.height, backgroundColor: "red" }}
                                        >
                                            <CalliopeChart schema={schema} fact={fact} data={data} />
                                        </div>
                                    </div>
                                    <div className='caption' contentEditable={isEdit} suppressContentEditableWarning ref={this.setCaptionRef(fact.id, index)} onBlur={() => this.endEdit(fact.id, index)}
                                        //title={script}
                                        dangerouslySetInnerHTML={{ __html: hightlight(fact) }}
                                    ></div>
                                </div>
                            </div>
                        </div >
                    })
                }
            </div >
        )
    }
}
import React, { Component } from 'react'
import AnsweredFacts from '../Layout/ChartCard/AnsweredFacts'
import ErrorView from '@/components/ErrorView/ErrorView'
import uuidv4 from 'uuid/v4';
import _ from 'lodash'
import './layout.less'

// const defaultNum = 1
// const defaultSubNum = 5

let subTitleNodes = new Map()

export default class LayoutView extends Component {
    titleRef = React.createRef();
    debounceTimer = null
    containerNodes = {
        width: 0,
        height: 0
    }
    // state = {
    //     num: this.props.decomposedQA.length,
    //     subNum: defaultSubNum
    // }
    // change = (event) => {
    //     this.setState({
    //         num: event.target.value
    //     })
    // }
    // subchange = (event) => {
    //     this.setState({
    //         subNum: event.target.value
    //     })
    // }

    componentDidMount() {
        this.onResize()
    }
    componentDidUpdate() {
        if (this.preContainerNodes && this.containerNodes) {
            if (this.preContainerNodes.width !== this.containerNodes.width || this.preContainerNodes.height !== this.containerNodes.height) {
                this.forceUpdate()
            }
        }
    }
    onResize = () => {
        window.addEventListener('resize', () => {
            if (this.debounceTimer) clearTimeout(debounceTimer)
            setTimeout(() => {
                this.forceUpdate()
            }, 1000)
        })
    }
    setFactId = (facts, index) => {
        let _facts = _.cloneDeep(facts).map(fact => {
            return {
                ...fact,
                id: `${index}QA${uuidv4()}`
            }
        })
        return _facts
    }

    fullscreen = () => {
        let element = document.documentElement;
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.mozRequestFullScreen) {   // 兼容火狐
            element.mozRequestFullScreen();
        } else if (element.webkitRequestFullscreen) {    // 兼容谷歌
            element.webkitRequestFullscreen();
        } else if (element.msRequestFullscreen) {   // 兼容IE
            element.msRequestFullscreen();
        }
    }
    //re-order the array so the "cards" read left-right
    reorder = (arr, columns) => {
        const cols = columns;
        const out = [];
        let col = 0;
        while (col < cols) {
            for (let i = 0; i < arr.length; i += cols) {
                let _val = arr[i + col];
                if (_val !== undefined)
                    out.push(_val);
            }
            col++;
        }
        return out
    }
    endEdit = (index) => {
        let _nodes = subTitleNodes.get(index).current
        if (_nodes) {
            let { cachedQA } = this.props
         if( cachedQA[index] )
          {
            cachedQA[index].question = _nodes.innerHTML
          }
            this.props.saveCachedDecomposedQA(cachedQA)
        }
    }
    setSubTitleRef = (index) => {
        subTitleNodes.set(index, React.createRef())
        return subTitleNodes.get(index)
    }
    setContainerRef = (e) => {
        if (e) {
            let subTitleH = 55
            this.containerNodes = { width: e.clientWidth, height: e.clientHeight - subTitleH }
        }
    }

    endTitleEdit = () => {
        let _nodes = this.titleRef.current
        if (_nodes) {
            let newtTitle = _nodes.innerHTML
            if (newtTitle !== this.props.editedTitle) {
                this.props.editTitle(newtTitle)
            }
        }
    }
    export = () => {
        window.print()
    }
    getTitle = () => {
        const { askedQuestion, editedTitle } = this.props
        let titleValue = editedTitle ? editedTitle : askedQuestion
        return titleValue.slice(0, 1).toUpperCase() + titleValue.slice(1)
    }

    isCanGetSize = () => {
        this.preContainerNodes = {
            width: 0,
            height: 0
        }
        if (this.containerNodes) {
            if (this.containerNodes.width !== 0 && this.containerNodes.height !== 0) {
                this.preContainerNodes = _.cloneDeep(this.containerNodes)
                return true
            }

        }
        return false
    }
    render() {
        const { initDone, intl, isEdit, decomposedQA, loading, isUpdateLayout } = this.props
        if (!decomposedQA) return null
        // const { num, subNum } = this.state
        // decomposedQA = decomposedQA.slice(0, num).map(QA => {
        //     return {
        //         ...QA,
        //         facts: QA.facts.slice(0, subNum)
        //     }
        // })

        const TitleView = () => {
            return <div className='title'>
                <h1 contentEditable={isEdit}
                    title={this.getTitle()}
                    suppressContentEditableWarning
                    onBlur={() => this.endTitleEdit()}
                    ref={this.titleRef}>{`${this.getTitle() || (initDone && intl.get("inputHint"))}`}</h1>
                <div className='fullscreen_icon' onClick={this.fullscreen}></div>
                <div className='export_icon' onClick={this.export}></div>
            </div>
        }

        const SubTitleView = ({ index, subQustion, isEdit }) => {     
            let newStr = subQustion.slice(0, 1).toUpperCase() + subQustion.slice(1)
            return <div className='sub-title-box'>
                <div className='right-box'>
                    <div className={newStr === this.getTitle() ? 'right-top hightlight' : 'right-top default'}></div>
                </div>
                <div className='sub-title' style={{ borderColor: newStr === this.getTitle() ? '#F19C0F' : '#A1AEB9' }}>
                    <div className={newStr === this.getTitle() ? 'index hightlight' : 'index default'}>{index + 1}</div>
                    <h1 contentEditable={isEdit}
                        suppressContentEditableWarning
                        title={`${newStr}`}
                        onBlur={() => this.endEdit(index)} ref={this.setSubTitleRef(index)}>{`${newStr}`}</h1>
                </div>
            </div >
        }

        let columns = decomposedQA.length === 4 ? 2 : decomposedQA.length
        return (
            <div className='large-size-screen'>
                <TitleView {...this.props} />
                {/* <div className='test'>
                    View
                    <select onChange={this.change} defaultValue={defaultNum}>
                        <option value='1'>1</option>
                        <option value='2'>2</option>
                        <option value='3'>3</option>
                        <option value='4'>4</option>
                    </select>
                </div>
                <div className='sub_test'>
                    subView
                    <select onChange={this.subchange} defaultValue={defaultSubNum}>
                        <option value='1'>1</option>
                        <option value='2'>2</option>
                        <option value='3'>3</option>
                        <option value='4'>4</option>
                        <option value='5'>5</option>
                    </select>
                </div> */}
                <div className='auto-layout' style={{ columnCount: columns }}>
                    <div className='dec1'></div>
                    <div className='dec2'></div>
                    {
                        decomposedQA.length > 0 ? this.reorder(decomposedQA, columns).map((QA, index) => {
                            return (
                                <div className='subView' key={QA.id} style={{ height: decomposedQA.length === 4 ? "calc(50% - 15px)" : "100%", width: "100%" }} ref={(e) => this.setContainerRef(e)}>
                                    <div className='d1'></div>
                                    <div className='d2'></div>
                                    {
                                        decomposedQA.length > 1 && <SubTitleView  index={QA.id} subQustion={QA.question} isEdit={isEdit} />
                                    }
                                    {
                                        this.isCanGetSize() ? <AnsweredFacts QAID={index} containerSize={this.containerNodes} facts={this.setFactId(QA.facts, index)} columnNum={decomposedQA.length} isUpdateLayout={isUpdateLayout} {...this.props} />
                                            : null
                                    }
                                </div>
                            )
                        })
                            :
                            !loading && <ErrorView initDone={initDone, intl} intl={intl} />
                    }
                </div>
            </div >
        )
    }
}
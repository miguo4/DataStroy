import FactType from '@/constant/FactType'
import getSuitableBreakdownList from './getSuitableBreakdownList';
import datafilter from './datafilter';
import * as d3 from 'd3';
// import _ from 'lodash';

// chart valid
export const isValid = function (fact) {
    let isValid = false;
    switch (fact.type) {
        case FactType.ASSOCIATION:
            if (fact.measure.length === 2)
                isValid = true
            break;

        case FactType.CATEGORIZATION:
            if (fact.groupby.length)
                isValid = true
            break;

        case FactType.DIFFERENCE:
            if (fact.measure.length && fact.groupby.length && fact.focus.length >= 2)
                isValid = true
            break;

        case FactType.DISTRIBUTION:
            if (fact.measure.length && fact.groupby.length)
                isValid = true
            break;

        case FactType.EXTREME:
            if (fact.measure.length && fact.groupby.length && fact.focus.length)
                isValid = true
            break;

        case FactType.OUTLIER:
            if (fact.measure.length && fact.groupby.length && fact.focus.length)
                isValid = true
            break;

        case FactType.PROPORTION:
            if (fact.measure.length && fact.groupby.length && fact.focus.length)
                isValid = true
            break;

        case FactType.RANK:
            if (fact.measure.length && fact.groupby.length)
                isValid = true
            break;

        case FactType.TREND:
            if (fact.measure.length && fact.groupby.length)
                isValid = true
            break;

        case FactType.VALUE:
            if (fact.measure.length)
                isValid = true
            break;

        default:
            break;
    }
    return isValid
}

/***
 * 清空不必要的fact属性
 ***/
export const customizeFact = function (fact, schema, data) {
    let newFact = Object.assign({}, fact)
    switch (fact.type) {
        case FactType.ASSOCIATION:
            newFact.focus = [];
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
                const measureList = schema.filter(key => key['type'] === "numerical");
                if (newFact.measure.length === 0 && measureList.length > 0) {
                    newFact.measure = [{ "field": measureList[0].field, "aggregate": "count" }];
                }
                if (newFact.measure.length === 1) {
                    newFact.measure.push({ "field": 'COUNT', "aggregate": "count" });
                }
            }
            break;

        case FactType.CATEGORIZATION:
            newFact.measure = []
            newFact.focus = []
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
            }
            break;

        case FactType.DIFFERENCE:
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema),
                    gbValueList = getFieldValue(data, fact.groupby);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
                /***** 设默认为第1、2条，并且更新到fact中 *****/
                if (!newFact.focus.length) {
                    newFact.focus = [{
                        field: newFact.groupby[0],
                        value: gbValueList[0],
                    },
                    {
                        field: newFact.groupby[0],
                        value: gbValueList[1],
                    }
                    ]
                }
            }
            break;

        case FactType.DISTRIBUTION:
            newFact.focus = []
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
            }
            break;

        case FactType.EXTREME:
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
                // aggregation
                if (newFact.measure.length && newFact.groupby.length) {
                    let encoding = {}
                    encoding['y'] = {};
                    encoding['y']['field'] = newFact.measure[0].field;
                    encoding['y']['aggregation'] = newFact.measure[0].aggregate;
                    encoding['x'] = {};
                    encoding['x']['field'] = newFact.groupby[0];
                    let filteredData = datafilter(data, newFact.subspace)
                    let aggregatedRows = getAggregatedRows(filteredData, encoding);
                    // filter gbValueList
                    let measureField = newFact.measure[0]['field'];
                    let max = aggregatedRows.reduce((a, b) => (a[measureField] > b[measureField]) ? a : b);

                    /***** 设默认为max，并且更新到fact中 *****/
                    if (!newFact.focus.length) {
                        newFact.focus = [{
                            field: newFact.groupby[0],
                            value: max[newFact.groupby[0]],
                            extremeFocus: 'max',
                            extremeValue: max[newFact.measure[0].field]
                        }]
                    }
                }
            }
            break;

        case FactType.OUTLIER:
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
                // aggregation
                if (newFact.measure.length && newFact.groupby.length) {
                    let encoding = {}
                    encoding['y'] = {};
                    encoding['y']['field'] = newFact.measure[0].field;
                    encoding['y']['aggregation'] = newFact.measure[0].aggregate;
                    encoding['x'] = {};
                    encoding['x']['field'] = newFact.groupby[0];
                    let filteredData = datafilter(data, newFact.subspace)
                    let aggregatedRows = getAggregatedRows(filteredData, encoding);
                    // filter gbValueList
                    let newOrder = aggregatedRows.sort(function (a, b) { return b[encoding.y.field] - a[encoding.y.field]; }).map(function (d) { return d[encoding.x.field]; })
                    let newOrderValue = aggregatedRows.sort(function (a, b) { return b[encoding.y.field] - a[encoding.y.field]; }).map(function (d) { return d[encoding.y.field]; })

                    let n = newOrderValue.length
                    // 整数部分
                    let posQ3 = parseInt((n - 1) * 0.25)
                    let posQ1 = parseInt((n - 1) * 0.75)
                    // 小数部分
                    let decimalQ3 = (n - 1) * 0.25 - posQ3
                    let decimalQ1 = (n - 1) * 0.75 - posQ1
                    let Q3 = newOrderValue[posQ3] + (newOrderValue[posQ3 + 1] - newOrderValue[posQ3]) * decimalQ3
                    let Q1 = newOrderValue[posQ1] + (newOrderValue[posQ1 + 1] - newOrderValue[posQ1]) * decimalQ1

                    let Low = Q1 - 1.5 * (Q3 - Q1)
                    let Up = Q3 + 1.5 * (Q3 - Q1)
                    let outlierIndex = []
                    newOrderValue.forEach((d, i) => {
                        if (d > Up || d < Low) {
                            outlierIndex.push(i)
                        }
                    });

                    /***** 设默认为outlier，并且更新到fact中 *****/
                    if (!newFact.focus.length && outlierIndex.length) {
                        newFact.focus = [{
                            field: fact.groupby[0],
                            value: newOrder[outlierIndex[0]],
                        }]
                    }
                }
            }
            break;

        case FactType.PROPORTION:
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(fact.type, fact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }

                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
                if (newFact.measure.length && newFact.groupby.length) {
                    // aggregation
                    let encoding = {}
                    encoding['y'] = {};
                    encoding['y']['field'] = newFact.measure[0].field;
                    encoding['y']['aggregation'] = newFact.measure[0].aggregate;
                    encoding['x'] = {};
                    encoding['x']['field'] = newFact.groupby[0];
                    let filteredData = datafilter(data, newFact.subspace)
                    let aggregatedRows = getAggregatedRows(filteredData, encoding);
                    // filter gbValueList
                    let measureField = newFact.measure[0]['field'];
                    let max = aggregatedRows.reduce((a, b) => (a[measureField] > b[measureField]) ? a : b)

                    /***** 设默认为max，并且更新到fact中 *****/
                    if (!newFact.focus.length) {
                        newFact.focus = [{
                            field: newFact.groupby[0],
                            value: max[newFact.groupby[0]],
                        }]
                    }
                }
            }
            break;

        case FactType.RANK:
            newFact.focus = []
            if (schema && data) {
                const groupbyList = getSuitableBreakdownList(newFact.type, newFact.chart, schema);
                if (newFact.groupby.length === 0 && groupbyList.length > 0) {
                    newFact.groupby = [groupbyList[0].field];
                }
                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
                // if (newFact.measure.length && newFact.groupby.length) {
                //     // aggregation
                //     let encoding = {}
                //     encoding['y'] = {};
                //     encoding['y']['field'] = newFact.measure[0].field;
                //     encoding['y']['aggregation'] = newFact.measure[0].aggregate;
                //     encoding['x'] = {};
                //     encoding['x']['field'] = newFact.groupby[0];
                //     let filteredData = datafilter(data, newFact.subspace)
                //     let aggregatedRows = getAggregatedRows(filteredData, encoding);
                //     // filter gbValueList
                //     let newOrder = aggregatedRows.sort(function (a, b) { return b[encoding.y.field] - a[encoding.y.field]; }).map(function (d) { return d[encoding.x.field]; })

                //     /***** 设默认为前3，并且更新到fact中 *****/

                //     let focus = []
                //     newOrder.forEach((d, i) => {
                //         if (i < 3) {
                //             focus.push({ field: fact.groupby[0], value: d })
                //         }
                //     });
                //     if(!_.isEqual(focus, newFact.focus)){
                //         newFact.focus = focus;
                //     }
                // }
            }
            break;

        case FactType.TREND:
            newFact.focus = [];
            if (schema && data) {
                let groupbyList = schema.filter(key => key['type'] === "temporal")
                const groupbyFieldList = groupbyList.map((d) => d.field);
                if (groupbyList.length === 0) {
                    newFact.groupby = []
                } else if (newFact.groupby.length === 0 || groupbyFieldList.indexOf(newFact.groupby[0]) === -1) {
                    newFact.groupby = [groupbyList[0].field];
                }

                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
            }
            break;

        case FactType.VALUE:
            newFact.groupby = []
            newFact.focus = []
            if (schema && data) {
                if (newFact.measure.length === 0) {
                    newFact.measure = [{ "field": 'COUNT', "aggregate": "count" }];
                }
            }
            break;

        default:
            break;
    }
    return newFact
}

// fact valid for score to update(RANK/PROPORTION/OUTLIER/DIFFERENCE)
//NO USE FOR A MOMENT!!!!!
export const isFactValid = function (_fact) {
    let fact = Object.assign({}, _fact)
    let isFactValid = false;
    switch (fact.type) {
        case FactType.ASSOCIATION:
            if (fact.measure.length === 2 && fact.groupby)
                isFactValid = true
            break;

        case FactType.CATEGORIZATION:
            if (fact.groupby)
                isFactValid = true
            break;

        case FactType.DIFFERENCE:
            if (fact.measure && fact.groupby && fact.focus.length >= 2)
                isFactValid = true
            break;

        case FactType.DISTRIBUTION:
            if (fact.measure && fact.groupby)
                isFactValid = true
            break;

        case FactType.EXTREME:
            if (fact.measure && fact.groupby)
                isFactValid = true
            break;

        case FactType.OUTLIER:
            if (fact.measure && fact.groupby && fact.focus.length)
                isFactValid = true
            break;

        case FactType.PROPORTION:
            if (fact.measure && fact.groupby && fact.focus.length)
                isFactValid = true
            break;

        case FactType.RANK:
            if (fact.measure.length && fact.groupby.length && fact.focus.length >= 3)
                isFactValid = true
            break;

        case FactType.TREND:
            if (fact.measure && fact.groupby)
                isFactValid = true
            break;

        case FactType.VALUE:
            if (fact.measure)
                isFactValid = true
            break;

        default:
            break;
    }
    return isFactValid
}

const getCountRows = (rawData, encoding) => {
    let calculateData = d3.nest().key(d => d[encoding.x.field]).entries(rawData);
    let countData = new Array(calculateData.length).fill(0);
    let data = calculateData.map(function (d, i) {
        d.values.forEach(() => {
            countData[i] += 1
        })
        let countRows = Object.assign({}, d.values[0])
        countRows['COUNT'] = countData[i]
        return countRows
    });
    return data;
}

const getMinRows = (rawData, encoding) => {
    let calculateData = d3.nest().key(d => d[encoding.x.field]).entries(rawData);
    let data = calculateData.map(function (d) {
        let index = d3.scan(d.values, function (a, b) {
            if (a[encoding.y.field] && b[encoding.y.field])
                return a[encoding.y.field] - b[encoding.y.field];
        });
        if (index >= 0) {
            return d.values[index]
        } else {
            return d.values[0]
        }
    });
    return data;
}

const getMaxRows = (rawData, encoding) => {
    let calculateData = d3.nest().key(d => d[encoding.x.field]).entries(rawData);
    let data = calculateData.map(function (d, i) {
        let index = d3.scan(d.values, function (a, b) {
            if (a[encoding.y.field] && b[encoding.y.field])
                return b[encoding.y.field] - a[encoding.y.field];
        });
        if (index >= 0) {
            return d.values[index]
        } else {
            return d.values[0];
        }
    });
    return data;
}

const getSumRows = (rawData, encoding) => {
    let calculateData = d3.nest().key(d => d[encoding.x.field]).entries(rawData);
    let sumData = new Array(calculateData.length).fill(0);
    let data = calculateData.map(function (d, i) {
        d.values.forEach(d => {
            sumData[i] += d[encoding.y.field]
        })
        let sumRows = Object.assign({}, d.values[0])
        sumRows[encoding.y.field] = sumData[i]
        return sumRows
    });
    return data;
}

const getAverageRows = (rawData, encoding) => {
    let calculateData = d3.nest().key(d => d[encoding.x.field]).entries(rawData);
    let sumData = new Array(calculateData.length).fill(0);
    let data = calculateData.map(function (d, i) {
        d.values.forEach(d => {
            sumData[i] += d[encoding.y.field]
        })
        let sumRows = Object.assign({}, d.values[0])
        sumRows[encoding.y.field] = sumData[i] / d.values.length;
        return sumRows;
    });
    return data;
}

const getAggregatedRows = (rawData, encoding) => {
    let data;
    switch (encoding.y.aggregation) {
        case 'sum':
            data = getSumRows(rawData, encoding);
            break;
        case 'avg':
            data = getAverageRows(rawData, encoding);
            break;
        case 'max':
            data = getMaxRows(rawData, encoding);
            break;
        case 'min':
            data = getMinRows(rawData, encoding);
            break;
        case 'count':
            data = getCountRows(rawData, encoding)
            break;

        default:
            data = getMaxRows(rawData, encoding);
            break;
    }
    return data;
}

const getFieldValue = (rawData, fieldName) => {
    if (fieldName)
        return Array.from(new Set(rawData.map(d => d[fieldName])));
    else return []
}
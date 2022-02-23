import React from 'react';
import ChartType from '@/constant/ChartType';
import getSupportedChartTypes from './getSupportedChartTypes';
import Chart from './Chart';
import { isValid, customizeFact } from './helper';
import _ from 'lodash';

export const facts2charts = (facts, shema, chartDiversity = 0) => {
    for (let i = 0; i < facts.length; i++) {
        let supportedChartTypes = getSupportedChartTypes(shema, facts[i]);
        let choiceCount = parseInt((supportedChartTypes.length + 1) * chartDiversity);
        let choicedChartTypes = supportedChartTypes.slice(0, choiceCount + 1);
        facts[i].chart = choicedChartTypes[Math.floor(Math.random() * choicedChartTypes.length)].chart;
    }
    return facts
}
export const getChoice = (length) => {
    let choice = Math.round(Math.random() * (length - 1));
    return choice;
}


export const getFactChartType = (shema, fact, choice = 0) => {
    let supportedChartTypes = getSupportedChartTypes(fact, shema);
    if (supportedChartTypes.length === 0) return null;
    return supportedChartTypes[getChoice(supportedChartTypes.length)].chart;
}

const getvischartype = (chart) => {
    let chartType = chart;
    switch (chart) {
        case ChartType.AREA_CHART:
            chartType = "areachart";
            break;
        case ChartType.BUBBLE_CHART:
            chartType = "bubblechart";
            break;
        case ChartType.COLOR_FILLING_MAP:
            chartType = "filledmap";
            break;
        case ChartType.BUBBLE_MAP:
            chartType = "bubblemap";
            break;
        case ChartType.HALF_RING_CHART:
            chartType = "donutchart";
            break;
        case ChartType.HORIZONTAL_BAR_CHART:
            chartType = "horizentalbarchart";
            break;

        case ChartType.VERTICAL_BAR_CHART:
        case ChartType.STACKED_BAR_CHART:
        case ChartType.VERTICAL_DIFFERENCE_BAR_CHART:
        case ChartType.ISOTYPE_BAR_CHART:
        case ChartType.VERTICAL_DIFFERENCE_ARROW_CHART:
            chartType = "verticalbarchart"
            break;
        case ChartType.LINE_CHART:
        case ChartType.STACKED_LINE_CHART:
            chartType = "linechart";
            break;
        case ChartType.PROPORTION_ISOTYPE_CHART:
        case ChartType.PIE_CHART:
            chartType = "piechart";
            break;
        case ChartType.PROGRESS_BAR_CHART:
            chartType = "progresschart";
            break;
        case ChartType.RING_CHART:
            chartType = "donutchart";
            break;
        case ChartType.SCATTER_PLOT:
            chartType = "scatterplot";
            break;
        case ChartType.TEXT_CHART:
            chartType = "textchart";
            break;
        case ChartType.TREE_MAP:
            chartType = "treemap";
            break;
        default:
            break;
    }
    return chartType;
}

export const fact2chart = function (specData, containerId, fact, data, size, vegalite) {
    if (!fact.chart || fact.chart === "") {
        fact.chart = getFactChartType(specData.schema, fact);//针对生成页面的chart
    }

    let chart = fact.chart;

    if (chart === ChartType.ISOTYPE_BAR_CHART) {
        fact.chart = ChartType.VERTICAL_BAR_CHART;
    }
    fact = customizeFact(fact);//important

    if (!fact.chart || !isValid(fact)) {
        console.log("no valid", fact)
        return null;
    }

    let specChart = {
        id: containerId,
        size: size,
        type: getvischartype(chart),
        style: "business",
        duration: 0,
        showSuggestion: false,//显示图表Unsupported,
        // ...vegalite //add vegalite spec
    }

    specData = {
        ...specData,
        values: data,
    }
    let specNew = {
        data: specData,
        fact: fact,
        chart: specChart,
    }

    return <Chart spec={_.cloneDeep(specNew)} />
}
